from dataclasses import asdict, fields, is_dataclass
from typing import Generic, TypeVar

from sqlalchemy.orm import declarative_base

_Base = declarative_base()

_T = TypeVar("_T")
_D = TypeVar("_D")


def _get_domain_class(cls):
    if hasattr(cls, "__orig_bases__"):
        for base in cls.__orig_bases__:
            if hasattr(base, "__args__") and is_dataclass(base.__args__[0]):
                return base.__args__[0]
    raise ValueError(f"The domain model must be defined: {cls}")


class Base(Generic[_D], _Base):
    __abstract__ = True
    __domain__: type[_D]

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.__domain__ = _get_domain_class(cls)

    @classmethod
    def from_domain(cls: type[_T], domain) -> _T:
        return cls(**asdict(domain))

    def to_domain(self, **kwargs) -> _D:
        return self.__domain__(
            **{f.name: getattr(self, f.name) for f in fields(self.__domain__)}
        )
