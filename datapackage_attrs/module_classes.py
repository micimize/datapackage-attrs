import typing as t
from textwrap import dedent

import attr
from tableschema import Field, Schema  # type: ignore

from ._types import TypeInfo, get_type_info


def _mapping_block(mapping: dict, join: str, value_join: str = ", ", prefix: str = ""):
    return "\n".join(
        join.join(
            [prefix + key, value_join.join(value) if isinstance(value, list) else value]
        )
        for key, value in mapping.items()
    )


@attr.s(auto_attribs=True)
class ModuleSnippet:
    """Snippet of a module to be generated

    Attributes
        imports: mapping of general module imports to optional aliases
        symbol_imports: mapping of necessary module imports to imported symbols
        definitions: mapping of variable names to definitions
    """

    imports: t.Dict[str, t.Optional[str]] = attr.ib(factory=dict)
    symbol_imports: t.Dict[str, t.Set[str]] = attr.ib(factory=dict)
    definitions: t.Dict[str, str] = attr.ib(factory=dict)
    body: t.List[str] = attr.ib(factory=list)

    def add_symbol_imports(self, module: str, *symbols: str):
        self.symbol_imports.setdefault(module, set())
        self.symbol_imports[module].update(symbols)

    @classmethod
    def merge(cls, *snippets: "ModuleSnippet") -> "ModuleSnippet":
        merged = ModuleSnippet()
        for snippet in snippets:
            merged.imports.update(snippet.imports)
            for mod, symbols in snippet.symbol_imports.items():
                merged.add_symbol_imports(mod, *symbols)
            merged.body.extend(snippet.body)
        return merged

    @property
    def _imports_text(self):
        return "\n\n".join(
            _mapping_block(self.imports, prefix="import ", join=" as "),
            _mapping_block(self.symbol_imports, prefix="from ", join=" import "),
        )

    @property
    def _definitions_repre(self):
        return _mapping_block(self.definitions, join=" = ")

    @property
    def _body_text(self):
        return "\n\n".join(self.body)

    @property
    def file_text(self):
        return "\n\n\n".join(
            self._imports_text, self._definitions_text, self._body_text
        )

    def overwrite(self, target: str):
        with open(target, "w") as file:
            file.write(self.file_text)


def _convert_schema(schema: t.Union[Schema, str, dict]):
    return Schema(schema.descriptor if isinstance(schema, Schema) else schema)


@attr.s(auto_attribs=True)
class SchemaClassDefinition:
    """
    Attributes:
        class_name: PascalCase python class name
        docstring: Docstring to generate the class with
        schema: source tableschema for this class
        snippet: The ModuleSnippet that defines this schema class
    """

    class_name: str
    docstring: str
    schema: Schema = attr.ib(converter=_convert_schema)

    snippet: ModuleSnippet = attr.ib(init=False)

    _field_definitions: t.List[str] = attr.ib(factory=list, init=False)

    def __attrs_post_init__(self):
        snippet = ModuleSnippet()
        for schema_field in schema.fields:
            type_info, type_def = get_type_info(schema_field)

            self._field_definitions.append(type_def)

            if type_info.source_module:
                snippet.add_symbol_imports(type_info.source_module, type_info.py_type)

            if type_info.definition:
                if type_info.definition == True:
                    snippet.imports["typing"] = "t"
                else:
                    snippet.definitions[type_info.py_type] = type_info.definition

        snippet.body = [
            dedent(
                f'''
            @attr.s(auto_attribs=True)
            class {self.class_name}:
                """{self.docstring}
                """
                {_BREAK_AND_INDENT.join(self._field_definitions)}
            '''
            )
        ]
        self.snippet = snippet

    @property
    def class_definition(self):
        return self.body[0]


_BREAK_AND_INDENT = "\n    "
