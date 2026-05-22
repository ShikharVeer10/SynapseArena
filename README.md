# SynapseArena
## A Multi-Agent AI Debate and Reasoning System

### Project Description
**SynapseArena** is a structured multi-agent AI system that simulates intelligent debates using specialized autonomous agents powered by PydanticAI and Pydantic schemas.

The system combines:
* Adversarial reasoning
* Evidence-grounded research
* Structured cognition
* Schema-constrained AI outputs

to create a collaborative AI debate environment where multiple agents interact, reason, challenge assumptions, and generate validated conclusions.

Unlike traditional chatbot systems, SynapseArena uses:
* Typed reasoning artifacts
* Structured validation pipelines
* Multi-agent orchestration
* Role-specialized cognition

to build reliable and interpretable AI interactions.

---

### Core Features

#### Multi-Agent Architecture
The system consists of multiple specialized agents:

| Agent | Responsibility |
|---|---|
| **Optimist Agent** | Generates supportive arguments |
| **Skeptic Agent** | Produces counterarguments and critiques |
| **Researcher Agent** | Collects factual evidence and supporting information |
| **Judge Agent (planned)** | Evaluates debate quality and produces final verdicts |

#### Structured AI Outputs
All agent responses are validated using:
* Pydantic schemas
* Constrained structured generation
* Runtime validation pipelines

This ensures:
* Reliable outputs
* Consistent reasoning structures
* Type-safe agent communication

#### Evidence-Grounded Reasoning
The Researcher Agent generates:
* Source-backed evidence
* Credibility scores
* Structured research artifacts

that can later be shared across agents to improve debate quality and reasoning accuracy.

#### Schema-Driven Cognition
The project uses:
* `BaseModel`
* `Field`
* Validators
* Enums
* Nested schemas

to transform raw LLM text into:
* Validated structured cognition objects.

---

### Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core language |
| **Pydantic** | Data validation and schema modeling |
| **PydanticAI** | Structured AI agent framework |
| **OpenAI Models** | Reasoning engine |
| **AsyncIO** | Asynchronous agent execution |

---

### CLI Model Configuration
The CLI workflow (`main.py`) resolves its model provider from environment variables.

| Variable | Purpose |
|---|---|
| `MODEL_PROVIDER` | `openai`, `google`, or `local` |
| `OPENAI_MODEL` | OpenAI model id (default `gpt-4o-mini`) |
| `GEMINI_MODEL` | Gemini model id (default `gemini-1.5-flash`) |
| `LOCAL_API_BASE_URL` | OpenAI-compatible base URL (default `http://localhost:11434/v1`) |
| `LOCAL_MODEL_NAME` | Local model name (default `llama3.2`) |
| `LOCAL_API_KEY` | Local API key (default `local-key`) |

---

### Current Architecture

```
Topic
   ↓
Researcher Agent
   ↓
Evidence Objects
   ↓
Optimist Agent ──┐
                 ├── Debate Reasoning
Skeptic Agent ───┘
   ↓
Judge Agent (planned)
   ↓
Final Verdict
```

---

### Key Engineering Concepts
This project explores:
* Multi-Agent Systems
* Structured LLM Outputs
* Schema-Constrained AI
* Agent Orchestration
* Autonomous Reasoning
* Evidence-Based AI Workflows
* Adversarial Cognition
* Typed Runtime Validation

---

### Future Enhancements
* Judge/Consensus Agent
* Debate memory systems
* Persistent agent state
* Vector-based retrieval
* Agent communication workflows
* Web UI dashboard
* Real-time streaming debates
* Multi-round debate orchestration

---

### Learning Goals
This project is designed to deeply explore:
* PydanticAI internals
* Agentic system architecture
* Schema-driven AI engineering
* Structured reasoning pipelines
* Modern autonomous AI workflows

---

### Example Use Cases
* AI Debate Simulations
* Autonomous Research Systems
* Educational AI Platforms
* Consensus Generation Systems
* AI Decision Support Systems
* Multi-Agent Reasoning Experiments

---

### Why This Project Matters
Most AI applications rely on:
```
User → Chatbot → Text Output
```

SynapseArena instead explores:
```
Multiple Specialized Agents
        ↓
Structured Reasoning
        ↓
Validated Cognition
        ↓
Collaborative Intelligence
```

<img width="1638" height="768" alt="image" src="https://github.com/user-attachments/assets/78fc26be-3170-45e3-b486-a1d7327fe2f8" />
<img width="1727" height="860" alt="image" src="https://github.com/user-attachments/assets/ca03059b-4d14-42c7-adcb-e56d76395060" />


This reflects the direction of modern AI systems engineering and agentic AI research.
