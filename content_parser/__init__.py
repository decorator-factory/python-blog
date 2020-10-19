import re
import json # json is needed to decode a string
from textwrap import dedent
from typing import Iterable, Mapping, Tuple
from lark import Lark, Transformer, v_args
from . import entities as e
from . import entity_types as et
from . import definitions


@v_args(inline=True)
class LanguageTransformer(Transformer):
    @staticmethod
    def integer(token):
        return e.Integer(int(token))

    @staticmethod
    def string(token):
        return e.String(json.loads(
            re.sub(r"\s+", " ", str(token))
        ))

    @staticmethod
    def raw_string(token):
        s = str(token)[2:-2].replace("\n", "\\n")
        return e.String(dedent(json.loads(s)))

    @staticmethod
    def name(token):
        return e.Name(str(token))

    @staticmethod
    def sexpr(fn, *args):
        return e.Sexpr(fn, args)


parser = Lark.open(
    "grammar.lark",
    rel_to=__file__,
    parser="lalr",
    transformer=LanguageTransformer(),
)


def parse(source: str) -> e.Entity:
    return parser.parse(source)  # type: ignore


def html(source: str, extensions: Iterable[Tuple[str, e.Entity]] = ()) -> str:
    runtime = {**definitions.BUILTINS}
    runtime.update(extensions)
    expr = parse(source).evaluate(runtime)
    return expr.render(runtime).as_text()
