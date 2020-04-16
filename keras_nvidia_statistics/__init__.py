try:
    import py3nvml.py3nvml as nvml
except ImportError:
    nvml = None

import numpy as np
import os

try:
    if 'USE_TENSORFLOW_KERAS' in os.environ and os.environ['USE_TENSORFLOW_KERAS'] == '1':
        from tensorflow.keras.callbacks import Callback
    else:
        from keras.callbacks import Callback
except ImportError:
    class Callback:
        def __init__(self):
            raise RuntimeError(self.__class__.__name__ + ' needs either tensorflow or keras installed. '
                                                         '(Choose via USE_TENSORFLOW_KERAS=1/0 environment variable)')


def _bytes_to_megabytes(b_):
    return b_ / 1024.0 / 1024.0


class NvidiaDeviceStatistics(Callback):
    reportable_values = dict(
        memory_total=lambda handle: _bytes_to_megabytes(nvml.nvmlDeviceGetMemoryInfo(handle).total),
        memory_used=lambda handle: _bytes_to_megabytes(nvml.nvmlDeviceGetMemoryInfo(handle).used),
        memory_free=lambda handle: _bytes_to_megabytes(
            nvml.nvmlDeviceGetMemoryInfo(handle).total - nvml.nvmlDeviceGetMemoryInfo(handle).used
        ),
        temperature=lambda handle: nvml.nvmlDeviceGetTemperature(handle, nvml.NVML_TEMPERATURE_GPU),
        power_state=lambda handle: nvml.nvmlDeviceGetPowerState(handle),
        power_draw=lambda handle: nvml.nvmlDeviceGetPowerUsage(handle) / 1000.0,
        utilization_gpu=lambda handle: nvml.nvmlDeviceGetUtilizationRates(handle).gpu,
        utilization_memory=lambda handle: nvml.nvmlDeviceGetUtilizationRates(handle).memory,
    )

    def __init__(self, report=None, devices=None, quiet=False, always_suffix=False, output=print, verbose_once=True):
        super(self.__class__, self).__init__()

        self.output = output

        if nvml is None:
            if not quiet:
                self.output("Could not load py3nvml, cannot report any nvidia device statistics.")
            report = []
        else:
            nvml.nvmlInit()

            device_count = nvml.nvmlDeviceGetCount()

            if devices is None:
                devices = list(range(device_count))
            else:
                devices = [int(device) for device in devices if 0 <= int(device) < device_count]

            self.devices = devices
            self.deviceHandles = [nvml.nvmlDeviceGetHandleByIndex(device) for device in devices]

            if not quiet:
                for n, handle in enumerate(self.deviceHandles):
                    self.output("Collecting statistics for device #% 2d: %s" % (n, nvml.nvmlDeviceGetName(handle)))

        if report is None:
            report = ['temperature', 'utilization_gpu']
        elif report == 'all':
            report = list(self.reportable_values.keys())

        self.verbose_once = verbose_once
        self.report = report
        self.always_suffix = always_suffix

    def __del__(self):
        if nvml:
            nvml.nvmlShutdown()

    def on_epoch_end(self, epoch, logs=None):
        for item in self.report:
            try:
                suffix = handle = None
                for n, handle in enumerate(self.deviceHandles):
                    if len(self.deviceHandles) == 1 and not self.always_suffix:
                        suffix = ''
                    else:
                        suffix = '_%02d' % (n,)  # TODO: this will not work nicely if more than 100 GPUs are in one sys

                    logs[item + suffix] = np.float32(self.reportable_values[item](handle))
            except nvml.NVMLError as err:
                self.output("Error trying to read out value from NVML: %r" % (err,))
        if self.verbose_once:
            self.output("Current status for device #% 2d (%s): %r" % (n, nvml.nvmlDeviceGetName(handle), {
                what: float(call(handle)) for what, call in self.reportable_values.items()
            }))
            self.verbose_once = False  # only print once