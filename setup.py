 from setuptools import setup, find_packages

setup(
    name="GeoConstructAndVerify",
    version="0.1.0",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    author="Petko0321",
    author_email="your.email@example.com",
    description="A Python library for constructing and verifying geometric constructions in Euclidean geometry",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Petko0321/GeoConstructAndVerify/tree/February",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)