#    Copyright 2022-2023 Ohad Lev.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0,
#    or in the root directory of this package("LICENSE.txt").

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Setup file for sat-circuits-engine package."""

from setuptools import setup, find_packages

# Reading long description from the README.md file
with open("README.md", "r") as readme_file:
    readme = readme_file.read()

# Installation requirements
with open("requirements.txt", "r") as req_file:
    requirements = req_file.read().split()

print(requirements)

setup(
    name="sat-circuits-engine",
    version="3.0",
    description="A Python-Qiskit package for synthesizing quantum circuits to n-SAT problems",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ohadlev77/sat-circuits-engine",
    author="Ohad Lev",
    author_email="ohadlev77@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(exclude=["test*"]),
    install_requires=requirements,
    python_requires=">=3.9"
)