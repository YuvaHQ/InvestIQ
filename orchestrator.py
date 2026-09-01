import json

from config import (
    DEMO_MODE,
)

from schemas import (
    SubAgentOutput,
    FinalSynthesisOutput,
    AgentError,
)

from agents import (
    run_technical_agent,
    run_fundamental_agent,
    run_sentiment_agent,
    generate_structured,
)


# ============================================================
# SAFE AGENT EXECUTION
# ============================================================

async def safe_agent_call(
    agent_name,
    agent_function,
    data
):

    try:

        result = await agent_function(data)

        return result, None

    except Exception as exc:

        print(
            f"[WARNING] {agent_name} failed: {exc}"
        )

        error = AgentError(
            agent_name=agent_name,
            error_type=type(exc).__name__,
            message=str(exc)[:500]
        )

        return None, error


# ============================================================
# DEMO SYNTHESIS
# ============================================================

def create_demo_synthesis(
    symbol,
    sub_agent_results,
    failed_agents,
    user_profile
):

    return FinalSynthesisOutput(

        symbol=symbol,

        user_risk_profile=user_profile.get(
            "risk_tolerance",
            "Moderate"
        ),

        final_recommendation="HOLD / CAUTION",

        synthesis_summary=(
            "Fundamental and sentiment signals are positive, "
            "but the technical agent identifies short-term "
            "overbought conditions and elevated volume. "
            "Because the user has a conservative risk profile "
            "and high sector concentration, the system favors "
            "caution instead of issuing a BUY recommendation."
        ),

        risk_adjustment_note=(
            "The conservative risk profile increases the "
            "weight given to downside protection. High energy "
            "sector concentration further reduces the "
            "attractiveness of taking additional exposure."
        ),

        dominant_factors=[
            "Strong profit growth",
            "Reduced debt-to-equity ratio",
            "Positive market sentiment",
            "RSI in overbought territory",
            "Elevated trading volume",
            "High portfolio concentration"
        ],

        conflicts=[
            "Fundamental analysis is Bullish while "
            "technical analysis is Bearish.",
            "Positive sentiment conflicts with "
            "short-term technical risk."
        ],

        sub_agent_traces=sub_agent_results,

        failed_agents=failed_agents
    )


# ============================================================
# LIVE SYNTHESIS
# ============================================================

async def synthesize_master_recommendation(
    symbol: str,
    sub_agent_results: list[SubAgentOutput],
    failed_agents: list[AgentError],
    user_profile: dict,
) -> FinalSynthesisOutput:

    if not sub_agent_results:
        raise RuntimeError(
            "No specialist agent results available."
        )

    if DEMO_MODE:

        return create_demo_synthesis(
            symbol,
            sub_agent_results,
            failed_agents,
            user_profile
        )

    agent_data = [
        result.model_dump()
        for result in sub_agent_results
    ]

    failed_data = [
        error.model_dump()
        for error in failed_agents
    ]

    prompt = f"""
You are the Lead Portfolio Synthesis Agent.

Combine the independent specialist analyses below.

STOCK:
{symbol}

USER PROFILE:
{json.dumps(user_profile, indent=2)}

SPECIALIST ANALYSES:
{json.dumps(agent_data, indent=2)}

FAILED AGENTS:
{json.dumps(failed_data, indent=2)}

RULES:

1. Consider each specialist independently.
2. Do not blindly use majority voting.
3. Consider evidence quality and confidence.
4. Identify conflicts explicitly.
5. Never invent missing information.
6. If an important agent failed, increase caution.
7. Conservative users require stronger downside protection.
8. Aggressive users may give more weight to momentum.
9. High portfolio concentration is an additional risk.
10. Recommendation must be one of:

STRONG BUY
BUY
HOLD / CAUTION
SELL
STRONG SELL

11. Explain the recommendation.
12. Explain the effect of the user's risk profile.
13. List dominant factors.
14. List conflicts.

Return structured output only.
"""

    result = await generate_structured(
        prompt,
        FinalSynthesisOutput
    )

    result.symbol = symbol

    result.user_risk_profile = user_profile.get(
        "risk_tolerance",
        "Moderate"
    )

    result.sub_agent_traces = sub_agent_results

    result.failed_agents = failed_agents

    return result


# ============================================================
# MAIN PIPELINE
# ============================================================

async def run_agent_pipeline(
    symbol: str,
    signals: dict,
    docs: list,
    user_profile: dict,
) -> FinalSynthesisOutput:

    print(
        "\n[ORCHESTRATOR] Starting specialist agents..."
    )

    # --------------------------------------------------------
    # TECHNICAL
    # --------------------------------------------------------

    technical_result, technical_error = (
        await safe_agent_call(
            "Technical Analysis Agent",
            run_technical_agent,
            signals
        )
    )

    # --------------------------------------------------------
    # FUNDAMENTAL
    # --------------------------------------------------------

    fundamental_result, fundamental_error = (
        await safe_agent_call(
            "Fundamental & Regulatory Agent",
            run_fundamental_agent,
            docs
        )
    )

    # --------------------------------------------------------
    # SENTIMENT
    # --------------------------------------------------------

    sentiment_result, sentiment_error = (
        await safe_agent_call(
            "Sentiment & Context Agent",
            run_sentiment_agent,
            signals
        )
    )

    # --------------------------------------------------------
    # COLLECT
    # --------------------------------------------------------

    sub_agent_results = []

    failed_agents = []

    for result in [
        technical_result,
        fundamental_result,
        sentiment_result
    ]:

        if result is not None:
            sub_agent_results.append(result)

    for error in [
        technical_error,
        fundamental_error,
        sentiment_error
    ]:

        if error is not None:
            failed_agents.append(error)

    print(
        f"[ORCHESTRATOR] "
        f"{len(sub_agent_results)} specialist agents succeeded."
    )

    if failed_agents:

        print(
            f"[ORCHESTRATOR] "
            f"{len(failed_agents)} specialist agents failed."
        )

    # --------------------------------------------------------
    # TOTAL FAILURE
    # --------------------------------------------------------

    if not sub_agent_results:

        raise RuntimeError(
            "All specialist agents failed. "
            "Cannot produce a synthesis."
        )

    # --------------------------------------------------------
    # SYNTHESIS
    # --------------------------------------------------------

    print(
        "[ORCHESTRATOR] Starting synthesis..."
    )

    final_output = await synthesize_master_recommendation(
        symbol=symbol,
        sub_agent_results=sub_agent_results,
        failed_agents=failed_agents,
        user_profile=user_profile
    )

    print(
        "[ORCHESTRATOR] Synthesis complete."
    )

    return final_output