# coding:utf8
from setuptools import setup, find_packages

setup(
    name='s-ssh',
    version='v0.0.1',
    install_requires=[  # 依赖列表
        'fire>=0.1.3',
        'libtmux>=0.8.0',
        'sshconf>=0.0.0',
    ],
    packages=find_packages(),
    entry_points={'console_scripts': 's-ssh=s_ssh.main:main'}
)
