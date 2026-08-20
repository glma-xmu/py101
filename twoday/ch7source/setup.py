# setup.py

from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension

extensions = [
    Extension(
        "c_fibonacci",          # Name of the resulting extension
        sources=["c_fibonacci.pyx"],  # Cython source file
    )
]

setup(
    name="fibonacci",
    ext_modules=cythonize(extensions),
)
