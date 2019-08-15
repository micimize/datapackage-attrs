import logging
import typing as t
from textwrap import dedent

import mypy.nodes as nodes
from mypy.options import Options
from mypy.parse import parse as mypy_parse
from mypy.plugin import (
    ClassDefContext,
    DynamicClassDefContext,
    FunctionContext,
    Plugin,
    SemanticAnalyzerPluginInterface,
)
from mypy.plugins import attrs as mypy_attrs

# from tableschema import Field, Schema


def parse_hack(class_def: str):
    return mypy_parse(dedent(class_def), "", "", None, Options()).defs[0]


class MyPlugin(Plugin):
    def get_dynamic_class_hook(
        self, fullname: str
    ) -> t.Optional[t.Callable[[DynamicClassDefContext], None]]:
        if fullname == "datapackage_attrs.generate.generate_attrs":
            return schema_info_hook
        return None


def schema_info_hook(ctx: DynamicClassDefContext) -> None:
    class_def = parse_hack(
        """
        @attr.s(auto_attribs=True)
        class Foo:
            "wooow"
            bar: int
            baz: str
        """
    )
    class_def.fullname = ctx.api.qualified_name(ctx.name)
    class_def.info = build_info(class_def, ctx)
    new_ctx = ClassDefContext(class_def, nodes.Expression(0, 0), ctx.api)
    return mypy_attrs.attr_class_maker_callback(new_ctx, True)


def build_info(class_def: nodes.ClassDef, ctx: DynamicClassDefContext):
    info = nodes.TypeInfo(nodes.SymbolTable(), class_def, ctx.api.cur_mod_id)
    for statement in class_def.defs.body:
        if isinstance(statement, nodes.AssignmentStmt):
            name_stmt = t.cast(nodes.NameExpr, statement.lvalues[0])
            name = name_stmt.name
            var = nodes.Var(name, statement.type)
            info.names[name] = nodes.SymbolTableNode(
                nodes.MDEF, var, plugin_generated=True
            )

    obj = ctx.api.builtin_type("builtins.object")
    info.mro = [info, obj.type]
    info.bases = [obj]
    return info


def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return MyPlugin
