import string
from turtle import home
from selenium.webdriver import Chrome

class ChromeDriverWrapper():
    executable_path: string = ""
    driver: Chrome = None
    home_page: string = None

    def __init__(self, executable_path: string, homepage: string = "https://saucedemo.com/"):
        self.executable_path = executable_path
        self.driver = Chrome(executable_path=self.executable_path)
        self.home_page = homepage
        self.driver.get(self.home_page)

    
    def reset(self):
        try:
            if self.driver is not None:
                self.driver.close()
        except:
            pass

        if self.driver is not None:
            self.driver.quit()

        self.driver = Chrome(executable_path=self.executable_path)
        self.driver.get(self.home_page)
        