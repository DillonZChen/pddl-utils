from pddl.core import Action, Predicate, And
from pddl.logic.base import Not
from pddl.logic.helpers import constants, variables

from pddlutils.regression import regress_action


def test_simple():
    x, y = variables("x y")
    p_on = Predicate("on", x, y)
    p_holding = Predicate("holding", x)
    a_pick_up = Action(
        name="pick-up",
        parameters=[x, y],
        precondition=p_on(x, y),
        effect=And(p_holding(x), Not(p_on(x, y))),
    )

    a, b, c = constants("a b c")
    condition = And(p_holding(a), p_on(b, c))
    action = a_pick_up.instantiate([a, b])

    regr_cond = regress_action(condition, action)
    regr_cond_expected = And(p_on(a, b), p_on(b, c))
    assert regr_cond == regr_cond_expected
