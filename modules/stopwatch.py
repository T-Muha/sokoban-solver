import time

#can be started, paused, and cleared

class StopWatch():
    def __init__(self, *args, **kwargs):
        self.running = False
        self.time = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

    def Press(self):
        self.running = False if self.running else True

    def GetTime(self):
        return str(round(self.seconds + self.minutes * 100, 2))

    def Update(self, dt):
        if self.running:
            self.seconds += dt
            if self.seconds > 60:
                self.seconds -= 60
                self.minutes += 1
                if self.minutes > 60:
                    self.minutes -= 60
                    self.hours += 1

    def Clear(self):
        self.seconds = 0.0
        self.minutes = 0
        self.hours = 0

    def Reset(self):
        if self.running:
            self.Press()
        self.Clear()