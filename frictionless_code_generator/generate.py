import typing as t

from .module_classes import ModuleSnippet, SchemaClassDefinition


def generate(
    tableschema_path: str,
    target_file: str,
    class_name: str,
    summary: str = None,
    description: str = None,
):
    SchemaClassDefinition(
        schema=tableschema_path,
        class_name=class_name,
        summary=summary,
        description=description,
    ).snippet.overwrite(target_file)
