import numpy as np
import io
import base64
import time

from PIL import Image
from selenium import webdriver


URL = "https://d29zfk7accxxr5.cloudfront.net/games/game-142/data/index.html"



class Game(object):

    def __init__(self, state_shape=128, tick=1):
        self.driver = webdriver.Chrome()
        self.paused = False
        self.states = []

        self.state_shape = state_shape, state_shape 
        self.tick = tick
        self.gameOver = False
        
    def _screen(self):
        data = self.driver.execute_script(
            "return document.getElementById('canvas').toDataURL().substring(22)"
        )
        data = base64.b64decode(data)
        image = Image.open(io.BytesIO(data))
        image.thumbnail((128, 128), Image.ANTIALIAS)
        image = image.convert('L')
        return np.asarray(image)

    def restart(self):
        self.run("gamee.onRestart()")
        self.states.append(self._screen())
        self.pause()
    
    def pause(self):
        self.run("gamee.onPause()")
        self.paused = True

    def resume(self):
        assert self.paused
        self.run("gamee.onResume()")
        self.paused = False
        
    def key(self, k):
        if self.check_gameOver(self.states[-1]):
            print("GameOver !")
            return 
        self.resume()
        self.run(
            'gamee.controller.trigger("keydown", {button: "'+k+'"})'
        )
        time.sleep(self.tick)
        self.run(
            'gamee.controller.trigger("keyup", {button: "'+k+'"})'
        )
        self.pause()
        self.states.append(self._screen())
        
    def run(self, sript):
        return self.driver.execute_script(sript)

    def check_gameOver(self, state):
        self.gameOver = np.all(state == np.zeros(self.state_shape)) 
        return self.gameOver

    
    
g = Game()
g.driver.get(URL)


