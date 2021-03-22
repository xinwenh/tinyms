# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""learning rate generator"""
import math
import tinyms as ts


def mobilenetv2_lr(global_step, lr_init, lr_end, lr_max, warmup_epochs, total_epochs, steps_per_epoch):
    """
    Generate learning rate for mobilenetv2.

    Args:
       global_step(int): total steps of the training.
       lr_init(float): init learning rate.
       lr_end(float): end learning rate.
       lr_max(float): max learning rate.
       warmup_epochs(int): number of warmup epochs.
       total_epochs(int): total epoch of training.
       steps_per_epoch(int): steps of one epoch.

    Returns:
       Tensor, learning rate.
    """
    lr_each_step = []
    total_steps = steps_per_epoch * total_epochs
    warmup_steps = steps_per_epoch * warmup_epochs
    for i in range(total_steps):
        if i < warmup_steps:
            lr = lr_init + (lr_max - lr_init) * i / warmup_steps
        else:
            lr = lr_end + \
                (lr_max - lr_end) * \
                (1. + math.cos(math.pi * (i - warmup_steps) / (total_steps - warmup_steps))) / 2.
        if lr < 0.0:
            lr = 0.0
        lr_each_step.append(lr)

    current_step = global_step
    lr_each_step = ts.array(lr_each_step, dtype=ts.float32)
    learning_rate = lr_each_step[current_step:]

    return learning_rate


def cyclegan_lr(max_epoch, n_epoch, dataset_size):
    """
    Generate learning rate for cycle_gan.

    Args:
       max_epoch(int): epoch size for training.
       n_epoch(int): number of epochs with the initial learning rate.
       dataset_size(int): total size of dataset.

    Returns:
       Tensor, learning rate.
    """
    n_epochs_decay = max_epoch - n_epoch
    lrs = [0.0002] * dataset_size * n_epoch
    lr_epoch = 0
    for epoch in range(n_epochs_decay):
        lr_epoch = 0.0002 * (n_epochs_decay - epoch) / n_epochs_decay
        lrs += [lr_epoch] * dataset_size
    lrs += [lr_epoch] * dataset_size * (max_epoch - n_epochs_decay - n_epoch)
    return ts.array(lrs, dtype=ts.float32)

