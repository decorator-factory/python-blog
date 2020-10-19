from dataclasses import dataclass
from typing import Optional, Tuple


class EntityType:
    def match(self, value):
        return value.ty == self or value.ty == TAny()

    def signature(self):
        raise NotImplementedError


@dataclass(frozen=True, eq=True)
class TAny(EntityType):
    def match(self, _value):
        return True

    def signature(self):
        return "Any"


@dataclass(frozen=True, eq=True)
class TInt(EntityType):
    def signature(self):
        return "int"


@dataclass(frozen=True, eq=True)
class TStr(EntityType):
    def signature(self):
        return "str"


@dataclass(frozen=True, eq=True)
class TInline(EntityType):
    def signature(self):
        return "inline"


@dataclass(frozen=True, eq=True)
class TBlock(EntityType):
    def signature(self):
        return "block"


@dataclass(frozen=True, eq=True)
class IInl(EntityType):
    def match(self, value):
        if super().match(value):
            return True
        return hasattr(value, "render_inline")

    def signature(self):
        return "Inl"


@dataclass(frozen=True, eq=True)
class IBlk(EntityType):
    def match(self, value):
        if super().match(value):
            return True
        return hasattr(value, "render_block")

    def signature(self):
        return "Blk"


@dataclass(frozen=True, eq=True)
class IRen(EntityType):
    def match(self, value):
        if super().match(value):
            return True
        return IInl().match(value) or IBlk().match(value)

    def signature(self):
        return "Ren"


@dataclass(frozen=True, eq=True)
class TFunction(EntityType):
    arg_types: Tuple[EntityType, ...]
    rest_type: Optional[EntityType]
    return_type: EntityType

    def match(self, value):
        if super().match(value):
            return True
        return (
            hasattr(value, "call")
            and value.return_type_when_called_with(
                args=self.arg_types,
                rest=self.rest_type,
            ) == self.return_type
        )

    def signature(self):
        args_repr = " ".join(t.signature() for t in self.arg_types)
        if self.rest_type is not None:
            args_repr += " ..." + self.rest_type.signature()
        return_repr = self.return_type.signature()
        return f"(λ {args_repr} . {return_repr})"


@dataclass(frozen=True, eq=True)
class TUnion(EntityType):
    variants: Tuple[EntityType, ...]

    def match(self, value):
        if super().match(value):
            return True
        return any(t.match(value) for t in self.variants)

    def signature(self):
        return "|".join(t.signature() for t in self.variants)