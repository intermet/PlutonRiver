import numpy as np
import io
import base64
import time

from PIL import Image
from selenium import webdriver

import gym
from gym import spaces






class Game(gym.Env):
    
    keys = ['nop', 'up', 'down', 'right', 'left']
    URL = "https://d29zfk7accxxr5.cloudfront.net/games/game-142/data/index.html"

    def __init__(self, state_shape=64, tick=0.2):
        self.driver = webdriver.PhantomJS()
        self.driver.get(self.URL)
        self.paused = False
        self.states = None
        
        self.state_shape = state_shape, state_shape 
        self.tick = tick
        
        self.viewer = None
        
        self.action_space = gym.spaces.Discrete(5)
        self.low = np.zeros(self.state_shape)
        self.high = 255 * np.ones(self.state_shape)
        self.observation_space = gym.spaces.Box(low=self.low, high=self.high)
        
        #self._reset()
        
    def _screen(self):
        data = self.driver.execute_script(
            "return document.getElementById('canvas').toDataURL().substring(22)"
        )
        data = base64.b64decode(data)
        image = Image.open(io.BytesIO(data))
        image.thumbnail((64, 64), Image.ANTIALIAS)
        image = image.convert('L')
        return np.asarray(image)

    def _reset(self):
        self.run("gamee.onRestart()")
        init = self._screen()
        self.states = [init] * 5
        self.pause()
        return self.states[-1]
    
    def _step(self, a):
        if a:
            self.key(self.keys[a])
            over = self.check_gameOver()
            return self.states[-1], int(not over), over, None
        else:
            return self.states[-1], 0, False, None
    
    def pause(self):
        self.run("gamee.onPause()")
        self.paused = True

    def resume(self):
        assert self.paused
        self.run("gamee.onResume()")
        self.paused = False
        
    def key(self, k):
        self.resume()
        self.run(
            'gamee.controller.trigger("keydown", {button: "'+k+'"})'
        )
        time.sleep(self.tick)
        self.run(
            'gamee.controller.trigger("keyup", {button: "'+k+'"})'
        )
        self.pause()
        
        self.states = self.states[1:]
        self.states.append(self._screen())
    
    def run(self, sript):
        return self.driver.execute_script(sript)

    def check_gameOver(self):
        over = np.all(self.states[-1] == np.zeros(self.state_shape)) 
        return over

    
    


