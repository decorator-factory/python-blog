import json # json is needed to decode a string
from lark import Lark, Transformer, v_args
from . import entities as e
from . import entity_types as et


@v_args(inline=True)
class LanguageTransformer(Transformer):
    @staticmethod
    def integer(token):
        return e.Integer(int(token))

    @staticmethod
    def string(token):
        return e.String(json.loads(str(token)))

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
