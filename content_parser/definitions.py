from typing import Dict
import content_parser.entity_types as et
import content_parser.entities as e


BUILTINS: Dict[str, e.Entity] = {}


def fn(name: str):
    def _add_fn_to_builtins(f):
        overloads = {
            et.TFunction(arg_types, rest_types, return_type): fn
            for arg_types, rest_types, return_type, fn in f()
        }
        BUILTINS[name] = e.Function(overloads)
        return f
    return _add_fn_to_builtins



@fn("bf")
def boldface():
    def from_inline(*args):
        for arg in args:
            if not et.IInl().match(arg):
                raise TypeError(f"bf: Expected :`Inl`, got {arg}:{arg.ty}")
        return e.InlineTag("b", "", args)
    yield ((), et.IInl(), et.TInline(), from_inline)


@fn("$")
def concat():
    def from_inline(*args):
        for arg in args:
            if not et.IInl().match(arg):
                raise TypeError(f"bf: Expected :`Inl`, got {arg}:{arg.ty}")
        return e.InlineConcat(args)
    yield ((), et.IInl(), et.TInline(), from_inline)

    def from_mixed(*args):
        for arg in args:
            if not et.IRen().match(arg):
                raise TypeError(f"bf: Expected :`Ren`, got {arg}:{arg.ty}")
        return e.BlockConcat(args)
    yield ((), et.IRen(), et.IRen(), from_mixed)