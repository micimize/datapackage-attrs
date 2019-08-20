from .configuration import configuration
from .generate import generate

for schema in configuration.get("tableschemas", []):
    generate(**schema)
