# 10 AI Agent Projects to Test with OpenVINO

This list highlights projects that leverage AI agents and can be integrated with OpenVINO for local, high-performance inference. All listed projects are recommended to be configured with **streaming enabled** and use **free tools** like DuckDuckGo for web searching.

## 1. OpenVINO Deep Research Agent
A specialized agent loop (see `samples/python/ai_agent_samples/deep_research_agent.py`) that performs multi-step information gathering and synthesis.
- **Key Feature:** Autonomous query generation and report synthesis.
- **Tools:** DuckDuckGo Search.

## 2. Local Coding Assistant
An agent that interacts with your local filesystem to explain code, suggest refactors, or write tests.
- **OpenVINO Integration:** Use `LLMPipeline` for low-latency code completion.
- **Streaming:** Essential for real-time code generation.

## 3. Web-Augmented Customer Support Bot
A chatbot that searches a local knowledge base or the live web to answer product questions.
- **Tools:** DuckDuckGo (for live info), local vector DB.

## 4. Personal News Aggregator
An agent that searches for the latest news on specific topics and provides a summarized daily brief.
- **Tools:** DuckDuckGo Search API.

## 5. Market Research Analyst
Gathers pricing and feature information for competitors in a specific niche.
- **Streaming:** Used to show the agent's "chain of thought" as it analyzes data.

## 6. Local Travel Planner
An agent that finds flights (via search), suggests itineraries, and provides weather updates.
- **Tools:** DuckDuckGo for general search.

## 7. Educational Tutor
An agent that explains complex topics by searching for the best pedagogical resources online.
- **Focus:** Interactive Q&A with streaming responses.

## 8. Technical Documentation Helper
Helps developers find specific API details by searching through online documentation.
- **OpenVINO Advantage:** Fast inference for parsing large blocks of documentation text.

## 9. Privacy-Preserving Personal Assistant
A general-purpose assistant that runs entirely locally on OpenVINO, ensuring your search queries (via DuckDuckGo) are the only data leaving your machine.

## 10. Automated Bug Triager
An agent that searches online forums (StackOverflow, GitHub Issues) to find solutions to local error messages.
- **Deep Research Component:** Investigates multiple potential fixes before recommending one.

---

## 10 Background Agents with Human-in-the-Loop (HITL)

These projects feature agents that work silently in the background and only surface information for human approval or intervention.

1.  **Smart Email Draftsman**
    - **Role:** Monitors inbox and prepares reply drafts.
    - **HITL:** User reviews and clicks "Send".
    - **Suggested Model:** `Llama-3.1-8B-Instruct` (High nuance).
2.  **Autonomous Meeting Summarizer**
    - **Role:** Listens to system audio and generates draft action items.
    - **HITL:** User edits and approves the final summary.
    - **Suggested Model:** `Phi-3.5-mini-instruct` (4B - Great logic/size balance).
3.  **Proactive Security Auditor**
    - **Role:** Watches file saves and flags potential security leaks (keys, CVEs).
    - **HITL:** Developer dismisses or fixes the warning.
    - **Suggested Model:** `Qwen2.5-Coder-7B-Instruct`.
4.  **Content Fact-Checker**
    - **Role:** Scans your active document and searches for verifying sources in the background.
    - **HITL:** Highlights text with "Source Found" or "Check Fact" tooltips.
    - **Suggested Model:** `Mistral-7B-v0.3`.
5.  **Technical Support Triage**
    - **Role:** Categorizes tickets and prepares "Suggested Resolution" cards.
    - **HITL:** Support agent verifies the solution before sending.
    - **Suggested Model:** `Llama-3.2-3B-Instruct`.
6.  **Real-time Documentation Sync**
    - **Role:** Detects structural changes in code and drafts documentation updates.
    - **HITL:** Developer reviews the diff and commits.
    - **Suggested Model:** `Phi-3.5-mini-instruct` (4B).
7.  **Smart Calendar Assistant**
    - **Role:** Parses chat messages for scheduling intent and finds free slots.
    - **HITL:** User selects one of the three proposed slots.
    - **Suggested Model:** `Qwen2.5-1.5B-Instruct` (Small and fast).
8.  **Automated PR Reviewer**
    - **Role:** Analyzes pull requests for style and logic errors.
    - **HITL:** Lead maintainer chooses which comments to keep.
    - **Suggested Model:** `Llama-3.1-8B-Instruct`.
9.  **Research Lab Monitor**
    - **Role:** Watches arXiv/RSS feeds for specific keywords and drafts summaries.
    - **HITL:** Researcher saves relevant abstracts to their library.
    - **Suggested Model:** `Gemma-2-9B`.
10. **Financial Alert Monitor**
    - **Role:** Monitors live market data and drafts "Anomalous Activity" reports.
    - **HITL:** Analyst verifies the alert and pushes to the client dashboard.
    - **Suggested Model:** `Phi-3-medium-instruct` (14B for high reliability, or 4B for speed).

---

## Recommended Models for Testing

Select one of the following model tiers to run the samples or your own projects. All models are optimized for OpenVINO.

| Tier | Model Name | Param Count | Best For |
| :--- | :--- | :--- | :--- |
| **Small** | `Qwen2.5-1.5B-Instruct` | 1.5B | High-speed response, limited memory (e.g., NPU/IGPU) |
| **Medium** | `Phi-3.5-mini-instruct` | 3.8B | Balanced logic and performance; excellent for background tasks |
| **Large** | `Llama-3.1-8B-Instruct` | 8B | Complex reasoning, high-quality research, and nuance |

### Implementation Tips for OpenVINO Agents
- **Enable Streaming:** Use the `streamer` callback in `pipe.generate()` for a responsive experience.
- **Model Choice:** Use INT4 quantized models for the best balance of speed and intelligence on consumer hardware.
- **Free Tools:** Use the `duckduckgo-search` Python library for easy, registration-free web access.
