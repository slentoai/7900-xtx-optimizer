from setuptools import find_packages, setup


setup(
    name="rdna3-optimization-layer",
    version="0.1.0",
    description="RDNA3 atlas-backed optimization layer demo by Craig Hasselbring",
    author="Craig Hasselbring",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "rdna3-opt=rdna3_optimization_layer.cli:main",
        ]
    },
    python_requires=">=3.10",
)
