from modules.recognition import calc_touch_answers, touch_screen

class Emulador:
    def __init__(self, id, key):
        self.id = id
        self.dic_key = key
        self.touch_answers = []
    
    def set_qlines(self):
        self.touch_answers = calc_touch_answers(self.id, self.dic_key)
    
    def touch(self,answer):
        touch_screen(self.id, (100,5))

a = Emulador("R9TMA04DF0J", "luigi")
a.set_qlines()
print(a.touch_answers)
a.touch("A")