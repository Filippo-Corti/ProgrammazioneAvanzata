from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Obj:
    first: int
    second: str
    third: float
