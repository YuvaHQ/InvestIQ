import asyncio
from datetime import datetime

import streamlit as st

from config import (
    MOCK_SIGNALS,
    MOCK_DOCS,
    DEMO_MODE,
    MODEL_NAME,
)

from orchestrator import run_agent_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="InvestIQ | Financial Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #09111f;
        color: #e6edf7;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }

    .eyebrow {
        color: #7f93ad;
        font-size: .73rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
    }

    .app-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -.04em;
        margin: .15rem 0;
    }

    .subtle {
        color: #97a8bf;
        font-size: .92rem;
    }

    .panel-title {
        color: #aebed2;
        font-size: .75rem;
        font-weight: 700;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin-bottom: .8rem;
    }

    .price {
        font-size: 2rem;
        font-weight: 750;
    }

    .recommendation {
        background: #152b4a;
        border: 1px solid #2e5c8d;
        border-radius: 18px;
        padding: 1.35rem;
    }

    .action {
        font-size: 1.45rem;
        font-weight: 850;
        letter-spacing: .06em;
    }

    .agent-card {
        background: #101c2e;
        border: 1px solid #22344e;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: .8rem;
    }

    .agent-title {
        font-size: 1rem;
        font-weight: 700;
        color: #edf3fb;
    }

    .agent-rationale {
        color: #a8b8cc;
        line-height: 1.5;
        margin-top: .5rem;
    }

    .citation {
        display: inline-block;
        color: #8fb9ff;
        background: #162945;
        border-radius: 5px;
        padding: .2rem .4rem;
        margin: .2rem .2rem 0 0;
        font-size: .72rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def run_pipeline(symbol, profile):

    return asyncio.run(
        run_agent_pipeline(
            symbol=symbol,
            signals=MOCK_SIGNALS,
            docs=MOCK_DOCS,
            user_profile=profile,
        )
    )


def stance_icon(stance):

    if stance == "Bullish":
        return "🟢"

    if stance == "Bearish":
        return "🔴"

    return "🟡"


def recommendation_icon(recommendation):

    if recommendation in ["STRONG BUY", "BUY"]:
        return "🟢"

    if recommendation in ["STRONG SELL", "SELL"]:
        return "🔴"

    return "🟡"


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        '<div class="eyebrow">'
        'Decision Intelligence Workspace'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-title">InvestIQ</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtle">'
        'Grounded signals, transparent agent summaries, '
        'profile-aware financial analysis.'
        '</div>',
        unsafe_allow_html=True,
    )


with header_right:

    st.markdown("<br>", unsafe_allow_html=True)

    if DEMO_MODE:
        st.warning("DEMO MODE")
        st.caption(
            "Using simulated market data and mock specialist agents."
        )
    else:
        st.success("API ONLINE")
        st.caption(f"Gemini model: {MODEL_NAME}")


# ============================================================
# INVESTOR PROFILE
# ============================================================

st.markdown("---")

st.subheader("Investor Profile Capture")

st.caption(
    "Build a smart investor profile for profile-aware analysis."
)


with st.form("investor_profile_form"):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Name",
            placeholder="Enter your name",
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18,
            step=1,
        )

        income = st.number_input(
            "Income",
            min_value=0.0,
            step=1000.0,
            format="%.2f",
        )

        roi_percent = st.number_input(
            "ROI Percent",
            min_value=-100.0,
            max_value=1000.0,
            value=0.0,
            step=0.1,
        )

    with col2:

        objective = st.text_input(
            "Objective",
            placeholder="e.g. Wealth creation",
        )

        holdings = st.text_input(
            "Holdings",
            placeholder="e.g. 5 stocks, 2 ETFs",
        )

        risk_profile = st.selectbox(
            "Risk Profile",
            [
                "Conservative",
                "Moderate",
                "Aggressive",
            ],
        )

        investment_horizon = st.selectbox(
            "Investment Horizon",
            [
                "Short Term",
                "Medium Term",
                "Long Term",
            ],
        )

        portfolio_concentration = st.selectbox(
            "Portfolio Concentration",
            [
                "Low",
                "Medium",
                "High",
            ],
        )

    save_profile = st.form_submit_button(
        "Save Investor Profile",
        use_container_width=True,
    )


# ============================================================
# SAVE PROFILE
# ============================================================

if save_profile:

    st.session_state["investor_profile"] = {

        "name": name.strip() or "Investor",

        "age": int(age),

        "income": float(income),

        "roi_percent": float(roi_percent),

        "objective": (
            objective.strip()
            if objective.strip()
            else "Not specified"
        ),

        "holdings": (
            holdings.strip()
            if holdings.strip()
            else "Not specified"
        ),

        "risk_tolerance": risk_profile,

        "investment_horizon": investment_horizon,

        "portfolio_concentration":
            portfolio_concentration,
    }

    st.success("Investor profile saved.")


# ============================================================
# DEFAULT PROFILE
# ============================================================

profile = st.session_state.get(
    "investor_profile",
    {
        "risk_tolerance": "Conservative",
        "investment_horizon": "Medium Term",
        "portfolio_concentration": "Medium",
    },
)


# ============================================================
# MARKET ANALYSIS
# ============================================================

st.markdown("---")

st.subheader("Market Analysis")

st.caption(
    "Select a stock symbol and run the multi-agent financial analysis."
)


col1, col2 = st.columns([3, 1])

with col1:

    stock_symbol = st.text_input(
        "Stock Symbol",
        value="RELIANCE",
        placeholder="e.g. RELIANCE",
    ).strip().upper()

with col2:

    st.markdown("<br>", unsafe_allow_html=True)

    analyze = st.button(
        "Run Analysis",
        use_container_width=True,
    )


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze:

    if not stock_symbol:

        st.error("Please enter a stock symbol.")

    else:

        with st.spinner(
            "Running Technical → Fundamental → Sentiment → Synthesis..."
        ):

            try:

                result = run_pipeline(
                    stock_symbol,
                    profile,
                )

                st.session_state["analysis_result"] = result

            except Exception as exc:

                st.error(
                    f"Pipeline failed: {type(exc).__name__}: {exc}"
                )


# ============================================================
# GET RESULT
# ============================================================

result = st.session_state.get(
    "analysis_result"
)


if result:

    st.markdown("---")

    # ========================================================
    # TOP SUMMARY
    # ========================================================

    left, right = st.columns([1.5, 1])

    with left:

        st.markdown(
            '<div class="panel-title">'
            'Profile-Adjusted Recommendation'
            '</div>',
            unsafe_allow_html=True,
        )

        recommendation = result.final_recommendation

        st.markdown(
            f"""
            <div class="recommendation">

                <div class="action">
                    {recommendation_icon(recommendation)}
                    {recommendation}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.write(
            result.synthesis_summary
        )

        st.info(
            result.risk_adjustment_note
        )


    with right:

        st.markdown(
            '<div class="panel-title">'
            'Analysis Overview'
            '</div>',
            unsafe_allow_html=True,
        )

        st.metric(
            "Stock",
            result.symbol,
        )

        st.metric(
            "Risk Profile",
            result.user_risk_profile,
        )

        st.metric(
            "Specialist Agents",
            len(result.sub_agent_traces),
        )

        st.metric(
            "Failed Agents",
            len(result.failed_agents),
        )


    # ========================================================
    # SPECIALIST AGENTS
    # ========================================================

    st.markdown("---")

    st.subheader("Agent Reasoning Trace")

    st.caption(
        "Each specialist independently analyzes one part of the financial picture."
    )


    for trace in result.sub_agent_traces:

        icon = stance_icon(
            trace.stance
        )

        with st.container(border=True):

            st.markdown(
                f"### {icon} {trace.agent_name}"
            )

            # Stance + confidence
            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    f"**Stance:** {trace.stance}"
                )

            with c2:

                st.write(
                    f"**Confidence:** "
                    f"{trace.confidence * 100:.1f}%"
                )


            st.write(
                "**Rationale**"
            )

            st.write(
                trace.rationale
            )


            # Evidence
            if trace.evidence:

                st.write(
                    "**Evidence**"
                )

                for evidence in trace.evidence:

                    st.info(
                        f"**{evidence.source}**\n\n"
                        f"{evidence.claim}"
                    )


            # Risks
            if trace.key_risks:

                st.write(
                    "**Key Risks**"
                )

                for risk in trace.key_risks:

                    st.warning(
                        risk
                    )


    # ========================================================
    # DOMINANT FACTORS
    # ========================================================

    if result.dominant_factors:

        st.markdown("---")

        st.subheader(
            "Dominant Factors"
        )

        cols = st.columns(2)

        for index, factor in enumerate(
            result.dominant_factors
        ):

            with cols[index % 2]:

                st.info(
                    factor
                )


    # ========================================================
    # CONFLICTS
    # ========================================================

    if result.conflicts:

        st.markdown("---")

        st.subheader(
            "Signal Conflicts"
        )

        for conflict in result.conflicts:

            st.warning(
                conflict
            )


    # ========================================================
    # FAILED AGENTS
    # ========================================================

    if result.failed_agents:

        st.markdown("---")

        st.subheader(
            "Failed Agents"
        )

        for error in result.failed_agents:

            st.error(
                f"{error.agent_name} — "
                f"{error.error_type}: "
                f"{error.message}"
            )


    # ========================================================
    # JSON
    # ========================================================

    st.markdown("---")

    with st.expander(
        "View Complete JSON Output"
    ):

        st.json(
            result.model_dump()
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:

    st.caption("SYSTEM")

    st.write(
        "DEMO MODE"
        if DEMO_MODE
        else "LIVE GEMINI"
    )

with c2:

    st.caption("MODEL")

    st.write(
        MODEL_NAME
    )

with c3:

    st.caption("LAST REFRESHED")

    st.write(
        datetime.now().strftime(
            "%H:%M:%S"
        )
    )
