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
