import mypy.nodes as nodes
from mypy.mro import MroError, calculate_mro
from mypy.plugin import (
    ClassDefContext,
    DynamicClassDefContext,
    FunctionContext,
    Plugin,
    SemanticAnalyzerPluginInterface,
)
from tableschema import Field, Schema


class MyPlugin(Plugin):
    def get_dynamic_class_hook(
        self, fullname: str
    ) -> Optional[Callable[[DynamicClassDefContext], None]]:
        if fullname == "datapackage_attrs.generate.generate_attrs":
            return schema_info_hook
        return None


# You can either tediously construct the ClassDef Block with
# AssignmentStmt(NameExpr('bar'), TempNode(Any), type=UnboundType('int', [], int)), etc
# or reconstruct the class string.
# There's already an attrs plugin for mypy, so maybe you can just decorate the constructed class
# here and leverage that.
# Also, if you just generate class strings, you can generate code later easily
def schema_info_hook(ctx: DynamicClassDefContext) -> None:
    class_def = nodes.ClassDef(ctx.name, nodes.Block([]))
    class_def.fullname = ctx.api.qualified_name(ctx.name)

    info = nodes.TypeInfo(nodes.SymbolTable(), class_def, ctx.api.cur_mod_id)
    class_def.info = info
    class_def.base
    info.bases = [ctx.api.builtin_type("builtins.object")]

    ctx.api.add_symbol_table_node(ctx.name, nodes.SymbolTableNode(nodes.GDEF, info))


def add_var_to_class(name: str, typ: nodes.Type, info: nodes.TypeInfo) -> None:
    """Add a variable with given name and type to the symbol table of a class.
    This also takes care about setting necessary attributes on the variable node.
    """
    var = Var(name)
    var.info = info
    var._fullname = info.fullname() + "." + name
    var.type = typ
    info.names[name] = nodes.SymbolTableNode(nodes.MDEF, var)
