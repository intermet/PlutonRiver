import numpy as np
import io
import base64

from PIL import Image
from selenium import webdriver


URL = "https://d29zfk7accxxr5.cloudfront.net/games/game-142/data/index.html"



class Game(object):

    def __init__(self):
        self.driver = webdriver.Chrome()

    def _screen(self):

        canvas = self.driver.find_element_by_css_selector("#canvas")
        data = self.driver.execute_script("return arguments[0].toDataURL().substring(22)", canvas)
        data = base64.b64decode(data)
        image = Image.open(io.BytesIO(data))
        return np.asarray(image)
        
g = Game()
g.driver.get(URL)


