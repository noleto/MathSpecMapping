from setuptools import setup

setup(name='MathSpecMapping',
      version='0.1.0',
      description='dynamic mathematical specification visualization library',
      packages=['MathSpecMapping'],
      author="SeanMcOwen",
      zip_safe=False,
      install_requires=[
          "graphviz>=0.20.1",
          "ipython>=7.7.0"
      ])
