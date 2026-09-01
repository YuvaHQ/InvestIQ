# 📈 InvestIQ

### AI-Powered Multi-Agent Financial Intelligence Platform

InvestIQ is an AI-powered financial intelligence platform that combines **market analysis, technical analysis, fundamental analysis, sentiment, and investor risk profiles** to generate transparent, explainable, and risk-aware investment insights.

Instead of relying on a single AI response, InvestIQ uses a **multi-agent architecture** where specialized analysis components evaluate different aspects of an investment and an orchestration layer combines their outputs into a final recommendation.

The platform is designed to make complex financial analysis easier to understand while keeping the reasoning and supporting evidence visible to the user.

> **InvestIQ is an educational and research tool. It does not provide guaranteed investment returns or professional financial advice.**

---

## 🚀 What InvestIQ Does

InvestIQ takes a stock and investor profile as input and produces a structured investment assessment.

```text
                    USER
                      │
                      ▼
             ┌─────────────────┐
             │  InvestIQ UI    │
             │    Streamlit    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   Orchestrator  │
             └────────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Market Agent   Technical     Fundamental
                  Agent          Agent
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
                Sentiment Agent
                      │
                      ▼
              Investor Profile
                      │
                      ▼
             ┌─────────────────┐
             │  Gemini / LLM   │
             │    Synthesis    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Final Investment│
             │   Assessment    │
             └─────────────────┘
```

The current application is implemented as a Streamlit interface and calls `run_agent_pipeline` from the orchestration layer.

---

# ✨ Key Features

### 🤖 Multi-Agent Analysis

InvestIQ is designed around multiple specialized analysis agents rather than a single monolithic AI prompt.

Each agent contributes:

* Market stance
* Confidence score
* Rationale
* Evidence
* Key risks

The outputs are represented using structured Pydantic models.

---

### 📊 Market Analysis

The market-analysis layer evaluates market-related information and contributes to the overall investment view.

The goal is to determine whether the available market signals are:

```text
Bullish
Bearish
Neutral
```

---

### 📈 Technical Analysis

Technical signals can be incorporated into the agent pipeline to evaluate:

* Price movement
* Momentum
* Trend
* Market signals
* Short/medium-term behavior

Technical analysis should complement fundamental analysis rather than replace it.

---

### 🏢 Fundamental Analysis

Fundamental analysis evaluates the underlying company and its financial characteristics.

Potential factors include:

* Revenue
* Profitability
* Growth
* Valuation
* Financial health
* Business performance
* Financial risks

---

### 📰 Sentiment Analysis

Sentiment analysis evaluates available market/news information and determines whether sentiment is:

```text
Bullish
Bearish
Neutral
```

This provides another independent signal for the final synthesis.

---

### 👤 Investor Profile

InvestIQ does not treat every investor identically.

The application accepts investor characteristics such as:

```text
Risk tolerance
Investment horizon
Portfolio concentration
Sector allocation
```

The Streamlit application currently builds an investor profile containing risk tolerance, investment horizon, portfolio concentration, and sector allocation before sending it to the orchestrator.

This allows the final analysis to be **risk-aware rather than purely stock-centric**.

---

# 🧠 Multi-Agent Architecture

The central component of InvestIQ is the orchestration layer.

```text
                 ┌──────────────────┐
                 │  Stock / Signals │
                 └─────────┬────────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │   Orchestrator   │
                 └─────────┬────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
   ┌───────────┐     ┌───────────┐     ┌───────────┐
   │  Market   │     │ Technical │     │Fundamental│
   │   Agent   │     │   Agent   │     │   Agent   │
   └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Sentiment  │
                    │    Agent    │
                    └──────┬──────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │ Investor Profile │
                 └─────────┬────────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │ Gemini Synthesis │
                 └─────────┬────────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │ Final Assessment │
                 └──────────────────┘
```

The architecture is intentionally designed so that individual agents can fail without necessarily bringing down the entire analysis. The schema layer explicitly supports both successful `SubAgentOutput` results and `AgentError` records.

---

# 🎯 Recommendation System

InvestIQ supports five final recommendation categories:

```text
STRONG BUY
BUY
HOLD / CAUTION
SELL
STRONG SELL
```

These recommendations are represented as a typed `Recommendation` literal in the project's schema.

Agent-level analysis uses three stances:

```text
Bullish
Bearish
Neutral
```

Each agent also produces a confidence value between `0.0` and `1.0`.

---

# 🔍 Explainability

InvestIQ is designed to avoid producing a recommendation without an explanation.

Each sub-agent can return:

```text
Agent name
Stance
Confidence
Rationale
Evidence
Key risks
```

The final synthesis can additionally contain:

```text
Final recommendation
Synthesis summary
Risk adjustment
Dominant factors
Conflicts between agents
Sub-agent traces
Failed agents
```

This makes the system easier to inspect and debug than a traditional black-box LLM application.

---

# 📚 Evidence-Based Analysis

Evidence is represented as:

```python
Evidence(
    source="...",
    claim="..."
)
```

This allows the application to associate an analytical claim with its supporting source.

For example:

```json
{
  "source": "Annual Report 2025",
  "claim": "Revenue increased year-over-year."
}
```

This evidence-first design is intended to make the AI output more transparent and auditable.

---

# 🧩 Project Structure

The current repository is intentionally lightweight and centered around the core AI pipeline:

```text
InvestIQ/
│
├── app.py
├── agents.py
├── orchestrator.py
├── schemas.py
├── config.py
├── prompts.py
├── gemini_client.py
├── validators.py
├── exceptions.py
├── .gitignore
└── README.md
```

The current GitHub repository contains these core files on the `main` branch.

---

# 📁 Module Responsibilities

## `app.py`

The Streamlit application and user interface.

Responsibilities include:

* UI rendering
* User inputs
* Investor-profile configuration
* Stock-analysis request
* Pipeline execution
* Result visualization

The current app is configured as a wide Streamlit application and invokes the agent pipeline through `run_agent_pipeline`.

---

## `orchestrator.py`

The central coordination layer.

Responsibilities:

```text
Receive analysis request
        ↓
Prepare agent inputs
        ↓
Execute agents
        ↓
Collect agent outputs
        ↓
Handle agent failures
        ↓
Send results for synthesis
        ↓
Return final structured result
```

This is the most important integration point in the system.

---

## `agents.py`

Contains the agent layer.

Each specialized agent should focus on a single analytical responsibility.

Recommended conceptual agents:

```text
Market Agent
Technical Agent
Fundamental Agent
Sentiment Agent
Risk Agent
Synthesis Agent
```

The agents should return structured results instead of arbitrary text.

---

## `schemas.py`

Defines the shared data contracts between components.

Important models include:

```text
Evidence
SubAgentOutput
AgentError
FinalSynthesisOutput
```

It also defines the supported stance and recommendation types.

This file should be treated as the **contract between the agents and orchestrator**.

---

## `gemini_client.py`

The low-level Gemini API wrapper.

The project intentionally isolates Google Gemini SDK communication inside this module.

The client is responsible for:

* Gemini client initialization
* Structured-output requests
* Pydantic response parsing
* SDK exception translation
* Token/usage metadata
* API error handling

The repository explicitly documents this module as the only component that directly communicates with the `google-genai` SDK.

This separation is important because the rest of the application should not depend directly on the Gemini SDK.

---

## `prompts.py`

Contains the prompts used by the AI agents and synthesis layer.

Prompts should remain centralized so they can be:

* Versioned
* Tested
* Improved
* Audited
* Changed without modifying orchestration logic

---

## `config.py`

Central configuration layer.

This should contain:

```text
Model configuration
Gemini configuration
Demo configuration
Mock signals
Mock documents
Mock investor profile
Application settings
```

The Streamlit application currently imports configuration values such as `DEMO_MODE`, `MODEL_NAME`, `MOCK_SIGNALS`, `MOCK_DOCS`, and `MOCK_USER_PROFILE`.

---

## `validators.py`

Responsible for validating inputs before they reach the AI pipeline.

Examples:

```text
Stock symbol validation
Investor profile validation
Signal validation
Document validation
Configuration validation
```

Validation should happen before expensive AI calls whenever possible.

---

## `exceptions.py`

Centralized application-specific exceptions.

This allows low-level errors to be translated into meaningful application errors rather than exposing raw SDK exceptions to the UI.

---

# 🔄 End-to-End Workflow

A typical analysis request follows this flow:

```text
1. User selects stock
        ↓
2. User provides investor profile
        ↓
3. Input validation
        ↓
4. Market/technical/fundamental/sentiment signals collected
        ↓
5. Specialized agents analyze their respective signals
        ↓
6. Agent outputs are validated
        ↓
7. Agent results are aggregated
        ↓
8. Investor risk profile is applied
        ↓
9. Gemini generates structured synthesis
        ↓
10. Final recommendation is validated
        ↓
11. Results displayed in Streamlit
```

---

# 🧮 Agent Output

A typical sub-agent result follows this structure:

```json
{
  "agent_name": "Fundamental Agent",
  "stance": "Bullish",
  "confidence": 0.82,
  "rationale": "The company's fundamentals remain strong...",
  "evidence": [
    {
      "source": "Annual Report",
      "claim": "..."
    }
  ],
  "key_risks": [
    "High valuation"
  ]
}
```

This corresponds to the project's `SubAgentOutput` schema.

---

# 🏁 Final Output

The final synthesis should resemble:

```json
{
  "symbol": "AAPL",
  "user_risk_profile": "Moderate",
  "final_recommendation": "BUY",
  "synthesis_summary": "...",
  "risk_adjustment_note": "...",
  "dominant_factors": [
    "Strong fundamentals",
    "Positive market trend"
  ],
  "conflicts": [],
  "sub_agent_traces": [],
  "failed_agents": []
}
```

The actual final structure is defined by `FinalSynthesisOutput`.

---

# 🤖 Gemini Integration

InvestIQ uses Google's Gemini through the `google-genai` SDK.

The integration follows a structured-output approach rather than simply requesting free-form text.

Conceptually:

```text
Prompt
  +
Analysis Context
  +
Response Schema
       │
       ▼
     Gemini
       │
       ▼
Structured JSON
       │
       ▼
Pydantic Validation
       │
       ▼
Final Agent Result
```

The Gemini client configures JSON output and a Pydantic response schema before making the model request.

This reduces the risk of downstream components receiving unpredictable AI output.

---

# 🔐 Security

API keys must never be hard-coded into the repository.

Use environment variables:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit:

```text
.env
```

to Git.

Instead provide:

```text
.env.example
```

for developers.

---

# 🛠️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YuvaHQ/InvestIQ.git
cd InvestIQ
```

---

## 2. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install dependencies

Create or update the project's dependency file:

```bash
pip install -r requirements.txt
```

At minimum, the environment needs the libraries used by the current implementation, including Streamlit, Pydantic, and Google's `google-genai` SDK.

---

## 4. Configure Gemini

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_model_name
```

Do not expose the API key in frontend code.

---

# ▶️ Running InvestIQ

Launch the Streamlit application:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

The application should provide the InvestIQ financial-intelligence interface.

---

# 🧪 Demo Mode

The current application contains demo/mock configuration, including:

```text
MOCK_SIGNALS
MOCK_DOCS
MOCK_USER_PROFILE
DEMO_MODE
```

This allows the UI and pipeline to be demonstrated without requiring every external data source to be connected.

For production, these mock inputs should be replaced with real data providers.

---

# 🔌 Production Integration

The current repository provides the AI orchestration foundation.

For a production-ready system, the following external data layer should be connected:

```text
                 DATA SOURCES
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Market Data    Financials     News/Sentiment
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
              Normalized Signals
                      │
                      ▼
                 AI Agents
```

Recommended production inputs include:

### Market Data

```text
Current price
Historical OHLCV
Volume
Market indices
Volatility
```

### Fundamental Data

```text
Revenue
Earnings
Margins
Debt
Cash flow
EPS
ROE
Valuation ratios
```

### Sentiment Data

```text
Financial news
Company announcements
Earnings commentary
Market sentiment
```

### Investor Data

```text
Risk tolerance
Investment horizon
Portfolio allocation
Sector concentration
Investment objectives
```

---

# 🏗️ Recommended Production Architecture

The current single-file layout is useful for prototyping, but the next stage should separate the application into services.

Recommended target:

```text
InvestIQ/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── agents/
│   │   ├── market_agent.py
│   │   ├── technical_agent.py
│   │   ├── fundamental_agent.py
│   │   ├── sentiment_agent.py
│   │   ├── risk_agent.py
│   │   └── synthesis_agent.py
│   │
│   ├── services/
│   │   ├── market_service.py
│   │   ├── financial_service.py
│   │   ├── sentiment_service.py
│   │   └── profile_service.py
│   │
│   ├── orchestration/
│   │   └── orchestrator.py
│   │
│   ├── ai/
│   │   ├── gemini_client.py
│   │   └── prompts.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   └── config/
│       └── settings.py
│
├── frontend/
│   └── streamlit_app.py
│
├── tests/
│
├── .env.example
├── requirements.txt
└── README.md
```

The existing modules should be migrated into this structure gradually rather than rewritten unnecessarily.

---

# 🧪 Testing Strategy

The project should eventually contain tests at three levels.

## Unit Tests

Test individual components:

```text
Validators
Schemas
Agents
Prompt builders
Gemini client
Configuration
```

---

## Integration Tests

Test:

```text
Agent
   ↓
Orchestrator
   ↓
Synthesis
```

---

## End-to-End Tests

Test the complete flow:

```text
User Input
   ↓
Streamlit
   ↓
Orchestrator
   ↓
Agents
   ↓
Gemini
   ↓
Final Recommendation
```

Example:

```python
def test_full_analysis():

    result = run_agent_pipeline(
        symbol="AAPL",
        signals=signals,
        docs=documents,
        user_profile=user_profile,
    )

    assert result.final_recommendation in [
        "STRONG BUY",
        "BUY",
        "HOLD / CAUTION",
        "SELL",
        "STRONG SELL",
    ]
```

---

# 🛡️ Failure Handling

A financial AI system should not fail completely because one analytical agent encounters an error.

InvestIQ's schema design supports explicit failed-agent reporting:

```json
{
  "agent_name": "Sentiment Agent",
  "error_type": "DATA_ERROR",
  "message": "Sentiment data unavailable"
}
```

The final synthesis can then account for missing analysis rather than pretending the agent succeeded.

---

# 📊 Explainable Decision Pipeline

The intended decision process is:

```text
             RAW DATA
                 │
                 ▼
        ┌─────────────────┐
        │ Data Validation  │
        └────────┬────────┘
                 │
                 ▼
       ┌───────────────────┐
       │ Specialized Agents│
       └─────────┬─────────┘
                 │
       ┌─────────┼─────────┐
       │         │         │
       ▼         ▼         ▼
    Market   Technical  Fundamental
       │         │         │
       └─────────┼─────────┘
                 │
                 ▼
             Sentiment
                 │
                 ▼
        Investor Risk Profile
                 │
                 ▼
          Gemini Synthesis
                 │
                 ▼
       ┌────────────────────┐
       │ Final Recommendation│
       └────────────────────┘
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   Decision   Evidence    Risks
```

The goal is not simply:

> "Ask an AI whether I should buy this stock."

Instead:

> **Collect multiple signals → analyze them independently → account for investor risk → synthesize the evidence → explain the resulting recommendation.**

---

# 🗺️ Development Roadmap

## Phase 1 — Core Prototype

* [x] Streamlit interface
* [x] Agent pipeline
* [x] Orchestrator
* [x] Structured Pydantic schemas
* [x] Gemini integration
* [x] Investor profile
* [x] Recommendation categories
* [x] Error handling structure

---

## Phase 2 — Real Data

* [ ] Connect live market-data provider
* [ ] Connect fundamental-data provider
* [ ] Connect news/sentiment provider
* [ ] Normalize external data
* [ ] Remove dependency on mock signals
* [ ] Add timestamps to data
* [ ] Add data-source attribution

---

## Phase 3 — Advanced Intelligence

* [ ] Historical backtesting
* [ ] Technical indicator engine
* [ ] Portfolio-level analysis
* [ ] Correlation analysis
* [ ] Risk scoring
* [ ] Scenario analysis
* [ ] Bull/base/bear cases
* [ ] Confidence calibration

---

## Phase 4 — Production Architecture

* [ ] Separate frontend and backend
* [ ] REST API
* [ ] Persistent database
* [ ] User authentication
* [ ] Portfolio storage
* [ ] Analysis history
* [ ] Caching
* [ ] Logging
* [ ] Monitoring
* [ ] Rate limiting

---

# 🎯 Definition of Done

InvestIQ can be considered production-ready when:

* [ ] One application starts the complete system
* [ ] Real market data is connected
* [ ] Real financial data is connected
* [ ] Real sentiment data is connected
* [ ] All agents return validated structured outputs
* [ ] Agent failures are handled gracefully
* [ ] Investor profile affects the final analysis
* [ ] Gemini produces structured synthesis
* [ ] Every important claim has supporting evidence
* [ ] Recommendations are explainable
* [ ] Data timestamps are displayed
* [ ] Mock data is clearly separated from production data
* [ ] API keys are securely managed
* [ ] Unit tests pass
* [ ] Integration tests pass
* [ ] End-to-end tests pass

---

# ⚠️ Disclaimer

InvestIQ is an AI-powered financial research and educational platform.

Its outputs are generated from available data, models, assumptions, and user-provided information. They may contain errors, omissions, or outdated information.

**InvestIQ does not provide guaranteed investment returns and should not be treated as professional financial, investment, tax, or legal advice.**

Users should independently verify financial information and consult a qualified financial professional before making investment decisions.

---

# 🤝 Contributing

Contributions are welcome.

Suggested workflow:

```bash
git checkout -b feature/your-feature
```

Make your changes, add tests, and verify the complete analysis pipeline before opening a pull request.

Recommended contribution areas:

* New analytical agents
* Market-data integrations
* Financial-data integrations
* Sentiment models
* Risk models
* Explainability
* UI improvements
* Testing
* Performance
* Security

---

# 📄 License

Add the project's chosen license here before public release.

---

# 🔗 Repository

**InvestIQ — YuvaHQ**

[GitHub Repository](https://github.com/YuvaHQ/InvestIQ?utm_source=chatgpt.com)

---

## 💡 Vision

InvestIQ aims to turn financial analysis from a confusing collection of charts and metrics into an understandable decision-support workflow:

```text
DATA
 ↓
ANALYSIS
 ↓
MULTI-AGENT REASONING
 ↓
RISK ADJUSTMENT
 ↓
EVIDENCE
 ↓
EXPLANATION
 ↓
INVESTMENT INSIGHT
```

**InvestIQ — Analyze smarter. Understand risk. Invest with context.**
