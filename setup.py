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