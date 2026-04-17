from typing import AbstractSet, Optional, Set, Union

from pddl.core import And, Formula, Predicate
from pddl.logic.base import Not

Literal = Union[Predicate, Not]
State = AbstractSet[Formula]
Plan = list[str]


def get_strips_literal_list(formula: Optional[Formula]) -> list[Literal]:
    """Get list of literals from a conjunct of literal"""
    if formula is None:
        return []
    elif isinstance(formula, And) and all(
        isinstance(c, Literal) for c in formula.operands
    ):
        return list(formula.operands)
    elif isinstance(formula, Literal):
        return [formula]
    else:
        raise ValueError(f"Unsupported input {formula}")
