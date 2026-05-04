#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import logging as log
import sys
import os
import shutil
from time import perf_counter

import numpy as np
import openvino as ov
from openvino import op, opset8


def create_dummy_model():
    """Create a simple model: input -> Relu -> output."""
    input_shape = [1, 3, 224, 224]
    param_node = op.Parameter(ov.Type.f32, ov.Shape(input_shape))
    relu_node = opset8.relu(param_node)
    model = ov.Model(relu_node, [param_node], 'dummy_model')
    return model


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s', level=log.INFO, stream=sys.stdout)

    device_name = 'CPU'
    if len(sys.argv) > 1:
        device_name = sys.argv[1]

    cache_dir = "model_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    os.makedirs(cache_dir)

    # --------------------------- Step 1. Initialize OpenVINO Runtime Core --------------------------------------------
    log.info('Creating OpenVINO Runtime Core')
    core = ov.Core()

    # --------------------------- Step 2. Enable Model Caching --------------------------------------------------------
    log.info(f'Enabling model caching in: {cache_dir}')
    core.set_property({'CACHE_DIR': cache_dir})

    # --------------------------- Step 3. Create/Read a model ---------------------------------------------------------
    log.info('Creating a dummy model')
    model = create_dummy_model()

    # --------------------------- Step 4. Apply preprocessing with PrePostProcessor -----------------------------------
    log.info('Applying preprocessing steps')
    ppp = ov.preprocess.PrePostProcessor(model)

    # 1) Set input tensor information:
    # - input() provides information about a single model input
    # - layout of data is 'NHWC'
    # - precision of tensor is 'u8'
    # - set_shape() is required if the input tensor has a different shape than the model
    ppp.input().tensor() \
        .set_shape([1, 400, 400, 3]) \
        .set_layout(ov.Layout('NHWC')) \
        .set_element_type(ov.Type.u8)

    # 2) Adding explicit preprocessing steps:
    # - convert u8 to f32
    # - apply linear resize
    ppp.input().preprocess() \
        .convert_element_type(ov.Type.f32) \
        .resize(ov.preprocess.ResizeAlgorithm.RESIZE_LINEAR)

    # 3) Set model input layout to 'NCHW'
    ppp.input().model().set_layout(ov.Layout('NCHW'))

    # 4) Apply preprocessing to the model
    model = ppp.build()

    # --------------------------- Step 5. Loading model with THROUGHPUT hint ------------------------------------------
    log.info(f'Loading the model to the {device_name} device with THROUGHPUT hint')
    config = {'PERFORMANCE_HINT': 'THROUGHPUT'}
    compiled_model = core.compile_model(model, device_name, config)

    # --------------------------- Step 6. Create AsyncInferQueue ------------------------------------------------------
    log.info('Creating AsyncInferQueue')
    # AsyncInferQueue automatically creates optimal number of InferRequest instances
    infer_queue = ov.AsyncInferQueue(compiled_model)

    def completion_callback(request, user_data):
        log.info(f"Inference finished for request {user_data}")

    infer_queue.set_callback(completion_callback)

    # --------------------------- Step 7. Prepare input and perform inference -----------------------------------------
    # Input tensor for PrePostProcessor (NHWC, u8)
    # The size can be different from model input as we added resize step
    input_data = np.random.randint(0, 255, (1, 400, 400, 3), dtype=np.uint8)

    log.info('Starting 10 asynchronous inference requests')
    start_time = perf_counter()
    for i in range(10):
        # start_async uses an idle request from the queue
        infer_queue.start_async({0: input_data}, i)

    # Wait for all requests to finish
    infer_queue.wait_all()
    end_time = perf_counter()

    log.info(f'Finished 10 requests in {(end_time - start_time) * 1000:.2f} ms')
    log.info('Optimization example completed successfully')

    # Cleanup cache
    shutil.rmtree(cache_dir)

    return 0


if __name__ == '__main__':
    sys.exit(main())
