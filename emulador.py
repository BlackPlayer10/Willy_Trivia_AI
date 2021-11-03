from modules.recognition import calc_touch_answers, touch_screen, tap
import time

class Emulador:
    def __init__(self, id, key):
        self.id = id
        self.dic_key = key
        self.touch_answers = []
    
    def set_touch_answers(self):
        self.touch_answers = calc_touch_answers(self.id, self.dic_key)
    
    def touch(self,answer):
        for i in range(0, 1000, 30):
            #touch_screen(self.id, (300,15+i))
            tap("/dev/input/event6", 300, 15+i, self.id)

a = Emulador("R9TMA04DF0J", "luigi")
a.set_touch_answers()
print(a.touch_answers)
a.touch("A")