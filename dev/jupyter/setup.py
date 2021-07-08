import setuptools

setuptools.setup(
    name="reshpc",
    version="0.0.0",
    author="Kitware, Inc.",
    author_email="kitware@kitware.com",
    description="Utilities for running ATS at NERSC",
    url="https://github.com/Kitware/resonanthpc",
    packages=[
        "reshpc",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
