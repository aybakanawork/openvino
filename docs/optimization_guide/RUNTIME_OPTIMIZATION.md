# OpenVINO™ Runtime Optimization Guide

This guide provides an overview of various techniques to optimize model inference performance using the OpenVINO™ toolkit.

## 1. Model Optimization with NNCF (Post-Training Quantization)

The Neural Network Compression Framework (NNCF) provides a suite of advanced algorithms for model compression, including quantization, pruning, and sparsity. Post-Training Quantization (PTQ) is often the easiest way to boost performance by converting models to INT8 precision.

```python
import nncf
import openvino as ov

# Load your model
core = ov.Core()
model = core.read_model("model.xml")

# Prepare calibration dataset
calibration_loader = ...
def transform_fn(data_item):
    return data_item[0].numpy()
calibration_dataset = nncf.Dataset(calibration_loader, transform_fn)

# Quantize the model
quantized_model = nncf.quantize(model, calibration_dataset)

# Save the INT8 model
ov.save_model(quantized_model, "quantized_model.xml")
```

## 2. High-Level Performance Hints

OpenVINO™ offers two dedicated high-level performance hints to configure an inference device without needing to know low-level details.

- **LATENCY**: Minimizes the time to process a single inference request. Ideal for real-time applications.
- **THROUGHPUT**: Maximizes the number of inference requests processed per unit of time. It often utilizes multiple streams and potentially increases batch size.

```python
core = ov.Core()
# Compile with THROUGHPUT hint
compiled_model = core.compile_model(model, "CPU", {"PERFORMANCE_HINT": "THROUGHPUT"})
```

## 3. Asynchronous Inference API

Asynchronous inference allows the application to keep the device busy while the host handles other tasks, such as data preprocessing or postprocessing. This is crucial for maximizing throughput.

The `AsyncInferQueue` is a helper class that manages a pool of inference requests and their execution.

```python
# Create an AsyncInferQueue
infer_queue = ov.AsyncInferQueue(compiled_model)

def callback(request, user_data):
    # Process results here
    print(f"Inference finished for {user_data}")

# Set the callback
infer_queue.set_callback(callback)

# Start asynchronous inference
for i, input_data in enumerate(data_list):
    infer_queue.start_async({0: input_data}, i)

# Wait for all requests to finish
infer_queue.wait_all()
```

## 4. Model Caching

Model caching helps to reduce the "first-inference latency" by storing the compiled model on disk. Subsequent loads of the same model will use the cached version, significantly speeding up the `compile_model` call.

```python
core = ov.Core()
# Enable model caching
core.set_property({"CACHE_DIR": "./model_cache"})

# The first call will compile and cache; subsequent calls will load from cache
compiled_model = core.compile_model(model, "GPU")
```

## 5. Input Preprocessing with OpenVINO™

Moving preprocessing steps (like resizing, color space conversion, or normalization) into the OpenVINO™ model graph allows them to be executed on the target device (CPU/GPU/NPU), potentially offloading the host CPU and reducing data transfer overhead.

```python
from openvino.preprocess import PrePostProcessor, ResizeAlgorithm

ppp = PrePostProcessor(model)

# 1. Declare input data information
ppp.input().tensor() \
    .set_layout(ov.Layout("NHWC")) \
    .set_element_type(ov.Type.u8)

# 2. Specify preprocessing steps
ppp.input().preprocess() \
    .convert_element_type(ov.Type.f32) \
    .resize(ResizeAlgorithm.RESIZE_LINEAR) \
    .mean([123.675, 116.28, 103.53]) \
    .scale([58.395, 57.12, 57.375])

# 3. Set the expected model input layout
ppp.input().model().set_layout(ov.Layout("NCHW"))

# 4. Build the optimized model
model = ppp.build()
```

## 6. The "get_tensor" Idiom

To avoid unnecessary memory copies, it is recommended to use the `get_tensor` method to get a pointer to the internal memory of an inference request and populate it directly.

```python
infer_request = compiled_model.create_infer_request()
input_tensor = infer_request.get_input_tensor()

# Populate input_tensor.data directly
input_tensor.data[:] = prepared_data
infer_request.infer()
```

## Summary Table

| Optimization | Target | Key Benefit |
| --- | --- | --- |
| **NNCF Quantization** | Model Precision | Faster execution, smaller model size |
| **Performance Hints** | Runtime Config | Simplified device-specific optimization |
| **Async API** | Pipeline | Improved device utilization and throughput |
| **Model Caching** | Initialization | Faster application startup |
| **PrePostProcessor** | Preprocessing | Reduced host CPU load and data transfer |
| **get_tensor** | Data Handling | Zero-copy data population |

## 7. GPU-Specific Optimizations

Intel GPUs (integrated and discrete) offer massive parallel processing power, making them ideal for high-throughput inference.

### LATENCY vs THROUGHPUT on GPU
- **LATENCY**: Often uses a single stream and avoids batching to minimize the time for a single response.
- **THROUGHPUT**: Automatically enables **Automatic Batching** and multiple streams to saturate the GPU's execution units.

```python
# Optimize for GPU throughput
compiled_model = core.compile_model(model, "GPU", {"PERFORMANCE_HINT": "THROUGHPUT"})
```

### Preprocessing on GPU
Using the `PrePostProcessor` to move resizing and color conversion to the GPU is highly recommended. This avoids the bottleneck of transferring large raw images to the GPU; instead, the GPU handles the conversion internally.

### Remote Tensors
For high-performance video pipelines (e.g., using VA-API or DirectX), use **Remote Tensors** to share memory between the decoder and the OpenVINO GPU plugin without copying data between the CPU and GPU.

## 8. Optimizing Generative AI (LLMs)

Generative AI models have unique performance characteristics, primarily being memory-bandwidth bound during the generation phase.

### Weight Compression
Reducing the weight precision to INT4 or INT8 is critical for LLMs to reduce memory bandwidth pressure and fit larger models into device memory. This is typically done during model export using `optimum-intel` or NNCF.

```bash
optimum-cli export openvino --model <MODEL_ID> --weight-format int4 <OUTPUT_DIR>
```

### KV Caching
Maintaining a Key-Value (KV) cache across generation steps is essential for efficiency. The `openvino_genai` library handles this automatically. For chat scenarios, use `start_chat()` and `finish_chat()` to maintain the context.

### Speculative Decoding
Speculative decoding uses a smaller "draft" model to predict multiple tokens at once, which are then verified by the main model in a single forward pass. This can significantly increase the tokens-per-second rate.

```python
import openvino_genai as ov_genai

draft_model = ov_genai.draft_model(draft_model_path, device)
pipe = ov_genai.LLMPipeline(main_model_path, device, draft_model=draft_model)
```

## 8. Optimization for AI Agents

AI Agents often involve complex workflows, including multiple model calls, tool use, and loop-based logic.

### Responsive Latency
For agentic loops, use the `LATENCY` performance hint for the "think" or "plan" phases to ensure the agent reacts quickly.

### Parallel Execution (Tool Use)
When an agent needs to process multiple information sources or tools in parallel, use the `THROUGHPUT` hint and `AsyncInferQueue`. This allows the agent to trigger multiple "perceptions" or "actions" simultaneously, reducing the overall time to reach a goal.

### Continuous Batching and Serving
For deploying agents at scale, consider using **OpenVINO™ Model Server (OVMS)**, which supports continuous batching for LLMs, maximizing throughput while maintaining reasonable latency for multiple concurrent agent sessions.

## 9. Integration with Agent Frameworks (LlamaIndex / LangChain)

OpenVINO™ integrates with popular agentic and RAG frameworks to simplify optimization.

### LlamaIndex Integration
When using `LlamaIndex`, you can pass OpenVINO™ performance hints directly through the `OpenVINOLLM` class.

```python
from llama_index.llms.openvino import OpenVINOLLM

llm = OpenVINOLLM(
    model_id_or_path="model_path",
    device_name="GPU",
    model_kwargs={"ov_config": {"PERFORMANCE_HINT": "LATENCY"}},
)
```

## 10. AI Agent Performance Patterns

Agents require a balance of low-latency reasoning and high-throughput tool execution.

### Reasoning Loop (Latency-Critical)
The main "Thinking" loop of an agent should use the `LATENCY` hint. This ensures the agent can quickly decide on the next action or tool to call.

### Multi-Tool Execution (Throughput-Critical)
When an agent triggers multiple tools (e.g., searching three different databases simultaneously), use the `Async API` with the `THROUGHPUT` hint. This allows OpenVINO to run multiple tool-related model inferences (like embedding lookups or small classifier models) in parallel across available hardware streams.

### Monitoring Performance
In agentic workflows, monitor **Tokens Per Second (TPS)** and **Time To First Token (TTFT)**. TTFT is crucial for agent responsiveness, while TPS determines the overall speed of the agent's complex multi-step reasoning.
