from lark import Lark, Transformer

parser = Lark.open("grammar.lark", rel_to=__file__, parser="lalr")

EXAMPLE = """
($
    ((h 1)
        "Hello, world!"
    )
    "Welcome to " (bf "my") " blog! It is:"
    (list-unordered
        (it "cool")
        ($ (bf "super") " awesome")
        ((style "color: red; font-size: 100%") "amazing")
    )
)
"""

tree = parser.parse(EXAMPLE)
print(tree.pretty())