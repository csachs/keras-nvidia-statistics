# keras-nvidia-statistics

## Description

(Neither affiliated with keras nor nvidia).

Little [callback](https://keras.io/callbacks/) for
[keras](https://keras.io/) which will add desired statistics to the
output of keras. Other callbacks like `TensorBoard` will pick them up
and produce plots accordingly.
Will work only with nvidia devices, obviously.

Please note, that, if everything runs optimally, the metrics are not
that useful (e.g. temperature will reach a steady-state and utilization
will be constantly high). However, the values might show if the current
ML setup is not utilizing the GPU properly, or serve as a remote (via
TensorBoard) way to watch device health.

Usage:

```python
from keras_nvidia_statistics import NvidiaDeviceStatistics

# ...

model.fit(X, Y, callbacks=[NvidiaDeviceStatistics()])
```

Yielding in TensorBoard:

![E.g. temperature and utilization are reported](https://csachs.github.io/keras-nvidia-statistics/demo.png)

## Dependencies

[`py3nvml`](https://github.com/fbcotter/py3nvml/), which is a fork of the [NVIDIA Management Library](https://pypi.python.org/pypi/nvidia-ml-py).

## License
BSD