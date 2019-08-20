import re
import typing as t
from textwrap import TextWrapper, dedent, indent

import attr
from tableschema import Field, Schema  # type: ignore

from ._types import TypeInfo, get_type_info

_NL = "\n\s*"

wrapper = TextWrapper(width=70, break_long_words=False, replace_whitespace=False)


def _clean_newlines(snippet: str, max_empty_lines=3):
    return re.sub(f"{_NL}{_NL}{_NL}{_NL}", "\n\n\n", snippet)


def _mapping_block(mapping: dict, join: str, value_join: str = ", ", prefix: str = ""):
    return "\n".join(
        [
            join.join(
                [
                    prefix + key,
                    value_join.join(value) if not isinstance(value, str) else value,
                ]
            )
            for key, value in mapping.items()
        ]
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
            [
                _mapping_block(self.imports, prefix="import ", join=" as "),
                _mapping_block(self.symbol_imports, prefix="from ", join=" import "),
            ]
        )

    @property
    def _definitions_text(self):
        return _mapping_block(self.definitions, join=" = ")

    @property
    def _body_text(self):
        return "\n\n".join(self.body)

    @property
    def file_text(self):
        return _clean_newlines(
            "\n\n\n".join([self._imports_text, self._definitions_text, self._body_text])
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
        summary: Summary doc to generate the class with
        description: Description doc to generate the class with
        schema: source tableschema for this class
        snippet: The ModuleSnippet that defines this schema class
    """

    class_name: str
    summary: str
    description: t.Optional[str]
    schema: Schema = attr.ib(converter=_convert_schema)

    snippet: ModuleSnippet = attr.ib(init=False)

    _field_definitions: t.List[str] = attr.ib(factory=list, init=False)

    def __attrs_post_init__(self):
        snippet = ModuleSnippet(imports={"attr": "attr", "typing": "t"})
        for schema_field in self.schema.fields:
            type_info, type_def = get_type_info(schema_field)

            self._field_definitions.append(type_def)
            if type_info.source_module:
                snippet.add_symbol_imports(type_info.source_module, type_info.py_type)

            if type_info.definition and type_info.definition != True:
                snippet.definitions[type_info.py_type] = type_info.definition

        snippet.body = [
            lines(
                "@attr.s(auto_attribs=True, slots=True)",
                f"class {self.class_name}:",
                indent(
                    lines(
                        f'"""{self._docstring}',
                        f'"""',
                        "",
                        lines(*self._field_definitions),
                    ),
                    prefix="    ",
                ),
                "",
            )
        ]
        self.snippet = snippet

    @property
    def _field_docs(self):
        return [
            lines(
                *wrapper.wrap(
                    schema_field.name
                    + ": "
                    + (schema_field.descriptor.get("description", ""))
                ),
                prefix="\n    ",
            )
            for schema_field in self.schema.fields
        ]

    @property
    def _docstring(self):
        return "".join(
            [
                self.summary,
                "\n\n" + self.description if self.description else "",
                "\n\nAttributes:\n",
                indent(lines(*self._field_docs), prefix="    "),
            ]
        )

    @property
    def class_definition(self):
        return self.body[0]


def _first_option(d: dict, options: t.Iterable):
    for key in options:
        value = d.get(options, None)
        if value is not None:
            return value


def lines(*text, prefix="\n"):
    return prefix.join(
        [
            lines(*line.split("\n"), prefix=prefix) if "\n" in line else line
            for line in text
        ]
    )


_BREAK_AND_INDENT = "\n   1   2   3   4   5"
