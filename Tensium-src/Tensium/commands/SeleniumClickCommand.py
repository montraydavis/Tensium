import string
from typing import overload
from selenium.webdriver import Chrome
from Tensium.commands.SeleniumBaseCommand import SeleniumBaseCommand


class SeleniumClickCommand(SeleniumBaseCommand):
    element_selector: string = None
    value: string = None

    def __init__(self, element_selector: string) -> None:
        super().__init__()

        self.element_selector = element_selector

    def execute(self, driver: Chrome):
        try:
            element = driver.find_element_by_css_selector(self.element_selector)
    
            element.click()

        except: 
            pass
        pass