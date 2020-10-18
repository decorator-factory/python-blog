import json
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


@fn("it")
def italics():
    def from_inline(*args):
        for arg in args:
            if not et.IInl().match(arg):
                raise TypeError(f"it: Expected :`Inl`, got {arg}:{arg.ty}")
        return e.InlineTag("i", "", args)
    yield ((), et.IInl(), et.TInline(), from_inline)


@fn("$")
def concat():
    def from_inline(*args):
        for arg in args:
            if not et.IInl().match(arg):
                raise TypeError(f"$: Expected :`Inl`, got {arg}:{arg.ty}")
        return e.InlineConcat(args)
    yield ((), et.IInl(), et.TInline(), from_inline)

    def from_mixed(*args):
        for arg in args:
            if not et.IRen().match(arg):
                raise TypeError(f"$: Expected :`Ren`, got {arg}:{arg.ty}")
        return e.BlockConcat(args)
    yield ((), et.IRen(), et.IRen(), from_mixed)


@fn("h")
def heading():
    FN_TYPE = et.TFunction((), et.IInl(), et.TInline())

    def from_int(n: e.Integer):
        def from_inline(*args):
            for arg in args:
                if not et.IInl().match(arg):
                    raise TypeError(f"(h {n.value}): Expected :`Inl`, got {arg}:{arg.ty}")
            return e.InlineTag(f"h{n.value}", "", args)
        return e.Function({FN_TYPE: from_inline})
    yield ((), et.TInt(), FN_TYPE, from_int)


@fn("style")
def style_inline():
    FN_TYPE = et.TFunction((), et.IInl(), et.TInline())

    def from_str(s: e.String):
        def from_inline(*args):
            for arg in args:
                if not et.IInl().match(arg):
                    raise TypeError(f'(style "..."): Expected :`Inl`, got {arg}:{arg.ty}')
            return e.InlineTag("span", "style=" + json.dumps(s.value), args)
        return e.Function({FN_TYPE: from_inline})
    yield ((), et.TStr(), FN_TYPE, from_str)


@fn("list-unordered")
def list_unordered():
    def from_inline(*args):
        for arg in args:
            if not et.IInl().match(arg):
                raise TypeError(f"list-unordered: Expected :`Inl`, got {arg}:{arg.ty}")
        return e.InlineTag(
            "ul",
            "",
            tuple(e.InlineTag("li", "", (arg,)) for arg in args)
        )
    yield ((), et.IInl(), et.TInline(), from_inline)


@fn("list-ordered")
def list_ordered():
    def from_inline(*args):
        for arg in args:
            if not et.IInl().match(arg):
                raise TypeError(f"list-ordered: Expected :`Inl`, got {arg}:{arg.ty}")
        return e.InlineTag(
            "ol",
            "",
            tuple(e.InlineTag("li", "", (arg,)) for arg in args)
        )
    yield ((), et.IInl(), et.TInline(), from_inline)


@fn("p")
def paragraph():
    def from_inline(*args):
        for arg in args:
            if not et.IRen().match(arg):
                raise TypeError(f"p: Expected :`Ren`, got {arg}:{arg.ty}")
        return e.BlockTag("p", "", args)
    yield ((), et.IRen(), et.TBlock(), from_inline)
