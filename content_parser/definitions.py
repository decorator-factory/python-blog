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


@fn("mono")
def monospace():
    def from_inline(*args):
        for arg in args:
            if not et.IInl().match(arg):
                raise TypeError(f"mono: Expected :`Inl`, got {arg}:{arg.ty}")
        return e.InlineTag("tt", "", args)
    yield ((), et.IInl(), et.TInline(), from_inline)


@fn("e")
def entity():
    def from_str(s):
        if not et.TStr().match(s):
            raise TypeError(f"e: Expected :`str`, got {s}:{s.ty}")
        return e.InlineRaw(f"&{s.value};")
    yield ((et.TStr(),), None, et.TInline(), from_str)


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
                if not et.IRen().match(arg):
                    raise TypeError(f"(h {n.value}): Expected :`Inl`, got {arg}:{arg.ty}")
            return e.BlockTag(f"h{n.value}", "", args)
        return e.Function({FN_TYPE: from_inline})
    yield ((et.TInt(),), None, FN_TYPE, from_int)


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
        return e.BlockTag(
            "ul",
            "",
            tuple(e.BlockTag("li", "", (arg,)) for arg in args)
        )
    yield ((), et.IInl(), et.TBlock(), from_inline)


@fn("list-ordered")
def list_ordered():
    def from_inline(*args):
        for arg in args:
            if not et.IInl().match(arg):
                raise TypeError(f"list-ordered: Expected :`Inl`, got {arg}:{arg.ty}")
        return e.BlockTag(
            "ol",
            "",
            tuple(e.BlockTag("li", "", (arg,)) for arg in args)
        )
    yield ((), et.IInl(), et.TBlock(), from_inline)


@fn("p")
def paragraph():
    def from_inline(*args):
        for arg in args:
            if not et.IRen().match(arg):
                raise TypeError(f"p: Expected :`Ren`, got {arg}:{arg.ty}")
        return e.BlockTag("p", "", args)
    yield ((), et.IRen(), et.TBlock(), from_inline)


@fn("a")
def link():
    def from_str_inline(adr, text):
        if not et.TStr().match(adr):
            raise TypeError(f"a: Expected :`str`, got {adr}:{adr.ty}")
        if not et.IInl().match(text):
            raise TypeError(f"a: Expected :`Inl`, got {adr}:{adr.ty}")
        return e.InlineTag("a", f"href={json.dumps(adr.value)}", (text,))
    yield ((et.TStr(), et.IInl()), None, et.TInline(), from_str_inline)


@fn("horizontal-rule")
def horizontal_rule():
    def from_void():
        return e.BlockRaw("<hr/>")
    yield ((), None, et.TBlock(), from_void)


@fn("--")
def emdash():
    def from_void():
        return e.InlineRaw("&emdash;")
    yield ((), None, et.TInline(), from_void)


@fn("nl")
def newline():
    def from_void():
        return e.InlineRaw("\n")
    yield ((), None, et.TInline(), from_void)
