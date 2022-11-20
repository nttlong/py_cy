import pathlib

from setuptools import setup
from Cython.Build import cythonize
import os
build_dir = pathlib.Path(__file__).parent.__str__()

file_path=os.path.join(build_dir, f"cy_web_x.py")


setup(
    name='cy_web',
    ext_modules=cythonize(file_path),
    zip_safe=True,
    packages=["cy_web"],
    install_requires=[
        "fastapi"
    ]

)
#python cy_web/setup.py build_ext --inplace
#python cy_web/setup.py bdist_wheel --universal