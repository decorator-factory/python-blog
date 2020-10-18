from content_parser.entities import Entity
from dataclasses import dataclass
from typing import Optional, Tuple


adt = dataclass(frozen=True, eq=True)


class EntityType:
    def match(self, value):
        return value.ty == self

    def signature(self):
        raise NotImplementedError


@adt
class TAny(EntityType):
    def match(self, _value):
        return True

    def signature(self):
        return "Any"


@adt
class TInt(EntityType):
    def signature(self):
        return "int"


@adt
class TStr(EntityType):
    def signature(self):
        return "str"


@adt
class TInline(EntityType):
    def signature(self):
        return "inline"


@adt
class TBlock(EntityType):
    def signature(self):
        return "block"


@adt
class IInl(EntityType):
    def match(self, value):
        return hasattr(value, "render_inline")

    def signature(self):
        return "Inl"


@adt
class IBlk(EntityType):
    def match(self, value):
        return hasattr(value, "render_block")

    def signature(self):
        return "Blk"


@adt
class IRen(EntityType):
    def match(self, value):
        return IInl().match(value) or IBlk().match(value)

    def signature(self):
        return "Ren"


@adt
class TFunction(EntityType):
    arg_types: Tuple[EntityType, ...]
    rest_type: Optional[EntityType]
    return_type: EntityType

    def match(self, value):
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
        return "(λ {args_repr} . {return_repr})"
