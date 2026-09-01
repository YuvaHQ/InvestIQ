import asyncio
from datetime import datetime
from typing import Any

import streamlit as st

from config import (
    MOCK_SIGNALS,
    MOCK_DOCS,
    MOCK_USER_PROFILE,
    DEMO_MODE,
    MODEL_NAME,
)

from orchestrator import run_agent_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Astra | Financial Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #09111f;
        color: #e6edf7;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2.2rem;
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
        font-size: 2.1rem;
        font-weight: 750;
        letter-spacing: -.04em;
        margin: .15rem 0;
    }

    .subtle {
        color: #97a8bf;
        font-size: .92rem;
    }

    .panel {
        background: #101c2e;
        border: 1px solid #22344e;
        border-radius: 16px;
        padding: 1.1rem 1.15rem;
        margin-bottom: .75rem;
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
        letter-spacing: -.04em;
    }

    .up {
        color: #55d6a6;
    }

    .down {
        color: #ff8b9c;
    }

    .signal-name {
        color: #dae4f1;
        font-weight: 650;
        font-size: .9rem;
    }

    .signal-value {
        color: #91a4bd;
        font-size: .82rem;
    }

    .pill {
        display: inline-block;
        border-radius: 999px;
        padding: .22rem .52rem;
        font-size: .67rem;
        font-weight: 800;
        letter-spacing: .04em;
    }

    .pill.positive {
        background: #123c35;
        color: #69e3b6;
    }

    .pill.caution {
        background: #443717;
        color: #f3ca66;
    }

    .pill.negative {
        background: #45232c;
        color: #ff9aaa;
    }

    .pill.neutral {
        background: #26364e;
        color: #bfd0e8;
    }

    .trace-dot {
        color: #65d9b1;
        font-size: 1rem;
        line-height: 1;
    }

    .agent-name {
        font-weight: 700;
        color: #edf3fb;
    }

    .trace-copy {
        color: #a8b8cc;
        line-height: 1.45;
        font-size: .89rem;
    }

    .citation {
        display: inline-block;
        color: #8fb9ff;
        background: #162945;
        border-radius: 5px;
        padding: .16rem .38rem;
        margin: .35rem .28rem 0 0;
        font-size: .72rem;
    }

    .recommendation {
        background: linear-gradient(135deg, #152b4a, #122037);
        border: 1px solid #2e5c8d;
        border-radius: 18px;
        padding: 1.35rem;
    }

    .action {
        font-size: 1.45rem;
        font-weight: 850;
        letter-spacing: .06em;
        color: #68dfb5;
    }

    .rec-headline {
        font-size: 1.16rem;
        font-weight: 700;
        margin: .35rem 0 .55rem;
        line-height: 1.35;
    }

    .portfolio-row {
        padding: .55rem 0;
        border-bottom: 1px solid #20324b;
    }

    .portfolio-row:last-child {
        border-bottom: 0;
    }

    .metric-label {
        color: #8295af;
        font-size: .73rem;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .metric-value {
        color: #eaf2fd;
        font-size: 1.05rem;
        font-weight: 700;
    }

    .input-card {
        background: linear-gradient(
            135deg,
            rgba(20,40,68,0.96),
            rgba(12,21,33,0.96)
        );
        border: 1px solid #314d76;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin: 1rem 0 1.2rem;
    }

    .input-card .title {
        font-size: 1.35rem;
        font-weight: 750;
        letter-spacing: -.03em;
        color: #eef5ff;
        margin-bottom: .2rem;
    }

    .input-card .subtitle {
        color: #9db0c9;
        font-size: .87rem;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label {
        color: #aebed2 !important;
        font-size: .78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .stButton button {
        border-radius: 9px;
        border: 1px solid #38557a;
        background: #142844;
        color: #e4efff;
        font-weight: 650;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def pill(text: str, kind: str = "neutral") -> str:
    return f'<span class="pill {kind}">{text}</span>'


def stance_class(stance: str) -> str:
    stance = stance.upper()

    if stance == "BULLISH":
        return "positive"

    if stance == "BEARISH":
        return "negative"

    return "neutral"


def recommendation_class(recommendation: str) -> str:
    if "BUY" in recommendation:
        return "positive"

    if "SELL" in recommendation:
        return "negative"

    return "caution"


def build_signals_for_profile(
    risk_profile: str,
    investment_horizon: str,
) -> dict[str, Any]:
    """
    Convert the existing mock signal format into the format expected
    by the current multi-agent backend.
    """

    return {
        **MOCK_SIGNALS,
        "risk_profile": risk_profile,
        "investment_horizon": investment_horizon,
    }


def build_docs() -> list:
    """
    Return the documents expected by the fundamental agent.
    """

    return MOCK_DOCS


def build_user_profile(
    risk_profile: str,
    investment_horizon: str,
    portfolio_concentration: str,
) -> dict:
    """
    Build the profile consumed by orchestrator.py.
    """

    return {
        "risk_tolerance": risk_profile,
        "investment_horizon": investment_horizon,
        "portfolio_concentration": portfolio_concentration,
        "sector_allocation": MOCK_USER_PROFILE.get(
            "sector_allocation",
            "Not specified",
        ),
    }


def run_pipeline_sync(
    symbol: str,
    signals: dict,
    docs: list,
    user_profile: dict,
):
    """
    Streamlit runs synchronously, while the backend pipeline is async.
    This helper bridges the two.
    """

    return asyncio.run(
        run_agent_pipeline(
            symbol=symbol,
            signals=signals,
            docs=docs,
            user_profile=user_profile,
        )
    )


# ============================================================
# HEADER
# ============================================================

title_col, status_col = st.columns([4, 1])

with title_col:

    st.markdown(
        """
        <div class="eyebrow">
            Decision intelligence workspace
        </div>

        <div class="app-title">
            Astra Finance
        </div>

        <div class="subtle">
            Grounded signals, transparent agent summaries,
            profile-aware recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )


with status_col:

    st.markdown("<br>", unsafe_allow_html=True)

    if DEMO_MODE:

        st.markdown(
            pill("DEMO MODE", "caution"),
            unsafe_allow_html=True,
        )

        st.caption(
            "Using simulated market data and mock specialist agents."
        )

    else:

        st.markdown(
            pill("API ONLINE", "positive"),
            unsafe_allow_html=True,
        )

        st.caption(
            f"Gemini model: {MODEL_NAME}"
        )


# ============================================================
# INVESTOR PROFILE
# ============================================================

st.markdown(
    """
    <div class="input-card">
        <div class="title">
            Investor Profile Capture
        </div>

        <div class="subtitle">
            Build a smart investor profile for profile-aware analysis.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.form("investor_profile_form"):

    col1, col2, col3 = st.columns(3)

    with col1:

        name = st.text_input(
            "Name",
            placeholder="Enter name",
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=30,
            step=1,
        )

    with col2:

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
            format="%.2f",
        )

    with col3:

        objective = st.text_input(
            "Objective",
            placeholder="e.g. Wealth creation",
        )

        holdings = st.text_input(
            "Holdings",
            placeholder="e.g. 5 stocks, 2 ETFs, 1 Bond",
        )

    st.markdown("### Analysis Preferences")

    pref1, pref2, pref3 = st.columns(3)

    with pref1:

        risk_profile = st.selectbox(
            "Risk Profile",
            [
                "Conservative",
                "Moderate",
                "Aggressive",
            ],
            index=0,
        )

    with pref2:

        investment_horizon = st.selectbox(
            "Investment Horizon",
            [
                "Short Term",
                "Medium Term",
                "Long Term",
            ],
            index=1,
        )

    with pref3:

        portfolio_concentration = st.selectbox(
            "Portfolio Concentration",
            [
                "Low",
                "Medium",
                "High",
            ],
            index=2,
        )

    submitted = st.form_submit_button(
        "Save Investor Profile",
        use_container_width=True,
    )


if submitted:

    st.session_state["investor_profile"] = {
        "name": name.strip() if name.strip() else "Unknown",
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
        "portfolio_concentration": portfolio_concentration,
    }

    st.success("Investor profile saved successfully.")


# ============================================================
# STOCK ANALYSIS INPUT
# ============================================================

st.markdown(
    """
    <div class="input-card">
        <div class="title">
            Market Analysis
        </div>

        <div class="subtitle">
            Select a stock symbol and run the multi-agent financial analysis.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


stock_col, button_col = st.columns([4, 1])

with stock_col:

    stock_symbol = st.text_input(
        "Stock Symbol",
        value="RELIANCE",
        placeholder="e.g. RELIANCE",
    ).strip().upper()


with button_col:

    st.markdown("<br>", unsafe_allow_html=True)

    analyze_button = st.button(
        "Run Analysis",
        use_container_width=True,
    )


# ============================================================
# DEFAULT PROFILE
# ============================================================

if "investor_profile" not in st.session_state:

    st.session_state["investor_profile"] = {
        "name": "Demo Investor",
        "age": 30,
        "income": 0.0,
        "roi_percent": 0.0,
        "objective": "Wealth creation",
        "holdings": "5 stocks, 2 ETFs",
        "risk_tolerance": "Conservative",
        "investment_horizon": "Medium Term",
        "portfolio_concentration": "High",
    }


profile = st.session_state["investor_profile"]


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_button:

    if not stock_symbol:

        st.error("Please enter a stock symbol.")

    else:

        backend_risk = profile.get(
            "risk_tolerance",
            "Moderate",
        )

        backend_horizon = profile.get(
            "investment_horizon",
            "Medium Term",
        )

        backend_concentration = profile.get(
            "portfolio_concentration",
            "Medium",
        )

        signals = build_signals_for_profile(
            backend_risk,
            backend_horizon,
        )

        docs = build_docs()

        user_profile = build_user_profile(
            risk_profile=backend_risk,
            investment_horizon=backend_horizon,
            portfolio_concentration=backend_concentration,
        )

        with st.spinner(
            "Running Technical, Fundamental and Sentiment agents..."
        ):

            try:

                result = run_pipeline_sync(
                    symbol=stock_symbol,
                    signals=signals,
                    docs=docs,
                    user_profile=user_profile,
                )

                st.session_state["analysis_result"] = result

                st.success(
                    "Multi-agent analysis completed successfully."
                )

            except Exception as exc:

                st.error(
                    f"Analysis failed: {type(exc).__name__}: {exc}"
                )


# ============================================================
# GET CURRENT RESULT
# ============================================================

result = st.session_state.get(
    "analysis_result"
)


# ============================================================
# NO RESULT YET
# ============================================================

if result is None:

    st.divider()

    st.info(
        "Enter an investor profile and click **Run Analysis** "
        "to start the multi-agent pipeline."
    )

    st.stop()


# ============================================================
# RESULT HEADER
# ============================================================

st.divider()

st.markdown(
    f"""
    <div class="eyebrow">
        Analysis complete
    </div>

    <div class="app-title">
        {result.symbol}
    </div>

    <div class="subtle">
        Profile-adjusted multi-agent financial intelligence
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MAIN COLUMNS
# ============================================================

left, center, right = st.columns(
    [1.03, 1.38, 1.12],
    gap="large",
)


# ============================================================
# LEFT — MARKET / AGENTS
# ============================================================

with left:

    st.markdown(
        '<div class="panel-title">Market Signals</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="panel">

            <div class="signal-name">
                {result.symbol}
            </div>

            <div class="subtle">
                Multi-agent signal aggregation
            </div>

            <br>

            <div class="signal-name">
                Overall Classification
            </div>

            {pill(
                result.final_recommendation,
                recommendation_class(result.final_recommendation)
            )}

        </div>
        """,
        unsafe_allow_html=True,
    )

    for trace in result.sub_agent_traces:

        st.markdown(
            f"""
            <div class="panel">

                <div class="signal-name">
                    {trace.agent_name}
                </div>

                <div style="margin-top:.45rem">
                    {pill(
                        trace.stance.upper(),
                        stance_class(trace.stance)
                    )}
                </div>

                <div class="signal-value"
                     style="margin-top:.45rem">

                    Confidence:
                    {trace.confidence * 100:.1f}%

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# CENTER — AGENT REASONING
# ============================================================

with center:

    st.markdown(
        '<div class="panel-title">Agent Reasoning Trace</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Concise, reviewable summaries from each specialist agent."
    )

    for trace in result.sub_agent_traces:

        evidence_html = ""

        for evidence in trace.evidence:

            evidence_html += (
                f'<span class="citation">'
                f'{evidence.source}'
                f'</span>'
            )

        risks_html = ""

        if trace.key_risks:

            risks_html = (
                '<div style="margin-top:.55rem">'
                '<div class="signal-value">Key risks</div>'
            )

            for risk in trace.key_risks:

                risks_html += (
                    f'<div class="trace-copy">'
                    f'• {risk}'
                    f'</div>'
                )

            risks_html += "</div>"

        st.markdown(
            f"""
            <div class="panel">

                <div class="trace-dot">
                    ●

                    <span class="agent-name">
                        {trace.agent_name}
                    </span>

                    {pill(
                        trace.stance.upper(),
                        stance_class(trace.stance)
                    )}

                </div>

                <div class="trace-copy"
                     style="margin-top:.55rem">

                    {trace.rationale}

                </div>

                <div style="margin-top:.4rem">

                    {evidence_html}

                </div>

                {risks_html}

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# RIGHT — FINAL RECOMMENDATION
# ============================================================

with right:

    st.markdown(
        '<div class="panel-title">'
        'Profile-Adjusted Recommendation'
        '</div>',
        unsafe_allow_html=True,
    )

    recommendation_kind = recommendation_class(
        result.final_recommendation
    )

    st.markdown(
        f"""
        <div class="recommendation">

            <div class="action">
                {result.final_recommendation}
            </div>

            <div class="rec-headline">
                Multi-agent synthesis
            </div>

            <div class="trace-copy">
                {result.synthesis_summary}
            </div>

            <div style="margin-top:.9rem">

                {pill(
                    result.user_risk_profile,
                    "caution"
                )}

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="panel-title" '
        'style="margin-top:1.25rem">'
        'Risk Adjustment'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="panel">

            <div class="trace-copy">
                {result.risk_adjustment_note}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DOMINANT FACTORS
# ============================================================

st.divider()

factor_col, conflict_col = st.columns(
    [1, 1],
    gap="large",
)


with factor_col:

    st.markdown(
        '<div class="panel-title">'
        'Dominant Factors'
        '</div>',
        unsafe_allow_html=True,
    )

    if result.dominant_factors:

        for factor in result.dominant_factors:

            st.markdown(
                f"""
                <div class="panel">
                    <div class="trace-copy">
                        • {factor}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.info("No dominant factors returned.")


# ============================================================
# CONFLICTS
# ============================================================

with conflict_col:

    st.markdown(
        '<div class="panel-title">'
        'Signal Conflicts'
        '</div>',
        unsafe_allow_html=True,
    )

    if result.conflicts:

        for conflict in result.conflicts:

            st.markdown(
                f"""
                <div class="panel">
                    <div class="trace-copy">
                        ⚠ {conflict}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.success(
            "No major conflicts were reported."
        )


# ============================================================
# FAILED AGENTS
# ============================================================

if result.failed_agents:

    st.divider()

    st.markdown(
        '<div class="panel-title">'
        'Failed Agents'
        '</div>',
        unsafe_allow_html=True,
    )

    for error in result.failed_agents:

        st.warning(
            f"{error.agent_name} failed — "
            f"{error.error_type}: "
            f"{error.message}"
        )


# ============================================================
# INVESTOR PROFILE SUMMARY
# ============================================================

st.divider()

st.markdown(
    '<div class="panel-title">'
    'Investor Profile'
    '</div>',
    unsafe_allow_html=True,
)

profile_a, profile_b, profile_c, profile_d = st.columns(4)

with profile_a:

    st.markdown(
        f"""
        <div class="metric-label">
            Investor
        </div>

        <div class="metric-value">
            {profile["name"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

with profile_b:

    st.markdown(
        f"""
        <div class="metric-label">
            Risk Profile
        </div>

        <div class="metric-value">
            {profile["risk_tolerance"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

with profile_c:

    st.markdown(
        f"""
        <div class="metric-label">
            Horizon
        </div>

        <div class="metric-value">
            {profile["investment_horizon"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

with profile_d:

    st.markdown(
        f"""
        <div class="metric-label">
            Concentration
        </div>

        <div class="metric-value">
            {profile["portfolio_concentration"]}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SYSTEM METRICS
# ============================================================

st.divider()

metric_a, metric_b, metric_c = st.columns(3)

with metric_a:

    st.markdown(
        '<div class="metric-label">Pipeline</div>'
        '<div class="metric-value">3 Specialist Agents</div>',
        unsafe_allow_html=True,
    )

with metric_b:

    st.markdown(
        '<div class="metric-label">Mode</div>'
        f'<div class="metric-value">'
        f'{"DEMO" if DEMO_MODE else "LIVE GEMINI"}'
        f'</div>',
        unsafe_allow_html=True,
    )

with metric_c:

    st.markdown(
        '<div class="metric-label">Last Refreshed</div>'
        f'<div class="metric-value">'
        f'{datetime.now().strftime("%H:%M:%S")}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# RAW JSON
# ============================================================

with st.expander("View complete pipeline JSON"):

    st.json(
        result.model_dump()
    )