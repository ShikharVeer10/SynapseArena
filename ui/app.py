import streamlit as st
import asyncio
from dotenv import load_dotenv
import os
import sys

# Ensure project root is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import agents and schemas
from agents.researcher import researcher_agent
from agents.optimist import optimist_agent
from agents.skeptic import skeptic_agent
from agents.judge import judge_agent
from models.debate_model import Evidence, DebateArgument, DebateVerdict

from model_resolver import resolve_local_model
from workflows.local_workflow import run_local_debate_workflow

# Load environment variables
load_dotenv()

# App Configuration
st.set_page_config(
    page_title="SynapseArena | Multi-Agent AI Debate System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
<style>
    /* Global styles and typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Main Layout Styling */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, rgba(9, 9, 11, 1) 90%);
    }

    /* Cards */
    .arena-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .arena-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    /* PRO Card Customization */
    .pro-card {
        border-left: 5px solid #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(30, 41, 59, 0.4));
    }
    
    /* CON Card Customization */
    .con-card {
        border-left: 5px solid #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.05), rgba(30, 41, 59, 0.4));
    }
    
    /* Verdict Card styling */
    .verdict-card {
        border: 1px solid rgba(99, 102, 241, 0.4);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(30, 41, 59, 0.6));
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.15);
    }
    
    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    
    .badge-pro {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .badge-con {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .badge-neutral {
        background-color: rgba(156, 163, 175, 0.2);
        color: #d1d5db;
        border: 1px solid rgba(156, 163, 175, 0.3);
    }
    
    .badge-credibility {
        background-color: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Progress Bars Customization */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #6366f1, #4f46e5);
    }

    /* Info text */
    .caption-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to run the async debate components sequentially to capture steps
async def execute_debate_step_by_step(topic: str, model_id, status_container) -> dict:
    # 1. Research phase
    status_container.update(label=f"🔍 Researcher Agent: Gathering evidence & facts using {model_id}...", state="running")
    research_prompt = f"Gather factual evidence (both pro and con) for the topic: {topic}"
    research_result = await researcher_agent.run(research_prompt, model=model_id)
    evidence_list: list[Evidence] = research_result.output
    
    evidence_str = "\n".join([
        f"- Source: {e.source} | Score: {e.credibility_score}\n  Content: {e.content}"
        for e in evidence_list
    ])
    
    # 2. Optimist PRO phase
    status_container.update(label=f"🟢 Optimist Agent: Generating supportive PRO arguments using {model_id}...", state="running")
    optimist_prompt = (
        f"Topic: {topic}\n"
        f"Round: 1\n"
        f"Use the following research evidence where appropriate to build your stance:\n"
        f"{evidence_str}\n\n"
        f"Generate a strong supporting argument (PRO) for the topic."
    )
    optimist_result = await optimist_agent.run(optimist_prompt, model=model_id)
    pro_argument: DebateArgument = optimist_result.output
    pro_argument.evidence = evidence_list
    
    # 3. Skeptic CON phase
    status_container.update(label=f"🔴 Skeptic Agent: Reviewing PRO stance & constructing CON counters using {model_id}...", state="running")
    skeptic_prompt = (
        f"Topic: {topic}\n"
        f"Round: 1\n"
        f"Research evidence gathered:\n"
        f"{evidence_str}\n\n"
        f"Optimist's (PRO) Argument:\n"
        f"{pro_argument.argument}\n\n"
        f"Generate a strong opposing argument (CON) countering the Optimist's points."
    )
    skeptic_result = await skeptic_agent.run(skeptic_prompt, model=model_id)
    con_argument: DebateArgument = skeptic_result.output
    con_argument.evidence = evidence_list
    
    # 4. Judge Verdict phase
    status_container.update(label=f"⚖️ Judge Agent: Evaluating arguments and evidence using {model_id}...", state="running")
    judge_prompt = (
        f"Topic: {topic}\n"
        f"Research Evidence:\n"
        f"{evidence_str}\n\n"
        f"Optimist (PRO) Argument:\n"
        f"{pro_argument.argument}\n\n"
        f"Skeptic (CON) Argument:\n"
        f"{con_argument.argument}\n\n"
        f"Evaluate both arguments and provide your final verdict."
    )
    judge_result = await judge_agent.run(judge_prompt, model=model_id)
    verdict: DebateVerdict = judge_result.output
    
    status_container.update(label="✅ Debate Complete! Verdict rendered.", state="complete")
    
    return {
        "topic": topic,
        "evidence": evidence_list,
        "pro_argument": pro_argument,
        "con_argument": con_argument,
        "verdict": verdict
    }

# Sidebar - Settings and Configuration
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400&auto=format&fit=crop&q=60", use_container_width=True)
    st.markdown("## ⚙️ Arena Settings")
    
    # Provider selection
    provider = st.selectbox(
        "Select Model Provider:",
        options=["OpenAI", "Google Gemini", "Local Server (Ollama, LM Studio, etc.)"],
        index=0
    )
    
    # Model selection depending on provider
    key_env_var = None
    custom_api_key = ""
    local_base_url = ""
    local_model_name = ""
    
    if provider == "OpenAI":
        model_name = st.selectbox(
            "Select Model:",
            options=["gpt-4o-mini", "gpt-4o", "o1-mini"],
            index=0
        )
        model_id = f"openai-chat:{model_name}"
        key_env_var = "OPENAI_API_KEY"
    elif provider == "Google Gemini":
        model_name = st.selectbox(
            "Select Model:",
            options=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.5-flash"],
            index=0
        )
        model_id = f"google:{model_name}"
        key_env_var = "GEMINI_API_KEY"
    else:
        # Local Server Settings
        local_base_url = st.text_input(
            "Local Server API URL:",
            value="http://localhost:11434/v1",
            help="E.g., http://localhost:11434/v1 for Ollama, http://localhost:1234/v1 for LM Studio."
        )
        local_model_name = st.text_input(
            "Model Name:",
            value="llama3.2",
            help="Enter the exact name of the locally pulled model (e.g. llama3.2, mistral, gemma2)."
        )
        model_id = "local-server"
        
    # Optional dynamic API key (only for OpenAI and Google Gemini)
    if provider in ["OpenAI", "Google Gemini"]:
        custom_api_key = st.text_input(
            f"Enter Custom {provider} API Key (optional):",
            type="password",
            placeholder=f"Leave blank to use environment {key_env_var}"
        )
    
    st.divider()
    st.markdown("### Suggested Topics to Explore")
    suggested_topics = [
        "Artificial Intelligence will make traditional coding obsolete",
        "Universal Basic Income is necessary in an automated economy",
        "Remote work is superior to in-office work for overall productivity",
        "Space exploration is a critical priority for humanity's survival"
    ]
    
    selected_suggested = st.selectbox("Quick-fill Topic:", ["-- Select a topic --"] + suggested_topics)

# Main Dashboard Content
st.markdown("<h1 style='text-align: center; color: #ffffff;'>⚔️ Synapse Arena ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.15rem; margin-bottom: 2rem;'>Multi-Agent AI Debate & Structured Reasoning Environment</p>", unsafe_allow_html=True)

# API Key Validation Notice for Cloud Providers
active_api_key = None
if provider in ["OpenAI", "Google Gemini"]:
    active_api_key = custom_api_key.strip() or os.getenv(key_env_var)
    if not active_api_key:
        st.warning(f"⚠️ No active `{key_env_var}` detected. Please provide a custom API key in the sidebar or configure it in a `.env` file.")

# User Input Form
st.markdown("### 📢 Issue the Challenge")
default_topic = ""
if selected_suggested != "-- Select a topic --":
    default_topic = selected_suggested
else:
    default_topic = "AI will replace most software engineers in the future"

topic_input = st.text_area(
    "Enter the topic for the AI Agents to debate:",
    value=default_topic,
    height=80,
    placeholder="E.g., Genetically modified organisms are essential to feed the growing world population."
)

start_debate = st.button("🚀 Run Debate Arena", use_container_width=True)

if start_debate:
    if not topic_input.strip():
        st.error("Please enter a valid debate topic.")
    elif provider in ["OpenAI", "Google Gemini"] and not active_api_key:
        st.error(f"Cannot start: Please provide a valid {provider} API Key in the sidebar or environment.")
    else:
        # Dynamically set the API key in system environment if cloud provider
        if provider in ["OpenAI", "Google Gemini"] and custom_api_key.strip():
            os.environ[key_env_var] = custom_api_key.strip()
            if provider == "Google Gemini":
                os.environ["GOOGLE_API_KEY"] = custom_api_key.strip()
                
        # Resolve target model identifier/object
        resolved_model = None
        if provider in ["OpenAI", "Google Gemini"]:
            resolved_model = model_id
        else:
            # Create a local OpenAI-compatible provider
            try:
                resolved_model = resolve_local_model(local_base_url, local_model_name)
            except Exception as ex:
                st.error(f"Failed to initialize local model provider: {ex}")
                st.stop()
                
        # Initialize debate execution container
        status_box = st.status("Initializing agents...", expanded=True)
        
        try:
            # Execute debate asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                if provider == "Local Server (Ollama, LM Studio, etc.)":
                    status_box.update(label="Running local model debate...", state="running")
                    result = loop.run_until_complete(run_local_debate_workflow(topic_input))
                    status_box.update(label="✅ Debate Complete! Verdict rendered.", state="complete")
                else:
                    result = loop.run_until_complete(execute_debate_step_by_step(topic_input, resolved_model, status_box))
            finally:
                loop.close()
                asyncio.set_event_loop(None)
            
            # Save results in session state to persist through UI interactions
            st.session_state["debate_results"] = result
            
        except Exception as e:
            status_box.update(label="❌ Error running debate", state="error")
            st.error(f"An error occurred: {str(e)}")

# Render results if available in session state
if "debate_results" in st.session_state:
    res = st.session_state["debate_results"]
    verdict = res["verdict"]
    pro = res["pro_argument"]
    con = res["con_argument"]
    evidence = res["evidence"]
    
    st.divider()
    
    # 1. JUDGE'S VERDICT SECTION
    st.markdown("## ⚖️ Judge's Final Verdict")
    
    # Custom colored banner depending on the winner
    if verdict.winning_stance == "PRO":
        border_color = "#10b981"
        badge_html = "<span class='badge badge-pro'>🏆 PRO WINS</span>"
    elif verdict.winning_stance == "CON":
        border_color = "#ef4444"
        badge_html = "<span class='badge badge-con'>🏆 CON WINS</span>"
    else:
        border_color = "#9ca3af"
        badge_html = "<span class='badge badge-neutral'>🤝 TIE / NEUTRAL</span>"
        
    st.markdown(f"""
    <div class="arena-card verdict-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div>{badge_html}</div>
            <div style="color: #a5b4fc; font-weight: 600;">Judge Confidence: {verdict.confidence * 100:.1f}%</div>
        </div>
        <h3 style="margin-top: 0; font-size: 1.5rem; color: #ffffff;">{verdict.summary}</h3>
        <p style="color: #cbd5e1; line-height: 1.6; font-size: 1.05rem; white-space: pre-wrap;">{verdict.reasoning}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. DEBATE ARGUMENTS COMPARISON
    st.markdown("## ⚔️ The Debate")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Optimist Argument (PRO)
        st.markdown(f"""
        <div class="arena-card pro-card">
            <span class="badge badge-pro">🟢 STANCE: PRO</span>
            <div class="caption-label">Agent Name</div>
            <h4 style="margin: 0 0 12px 0; color: #ffffff;">{pro.agent_name}</h4>
            <div class="caption-label">Main Claim & Reasoning</div>
            <p style="color: #e2e8f0; line-height: 1.6; font-size: 0.95rem; white-space: pre-wrap;">{pro.argument}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Agent Confidence:** {pro.confidence * 100:.1f}%")
        st.progress(pro.confidence)
        
    with col2:
        # Skeptic Argument (CON)
        st.markdown(f"""
        <div class="arena-card con-card">
            <span class="badge badge-con">🔴 STANCE: CON</span>
            <div class="caption-label">Agent Name</div>
            <h4 style="margin: 0 0 12px 0; color: #ffffff;">{con.agent_name}</h4>
            <div class="caption-label">Main Claim & Reasoning</div>
            <p style="color: #e2e8f0; line-height: 1.6; font-size: 0.95rem; white-space: pre-wrap;">{con.argument}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Agent Confidence:** {con.confidence * 100:.1f}%")
        st.progress(con.confidence)
        
    st.divider()
    
    # 3. RESEARCH EVIDENCE VAULT
    st.markdown("## 📋 Factual Evidence Vault")
    st.markdown("The Researcher Agent gathered the following supporting data points from academic, statistical, and industry sources:")
    
    ev_col1, ev_col2 = st.columns(2)
    
    for idx, ev in enumerate(evidence):
        target_col = ev_col1 if idx % 2 == 0 else ev_col2
        with target_col:
            # Color indicator for credibility score
            score_color = "#34d399" if ev.credibility_score >= 0.8 else ("#fbbf24" if ev.credibility_score >= 0.5 else "#f87171")
            
            st.markdown(f"""
            <div class="arena-card" style="padding: 16px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-weight: 700; color: #a5b4fc; font-size: 0.9rem;">{ev.source.upper()}</div>
                    <div>
                        <span class="badge" style="background-color: rgba(99, 102, 241, 0.1); color: {score_color}; border: 1px solid rgba(255, 255, 255, 0.15)">
                            Credibility: {ev.credibility_score:.2f}
                        </span>
                    </div>
                </div>
                <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; margin: 0;">{ev.content}</p>
            </div>
            """, unsafe_allow_html=True)
