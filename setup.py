from setuptools import setup, find_packages

__package_name__ = "safe"


def get_version_and_cmdclass(pkg_path):
    """Load version.py module without importing the whole package.

    Template code from miniver
    """
    import os
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("version", os.path.join(pkg_path, "_version.py"))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.get_cmdclass(pkg_path)


__version__, cmdclass = get_version_and_cmdclass(__package_name__)


# noinspection PyTypeChecker
setup(
    name=__package_name__,
    version=__version__,
    description="SAFE: Statistically-based Failure Evaluation",
    long_description="SAFE: Statistically-based Failure Evaluation",
    author="Kathleen M Bartz",
    author_email="kbartz2@jh.edu",
    url="https://github.com/katembartz/SAFE/",
    license="Apache License, 2.0",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
    packages=find_packages(),
    keywords="mri segmentation statistical-methodology",
    entry_points={
        "console_scripts": [
            "safe=safe.main:main"
        ]
    },

    install_requires=[
        "nibabel",
        "numpy",
        "scipy",
        "torch>=2.0",
        "tqdm",
    ],
    cmdclass=cmdclass,
)
