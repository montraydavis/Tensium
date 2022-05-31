import string
from Tensium.TensiumEnv import TensiumEnv
from Tensium.goals.TensiumTextComparerBaseGoal import TensiumTextComparerBaseGoal


class TensiumTextNotEqualsGoal(TensiumTextComparerBaseGoal):
    config: dict = {}
    element_text: string = None

    def __init__(self, element_selector: string, value_selector: string, config: dict = {}) -> None:
        super(TensiumTextNotEqualsGoal, self).__init__(
            element_selector, value_selector, config)

        if config is not None:
            self.config = config

        pass

    def check_goal(self, env: TensiumEnv) -> bool:

        if super(TensiumTextNotEqualsGoal, self).check_goal(env) == True:
            return self.get_text(env) != self.value_selector

        return False
