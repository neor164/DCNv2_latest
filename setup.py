#!/usr/bin/env python

import glob
import os

import torch
from setuptools import setup
from torch.utils.cpp_extension import CUDA_HOME, CppExtension, CUDAExtension, BuildExtension

def get_extensions():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    src_relative = "src"
    src_full = os.path.join(this_dir, src_relative)

    main_file = glob.glob(os.path.join(src_relative, "*.cpp"))
    source_cpu = glob.glob(os.path.join(src_relative, "cpu", "*.cpp"))
    source_cuda = glob.glob(os.path.join(src_relative, "cuda", "*.cu"))
    os.environ["CC"] = "g++"
    sources = main_file + source_cpu
    extension = CppExtension
    extra_compile_args = {"cxx": []}
    define_macros = []

    if torch.cuda.is_available() and CUDA_HOME is not None:
        extension = CUDAExtension
        sources += source_cuda
        define_macros += [("WITH_CUDA", None)]
        extra_compile_args["nvcc"] = [
            "-DCUDA_HAS_FP16=1",
            "-D__CUDA_NO_HALF_OPERATORS__",
            "-D__CUDA_NO_HALF_CONVERSIONS__",
            "-D__CUDA_NO_HALF2_OPERATORS__",
        ]

    sources = [os.path.relpath(s, this_dir) for s in sources]
    include_dirs = [src_full]
    print("sources", sources)
    print("include_dirs", include_dirs)
    print("define_macros", define_macros)
    print("extra_compile_args", extra_compile_args)
    return [
        extension(
            "dcnv2._ext",
            sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
        )
    ]

setup(
    name='dcnv2',
    version='0.1.3',
    packages=['dcnv2'],
    ext_modules=get_extensions(),
    cmdclass={"build_ext": BuildExtension},
)
