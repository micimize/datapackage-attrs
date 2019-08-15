from textwrap import dedent

import mypy.nodes as nodes
from mypy.mro import MroError, calculate_mro
from mypy.parse import parse as mypy_parse
from mypy.plugin import (
    ClassDefContext,
    DynamicClassDefContext,
    FunctionContext,
    Plugin,
    SemanticAnalyzerPluginInterface,
)
from mypy.plugins import attrs as mymy_attrs
from tableschema import Field, Schema


def parse_hack(class_def: str) -> nodes.ClassDef:
    return mypy_parse(dedent(class_def), "", "", None, options.Options()).defs[0]


class MyPlugin(Plugin):
    def get_dynamic_class_hook(
        self, fullname: str
    ) -> Optional[Callable[[DynamicClassDefContext], None]]:
        if fullname == "datapackage_attrs.generate.generate_attrs":
            return schema_info_hook
        return None


def schema_info_hook(ctx: DynamicClassDefContext) -> None:
    print(ctx)
    class_def = parse_hack(
        """
        @attr.s(auto_attribs=True)
        class Foo:
            bar: int
            baz: str
        """
    )
    class_def.fullname = ctx.api.qualified_name(ctx.name)
    info = nodes.TypeInfo(nodes.SymbolTable(), class_def, ctx.api.cur_mod_id)
    class_def.info = build_info(class_def, ctx)
    return attrs.attr_class_maker_callback(class_def, ctx)


def build_info(cass_def: nodes.ClassDef, ctx: DynamicClassDefContext):
    info = nodes.TypeInfo(nodes.SymbolTable(), class_def, ctx.api.cur_mod_id)
    obj = ctx.api.builtin_type("builtins.object")
    info.mro = [info, obj.type]
    info.bases = [obj]
    return info
