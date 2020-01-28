# -*- coding: utf-8 -*-
"""
documentation
"""

from setuptools import setup, find_packages


setup(
    name='keras_nvidia_statistics',
    version='0.0.1-3',
    description='Generate device statistics (such as utilization, temperature, …) via a keras callback',
    long_description='',
    author='Christian C. Sachs',
    author_email='sachs.christian@gmail.com',
    url='',
    packages=find_packages(),
    requires=['numpy', 'py3nvml'],
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
    ]
)
