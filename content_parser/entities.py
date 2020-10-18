from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple
from content_parser import entity_types as et
import html


class Entity:
    @property
    def ty(self):
        return et.TAny()

    def render(self) -> str:
        if hasattr(self, "render_inline"):
            return self.render_inline() # type: ignore
        if hasattr(self, "render_block"):
            return self.render_block() # type: ignore
        raise TypeError(f"Cannot render {self}")

    def evaluate(self, runtime) -> Entity:
        return self


@dataclass(frozen=True, eq=True)
class Name(Entity):
    name: str

    _cached: Optional[Entity] = None

    @property
    def ty(self):
        if self._cached is None:
            return et.TAny()
        else:
            return self._cached.ty

    def evaluate(self, runtime) -> Entity:
        self._cached = runtime.find_entity_by_name(self.name)
        if self._cached is None:
            raise KeyError(f"Name {self.name} not found")
        return self._cached


@dataclass(frozen=True, eq=True)
class Integer(Entity):
    value: int

    ty = et.TInt()

    def render_inline(self):
        return str(self.value)


@dataclass(frozen=True, eq=True)
class String(Entity):
    value: str

    ty = et.TStr()

    def render_inline(self):
        return html.escape(self.value, quote=True)


@dataclass(frozen=True, eq=True)
class InlineTag(Entity):
    tag: str
    options: str
    children: Tuple[Entity, ...]

    ty = et.TInline()

    def render_inline(self):
        return (
             f"<{self.tag} {self.options}>"
            + "".join(e.render_inline() for e in self.children) # type: ignore
            +f"</{self.tag}>"
        )


@dataclass(frozen=True, eq=True)
class BlockTag(Entity):
    tag: str
    options: str
    children: Tuple[Entity, ...]

    ty = et.TBlock()

    def render_block(self):
        return (
             f"<{self.tag} {self.options}>"
            + "".join(e.render() for e in self.children)
            +f"</{self.tag}>"
        )


@dataclass(frozen=True, eq=True)
class Function(Entity):
    overloads: Dict[et.TFunction, Callable]

    @property
    def ty(self):
        return et.TUnion(tuple(self.overloads.keys()))

    def call(self, *args):
        for (o, f) in self.overloads.items():
            if o.rest_type is None:
                same_length = len(o.arg_types) == len(args)
                types_match = all(
                    expected_type.match(arg)
                    for arg, expected_type in zip(args, o.arg_types)
                )
                if same_length and types_match:
                    return f(*args)
            else:
                for i in range(len(args) + 1):
                    positional_args, rest_args = args[:i], args[i:]

                    # check if the rest_args are the same
                    assert o.rest_type is not None
                    if not all(o.rest_type.match(r) for r in rest_args):
                        break

                    for arg, expected_type in zip(positional_args, o.arg_types):
                        if not expected_type.match(arg):
                            break

                    return f(*positional_args, *rest_args)
        raise TypeError(f"Cannot call {self} with {args}")


    def return_type_when_called_with(self, *, args, rest):
        # TODO: implement these cases:
        # (λ x ...y . z) can be called as (λ x y y y . z)
        # (λ x y ...y . z) can be called as (λ x y y y . z)
        # (λ x y y y y ...y . z) can't be called as (λ x y y y . z)
        for o in self.overloads.keys():
            if o.arg_types == args and o.rest_type == rest:
                return o.return_type
        return None
