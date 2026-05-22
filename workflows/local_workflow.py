import json
import os
import urllib.error
import urllib.request
from typing import Any

from models.debate_model import DebateArgument, DebateStance, DebateVerdict, Evidence
from model_resolver import (
    DEFAULT_LOCAL_API_BASE_URL,
    DEFAULT_LOCAL_MODEL_NAME,
)


def is_local_provider_enabled() -> bool:
    provider = os.getenv("MODEL_PROVIDER", "").strip().lower()
    return provider in {"local", "local-server", "local_server"}


def _model_name() -> str:
    return os.getenv("LOCAL_MODEL_NAME", DEFAULT_LOCAL_MODEL_NAME)


def _chat(system_prompt: str, user_prompt: str, fallback: str, max_tokens: int = 450) -> str:
    url = _ollama_chat_url()
    body = json.dumps(
        {
            "model": _model_name(),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": max_tokens,
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return f"{fallback} Local model request failed: {exc}"

    message = payload.get("message") or {}
    return message.get("content") or fallback


def _ollama_chat_url() -> str:
    base_url = os.getenv("LOCAL_API_BASE_URL", DEFAULT_LOCAL_API_BASE_URL).rstrip("/")
    if base_url.endswith("/v1"):
        base_url = base_url[:-3]
    return f"{base_url}/api/chat"


def _parse_json(text: str) -> Any | None:
    text = text.strip()
    if not text:
        return None

    for candidate in (text, _slice_json(text, "[", "]"), _slice_json(text, "{", "}")):
        if not candidate:
            continue
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


def _slice_json(text: str, start: str, end: str) -> str | None:
    start_index = text.find(start)
    end_index = text.rfind(end)
    if start_index == -1 or end_index == -1 or end_index <= start_index:
        return None
    return text[start_index : end_index + 1]


def _as_evidence_list(raw: Any, fallback_text: str, topic: str) -> list[Evidence]:
    if isinstance(raw, dict):
        raw = raw.get("evidence") or raw.get("items") or raw.get("results")

    evidence: list[Evidence] = []
    if isinstance(raw, list):
        for index, item in enumerate(raw, 1):
            if not isinstance(item, dict):
                continue
            evidence.append(
                Evidence(
                    source=str(item.get("source") or f"Local model evidence {index}"),
                    content=str(item.get("content") or item.get("summary") or item),
                    credibility_score=_clamp_float(item.get("credibility_score"), 0.6),
                )
            )

    if evidence:
        return evidence

    if fallback_text.lstrip().startswith(("[", "{")):
        fallback_text = (
            "AI can automate routine software engineering tasks, while complex design, "
            "requirements analysis, product judgment, and accountability still benefit from human engineers."
        )

    return [
        Evidence(
            source="Local model synthesis",
            content=(
                fallback_text.strip()
                or f"Local model generated general evidence for the topic: {topic}"
            )[:3000],
            credibility_score=0.5,
        )
    ]


def _as_argument(
    raw: Any,
    fallback_text: str,
    topic: str,
    stance: DebateStance,
    agent_name: str,
    evidence: list[Evidence],
    round_number: int,
) -> DebateArgument:
    data = raw if isinstance(raw, dict) else {}
    return DebateArgument(
        agent_name=str(data.get("agent_name") or agent_name),
        topic=str(data.get("topic") or topic),
        stance=stance,
        argument=str(data.get("argument") or data.get("reasoning") or fallback_text).strip()[:5000],
        confidence=_clamp_float(data.get("confidence"), 0.65),
        evidence=evidence,
        round_number=round_number,
    )


def _as_verdict(raw: Any, fallback_text: str, topic: str) -> DebateVerdict:
    data = raw if isinstance(raw, dict) else {}
    winning_stance = str(data.get("winning_stance") or "NEUTRAL").upper()
    if winning_stance not in DebateStance.__members__:
        winning_stance = "NEUTRAL"

    reasoning = str(data.get("reasoning") or fallback_text).strip()
    summary = str(data.get("summary") or reasoning[:180] or "The debate was evaluated.")

    return DebateVerdict(
        topic=str(data.get("topic") or topic),
        winning_stance=DebateStance[winning_stance],
        reasoning=reasoning[:5000],
        confidence=_clamp_float(data.get("confidence"), 0.6),
        summary=summary[:500],
    )


def _clamp_float(value: Any, default: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = default
    return min(1.0, max(0.0, number))


async def run_local_debate_workflow(topic: str, round_number: int = 1) -> dict[str, Any]:
    print("[*] Running local Researcher fallback...")
    evidence_prompt = (
        "Return concise JSON only: an array of 3 objects. Each object must have source, "
        "content, and credibility_score. Topic: "
        f"{topic}"
    )
    evidence_text = _chat(
        "You produce compact JSON for a debate research system.",
        evidence_prompt,
        f"Evidence for {topic}: automation will change software work, but adoption varies by task.",
        max_tokens=120,
    )
    evidence = _as_evidence_list(_parse_json(evidence_text), evidence_text, topic)
    evidence_str = "\n".join(
        f"- Source: {item.source} | Score: {item.credibility_score}\n  Content: {item.content}"
        for item in evidence
    )

    print("[*] Running local Optimist fallback...")
    pro_text = _chat(
        "You are the Optimist Agent. Prefer concise JSON, but clear prose is acceptable.",
        (
            "Create a PRO debate argument. JSON fields: agent_name, topic, stance, "
            "argument, confidence, round_number.\n"
            f"Topic: {topic}\nRound: {round_number}\nEvidence:\n{evidence_str}"
        ),
        f"AI will replace many routine software engineering tasks related to {topic}.",
        max_tokens=160,
    )
    pro_argument = _as_argument(
        _parse_json(pro_text),
        pro_text,
        topic,
        DebateStance.PRO,
        "Optimist Agent",
        evidence,
        round_number,
    )

    print("[*] Running local Skeptic fallback...")
    con_text = _chat(
        "You are the Skeptic Agent. Prefer concise JSON, but clear prose is acceptable.",
        (
            "Create a CON debate argument countering the PRO argument. JSON fields: "
            "agent_name, topic, stance, argument, confidence, round_number.\n"
            f"Topic: {topic}\nRound: {round_number}\nEvidence:\n{evidence_str}\n"
            f"PRO argument:\n{pro_argument.argument}"
        ),
        f"AI will augment software engineers more than fully replace them because requirements, judgment, and accountability remain human-led.",
        max_tokens=160,
    )
    con_argument = _as_argument(
        _parse_json(con_text),
        con_text,
        topic,
        DebateStance.CON,
        "Skeptic Agent",
        evidence,
        round_number,
    )

    print("[*] Running local Judge fallback...")
    verdict_text = _chat(
        "You are the Judge Agent. Prefer concise JSON, but clear prose is acceptable.",
        (
            "Evaluate both arguments. JSON fields: topic, winning_stance, reasoning, "
            "confidence, summary. winning_stance must be PRO, CON, or NEUTRAL.\n"
            f"Topic: {topic}\nEvidence:\n{evidence_str}\n"
            f"PRO:\n{pro_argument.argument}\n\nCON:\n{con_argument.argument}"
        ),
        "Both sides have merit; the likely outcome is augmentation and partial displacement rather than full replacement.",
        max_tokens=140,
    )
    verdict = _as_verdict(_parse_json(verdict_text), verdict_text, topic)

    return {
        "topic": topic,
        "evidence": evidence,
        "pro_argument": pro_argument,
        "con_argument": con_argument,
        "verdict": verdict,
    }
