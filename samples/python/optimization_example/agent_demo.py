import streamlit as st
import time
import random

# For the demo, we use a sequential approach with status updates to ensure Streamlit stability,
# as background threads require complex context management.
# In a real OpenVINO application, AsyncInferQueue would handle the parallelism.

class DemoAgent:
    def __init__(self, name, optimization, base_tps):
        self.name = name
        self.optimization = optimization
        self.base_tps = base_tps

    def run(self, placeholder, metric_placeholder):
        # Simulated performance characteristics based on OpenVINO hints
        tps_multiplier = 1.0
        ttft = 1.0

        if self.optimization == "THROUGHPUT":
            tps_multiplier = 1.6 # Simulated throughput gain
            ttft = 1.5
        elif self.optimization == "LATENCY":
            tps_multiplier = 1.1
            ttft = 0.4 # Simulated latency improvement

        time.sleep(ttft)

        tokens = []
        num_tokens = random.randint(30, 80)
        start_time = time.time()

        for i in range(num_tokens):
            tokens.append(f"token_{i} ")
            current_text = "".join(tokens)
            placeholder.code(current_text[-200:] + "...", language=None)

            elapsed = time.time() - start_time
            if elapsed > 0:
                actual_tps = (i + 1) / elapsed
                metric_placeholder.metric("Current TPS", f"{actual_tps:.2f}")

            # Control speed to match the "TPS"
            speed = self.base_tps * tps_multiplier * random.uniform(0.9, 1.1)
            time.sleep(1.0 / speed)

        return "".join(tokens)

st.set_page_config(page_title="OpenVINO Agent Optimizer", layout="wide")

st.title("🚀 OpenVINO™ AI Agent Performance Demo")
st.markdown("""
This demo visualizes how different **OpenVINO™ Runtime Optimizations** affect Agent performance.
In a real production environment, you would use `THROUGHPUT` for parallel tool execution and `LATENCY` for interactive responses.

*Note: This is a portable simulation of performance gains. Actual TPS depends on your hardware (Intel GPU/CPU) and model size.*
""")

with st.sidebar:
    st.header("Settings")
    device = st.selectbox("Target Device", ["CPU", "GPU", "AUTO"], index=0)
    base_speed = st.slider("Base TPS", 10, 100, 30)

st.divider()

col1, col2, col3 = st.columns(3)

# Setup containers
with col1:
    st.subheader("Agent 1")
    st.info("Optimization: **DEFAULT**")
    m1 = st.empty()
    t1 = st.empty()

with col2:
    st.subheader("Agent 2")
    st.success("Optimization: **THROUGHPUT**")
    m2 = st.empty()
    t2 = st.empty()

with col3:
    st.subheader("Agent 3")
    st.warning("Optimization: **LATENCY**")
    m3 = st.empty()
    t3 = st.empty()

if st.button("▶️ Start Agentic Workflow"):
    agent1 = DemoAgent("Agent 1", "DEFAULT", base_speed)
    agent2 = DemoAgent("Agent 2", "THROUGHPUT", base_speed)
    agent3 = DemoAgent("Agent 3", "LATENCY", base_speed)

    # We run them sequentially for the UI demo to avoid threading context issues in the sandbox,
    # but we present them as a workflow.

    with st.status("Agent 1 Thinking...", expanded=True):
        agent1.run(t1, m1)

    with st.status("Agent 2 (Parallel Task 1) - Optimized for Throughput...", expanded=True):
        agent2.run(t2, m2)

    with st.status("Agent 3 (Parallel Task 2) - Optimized for Latency...", expanded=True):
        agent3.run(t3, m3)

    st.success("Workflow Complete!")

st.divider()
st.markdown("### 💡 Implementation Snippet")
st.code(f"""
import openvino as ov
core = ov.Core()

# Use THROUGHPUT hint for Agent B/C parallel tasks
config = {{"PERFORMANCE_HINT": "THROUGHPUT"}}
compiled_model = core.compile_model("model.xml", "{device}", config)
""", language="python")
