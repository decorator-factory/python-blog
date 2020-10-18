from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple
from content_parser import entity_types as et
import html


class Entity:
    @property
    def ty(self):
        return et.TAny()

    def render(self, runtime) -> str:
        e = self.evaluate(runtime)
        if hasattr(e, "render_inline"):
            return e.render_inline(runtime) # type: ignore
        if hasattr(e, "render_block"):
            return e.render_block(runtime) # type: ignore
        raise TypeError(f"Cannot render {e}")

    def evaluate(self, runtime) -> Entity:
        return self


@dataclass(eq=True)
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
        self._cached = runtime[self.name]
        if self._cached is None:
            raise KeyError(f"Name {self.name} not found")
        return self._cached


@dataclass(eq=True)
class Sexpr(Entity):
    fn: Entity
    args: Tuple[Entity, ...]

    _cached: Optional[Entity] = None

    @property
    def ty(self):
        if self._cached is None:
            return et.TAny()
        return self._cached.ty

    def evaluate(self, runtime):
        self.fn = self.fn.evaluate(runtime)
        if not hasattr(self.fn, "call"):
            raise TypeError(f"Trying to call {self.fn.ty.signature()}")
        self.args = tuple(e.evaluate(runtime) for e in self.args)
        self._cached = self.fn.call(*self.args).evaluate(runtime) # type: ignore
        assert self._cached is not None
        return self._cached


@dataclass(frozen=True, eq=True)
class Integer(Entity):
    value: int

    ty = et.TInt()

    def render_inline(self, runtime):
        return str(self.value)


@dataclass(frozen=True, eq=True)
class String(Entity):
    value: str

    ty = et.TStr()

    def render_inline(self, runtime):
        return html.escape(self.value, quote=True)


@dataclass(frozen=True, eq=True)
class InlineTag(Entity):
    tag: str
    options: str
    children: Tuple[Entity, ...]

    ty = et.TInline()

    def render_inline(self, runtime):
        option_str = " "*(self.options != "") + self.options
        return (
             f"<{self.tag}{option_str}>"
            + "".join(e.render_inline(runtime) for e in self.children) # type: ignore
            +f"</{self.tag}>"
        )


@dataclass(frozen=True, eq=True)
class BlockTag(Entity):
    tag: str
    options: str
    children: Tuple[Entity, ...]

    ty = et.TBlock()

    def render_block(self, runtime):
        option_str = " "*(self.options != "") + self.options
        return (
             f"<{self.tag}{option_str}>"
            + "".join(e.render(runtime) for e in self.children)
            +f"</{self.tag}>"
        )


@dataclass(frozen=True, eq=True)
class InlineRaw(Entity):
    html: str

    ty = et.TInline()

    def render_inline(self, runtime):
        return self.html


@dataclass(frozen=True, eq=True)
class BlockRaw(Entity):
    html: str

    ty = et.TInline()

    def render_block(self, runtime):
        return self.html


@dataclass(frozen=True, eq=True)
class InlineConcat(Entity):
    children: Tuple[Entity, ...]

    ty = et.TInline()

    def render_inline(self, runtime):
        return "".join(e.render_inline(runtime) for e in self.children) # type: ignore


@dataclass(frozen=True, eq=True)
class BlockConcat(Entity):
    children: Tuple[Entity, ...]

    ty = et.TBlock()

    def render_block(self, runtime):
        return "".join(e.render(runtime) for e in self.children) # type: ignore


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
        arg_types_repr = "(" + ", ".join(e.ty.signature() for e in args) + ")"
        raise TypeError(f"Cannot call {self.ty.signature()} with {arg_types_repr}")


    def return_type_when_called_with(self, *, args, rest):
        # TODO: implement these cases:
        # (λ x ...y . z) can be called as (λ x y y y . z)
        # (λ x y ...y . z) can be called as (λ x y y y . z)
        # (λ x y y y y ...y . z) can't be called as (λ x y y y . z)
        for o in self.overloads.keys():
            if o.arg_types == args and o.rest_type == rest:
                return o.return_type
        return None
