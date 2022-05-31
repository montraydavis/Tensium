import string
from selenium.webdriver import Chrome


class TensiumBaseGoal():
    element = None
    value_selector: string = None
    element_selector: string = None
    config: dict = {}

    def __init__(self, element_selector: string, value_selector: string, config: dict) -> None:
        self.element_selector = element_selector
        self.value_selector = value_selector
        if config is not None:
            self.config = config
        else:
            self.config = {}
       
    def check_goal(self, env) -> bool:
        try:
            self.element = env.driver_wrapper.driver.find_element_by_css_selector(self.element_selector)
        except:
            return False

        if self.element is None:
            return False

        return env.get_discounts() <= 0