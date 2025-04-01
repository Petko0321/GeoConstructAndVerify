from setuptools import setup, find_packages
import os

# Read requirements
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Read README for long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Find any data files in the package
package_data = {}
for package in find_packages():
    package_dir = os.path.join(*package.split('.'))
    data_files = []
    # Look for non-Python files
    for root, dirs, files in os.walk(package_dir):
        for file in files:
            if not file.endswith('.py') and not file.endswith('.pyc'):
                data_files.append(os.path.join(root, file).replace(package_dir + os.sep, ''))
    if data_files:
        package_data[package] = data_files

setup(
    name="geocv",
    version="0.1.0",
    packages=find_packages(),
    package_data=package_data,
    include_package_data=True,
    install_requires=requirements,
    author="Petko0321",
    author_email="your.email@example.com",
    description="A Python library for constructing and verifying geometric constructions in Euclidean geometry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Petko0321/GeoConstructAndVerify/tree/February",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # Keep the examples directory as part of the package
    data_files=[('samples', [os.path.join('samples', f) for f in os.listdir('samples') if not f.endswith('.pyc')])],
)