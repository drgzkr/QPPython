from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='QPPython',
    version='0.0.1',
    packages=['QPPython'],
    url='https://github.com/drgzkr/QPPython',
    license='MIT',
    author='Dora Gozukara, Nasir Ahmad',
    description='Python implementation of the core functionality of QPPLab: A generally applicable software package for detecting, analyzing, and visualizing large-scale quasiperiodic spatiotemporal patterns (QPPs) of brain activity',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
