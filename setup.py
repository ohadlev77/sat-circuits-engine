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

import os
import sys
from setuptools import setup, find_packages

# Read long description from the README.md file
# README_PATH = os.path.abspath(__file__)
# print()
# print(README_PATH)
# print()
# README = None

# print()
# print(f"__file__ = {__file__}")
# print(f"os.path.abspath(__file__) = {os.path.abspath(__file__)}")
# print(f"os.path.basename(__file__) = {os.path.basename(__file__)}")
# print(f"os.path.dirname(__file__) = {os.path.dirname(__file__)}")
# print(f"os.path.realpath(__file__) = {os.path.realpath(__file__)}")
# print(f"os.path.relpath(__file__) = {os.path.relpath(__file__)}")
# print()

# print(sys.path)
# print()
# print(sys.meta_path)

setup(
    name="sat_circuits_engine",
    version="2.0",
    description="A Python-Qiskit package for creating qunatum circuits to satisfiability problems",
    # long_description=README,
    # long_description_content_type="text/markdown",
    url="https://github.com/ohadlev77/SAT_Circuits_Engine",
    author="Ohad Lev",
    author_email="ohadlev77@gmail.com",
    packages=find_packages(),
    include_package_data=True
)

# print()
# print(find_packages())
# print()