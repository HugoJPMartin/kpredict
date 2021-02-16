from os import path
from setuptools import setup, find_packages

this_directory = path.dirname(__file__)
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="kpredict",
    packages=find_packages(exclude=("linux-stable",)),
    package_data={"": ["*.joblib", "*.json"],},
    python_requires='>=3.8',
    version="0.1.1",
    install_requires=["scikit-learn == 0.23.0", "numpy >= 1.16.2", "pandas", "joblib"],
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hugo Martin",
    author_email="hugo.martin@irisa.fr",
    url="https://github.com/HugoJPMartin/kpredict",
    keywords=[],
    classifiers=[],
    scripts=["bin/kpredict"],
)
