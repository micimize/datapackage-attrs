import typing as t

from .module_classes import ModuleSnippet, SchemaClassDefinition


def generate(schema_path: str, class_name: str, docstring: str, target: str):
    SchemaClassDefinition(
        class_name=class_name, docstring=docstring, schema=schema_path
    ).snippet.overwrite(target)
