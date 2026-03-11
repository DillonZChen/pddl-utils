from pddl.action import Action
from pddl.logic import Predicate
from pddl.logic.base import And, Formula, Not

from pddlutils.utils import get_strips_literal_list
from pddlutils.exceptions import PDDLLogicError


def regressable(condition: Formula, action: Action) -> bool:
    r"""Check if a condition g is regressable under an action a.

    Defined for STRIPS as (\add(a) \cap g \neq \emptyset) \and (\del(a) \cap g = \emptyset)
    """

    g = set()
    add_effect = []
    del_effect = []

    for g_cond in get_strips_literal_list(condition):
        if isinstance(g_cond, Predicate):
            g.add(g_cond)
        elif isinstance(g_cond, Not) and isinstance(g_cond.argument, Predicate):
            raise NotImplementedError("Negative regression not yet supported")
        else:
            raise NotImplementedError(f"Unsupported condition type: {type(g_cond)}")

    for effect in get_strips_literal_list(action.effect):
        if isinstance(effect, Predicate):
            add_effect.append(effect)
        elif isinstance(effect, Not) and isinstance(effect.argument, Predicate):
            del_effect.append(effect.argument)
        else:
            raise NotImplementedError(f"Unsupported effect type: {type(effect)}")

    non_empty_add_intersection = any(eff in g for eff in add_effect)
    empty_del_intersection = all(eff not in g for eff in del_effect)

    return non_empty_add_intersection and empty_del_intersection


def regress_goal(condition: Formula, action: Action) -> Formula:
    r"""Regress a condition g over an action a

    Defined for STRIPS as (g \setminus \add(a)) \cup \pre(a)
    """
    if not regressable(condition, action):
        raise PDDLLogicError("Action is not regressable under the given condition.")

    g = set()
    add_effect = set()
    precondition = set()

    for g_cond in get_strips_literal_list(condition):
        if isinstance(g_cond, Predicate):
            g.add(g_cond)
        elif isinstance(g_cond, Not) and isinstance(g_cond.argument, Predicate):
            raise NotImplementedError("Negative regression not yet supported")
        else:
            raise NotImplementedError(f"Unsupported condition type: {type(g_cond)}")

    for effect in get_strips_literal_list(action.effect):
        if isinstance(effect, Predicate):
            add_effect.add(effect)
        elif isinstance(effect, Not) and isinstance(effect.argument, Predicate):
            pass  # del effects do not affect regression
        else:
            raise NotImplementedError(f"Unsupported effect type: {type(effect)}")

    for condition in get_strips_literal_list(action.precondition):
        if isinstance(condition, Predicate):
            precondition.add(condition)
        elif isinstance(condition, Not) and isinstance(condition.argument, Predicate):
            raise NotImplementedError("Negative regression not yet supported")
        else:
            raise NotImplementedError(f"Unsupported precondition type: {type(condition)}")

    regr = (g - add_effect) | precondition

    return And(*regr)
