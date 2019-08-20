import os

import toml

dirpath = os.getcwd()
pyproject = os.path.join(os.getcwd(), "pyproject.toml")

configuration = toml.load(pyproject)["tool"]["codegen"]
