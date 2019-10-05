import time

#can be started, paused, and cleared

class StopWatch():
    def __init__(self, *args, **kwargs):
        self.running = False
        self.time = 0

    def Press(self):
        self.running = False if self.running else True

    def GetTime(self):
        return str(round(self.time, 2))

    def Update(self, dt):
        if self.running:
            self.time += dt
        return self.time

    def Clear(self):
        self.time = 0.0

    def Reset(self):
        if self.running:
            self.Press()
        self.Clear()