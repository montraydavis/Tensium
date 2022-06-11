import base64
import io

from selenium.webdriver.remote.webelement import WebElement
from Tensium.envs.TensiumEnv import TensiumEnv
from Tensium.helpers.ImageInlierDetector import ImageInlierDetector
from PIL import Image

class TensiumObservation():
    env: TensiumEnv
    elements_watched: list
    elements_watching = {}
    revision: int = 0

    inlier_history = {}
    data = {}

    def get_elements(self, info: dict):
        self.elements_watching = {}

        for element_selector in self.elements_watched:
            try:
                web_element = self.env.driver_wrapper.driver.find_element_by_css_selector(element_selector)
                if web_element is not None:
                    self.elements_watching[element_selector] = web_element
            except: pass

    def __on_tensium_stepped__(self, info: dict):
        for element_key in self.elements_watching.keys():
            web_element: WebElement = self.elements_watching[element_key]
            element_screenshot = web_element.screenshot_as_base64
            element_screenshot = base64.b64decode(element_screenshot)
            element_screenshot = Image.open(io.BytesIO(element_screenshot)).convert('RGB')

            element_id = ('{}:{}').format(self.env.driver_wrapper.driver.current_url, element_key)

            if self.data.__contains__(element_id) == True:
                inliers = int(ImageInlierDetector().get_image_inliers(self.data[element_id], element_screenshot))

                if self.inlier_history.keys().__contains__(element_key) == False:
                    self.inlier_history[element_key] = []

                self.inlier_history[element_key].append(inliers)


            self.data[element_id] = element_screenshot



        self.revision += 1
                
        pass

    def __init__(self, env: TensiumEnv, elements_watched: list, auto_refresh = True) -> None:
        self.env = env
        self.elements_watched = elements_watched

        if auto_refresh == True:
            env.event_handlers['on_stepped'] += lambda info: self.get_elements(info)

        env.event_handlers['on_stepped'] += lambda info: self.__on_tensium_stepped__(info)

    pass