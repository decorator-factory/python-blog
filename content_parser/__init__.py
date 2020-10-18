import re
import json # json is needed to decode a string
from typing import Mapping
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


def run_with_runtime(source: str, runtime: Mapping[str, e.Entity]) -> e.Entity:
    parsed = parse(source)
    return parsed.evaluate(runtime)

def run(source: str) -> e.Entity:
    return run_with_runtime(source, definitions.BUILTINS)

def html(source: str) -> str:
    result = run(source)
    return result.render()