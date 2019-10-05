import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from PIL import Image as PILIMAGE
import json
from os import listdir
from io import BytesIO
import threading
from modules import resources, board, solver, stopwatch


class SokobanLayout(BoxLayout):
    def __init__(self, **kwargs):
        with open('levels/standard/1.json') as json_file:
            levelData = json.load(json_file)
        self.gameBoard = board.Board(levelData)
        canvas_img = self.gameBoard.drawnLevel
        data = BytesIO()
        canvas_img.save(data, format='png')
        data.seek(0)
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.image = Image()
        self.image.texture = im.texture
        self.SolverAI = solver.Solver(self.gameBoard.GetData())
        self.running = False
        self.manual = False
        self.levelSrc = 'standard'
        self.windowSize = Window.size
        self.stopWatch = stopwatch.StopWatch()
        self.waiting = False
        super(SokobanLayout, self).__init__(**kwargs)

        ###initialize the level selection dropdown
        dropdown = DropDown()
        for level in listdir('levels/' + self.levelSrc):
            levelName = level[:-5]
            btn = Button(text=levelName, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            btn.bind(on_press=lambda btn: self.LoadLevel(btn.text))
            dropdown.add_widget(btn)
        self.mainButton = Button(text='1', pos=(100,500))
        self.mainButton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.mainButton, 'text', x))        
        self.ids['load_level'].add_widget(self.mainButton)

        srcDropdown = DropDown()
        stButton = Button(text='Standard', size_hint_y=None, height=44)
        stButton.bind(on_release=lambda btn: srcDropdown.select(btn.text))
        stButton.bind(on_press=lambda btn: self.ChangeLvlSrc(btn.text))
        srcDropdown.add_widget(stButton)
        dbButton = Button(text='Debug', size_hint_y=None, height=44)
        dbButton.bind(on_release=lambda btn: srcDropdown.select(btn.text))
        dbButton.bind(on_press=lambda btn: self.ChangeLvlSrc(btn.text))
        srcDropdown.add_widget(dbButton)
        srcButton = Button(text='Level Group', pos=(0,500))
        srcButton.bind(on_release=srcDropdown.open)
        srcDropdown.bind(on_select=lambda instance, x: setattr(srcButton, 'text', x))        
        self.ids['load_level'].add_widget(srcButton)

    def Run(self, dt):
        self.stopWatch.Update(dt)
        self.UpdateTimer()
        if not self.waiting:
            self.waiting = True
            temp = threading.Thread(target=self.RequestDecision)
            temp.start()
            self.UpdateBoardImage()

    def RequestDecision(self):
        isSolved = 0
        decision = self.SolverAI.Decide()
        if isinstance(decision, list):
            for move in decision:
                isSolved = self.gameBoard.Move(move)
        else:
            if decision == "Stop":
                self.ToggleRun()
                self.waiting = False
                return
            isSolved = self.gameBoard.Move(decision)
            if decision == "Reset":
                self.SolverAI.UpdateData(self.gameBoard.GetData())
        if isSolved:
            self.stopWatch.Press()
            self.ToggleRun()
            Clock.schedule_once(self.UpdateBoardImage, 1/100.0)
        self.waiting = False

    def UpdateBoardImage(self, dt=0):
        canvas_img = self.gameBoard.drawnLevel
        data = BytesIO()
        canvas_img.save(data, format='png')
        data.seek(0)
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.image.texture = im.texture

    def UpdateTimer(self):
        time = self.stopWatch.GetTime()
        if time[-2] == '.':
            time = time + '0'
        for i in range(7-len(time)):
            time = '0' + time
        time = time[0:2] + '.' + time[2:]
        self.ids['timer'].text = time

    def ToggleRun(self):
        self.stopWatch.Press()
        if self.running:
            self.running = False
            button = self.ids['run_toggler']
            button.text = "Resume"
            Clock.unschedule(self.Run)
        else:
            Clock.schedule_interval(self.Run, 1/32.0)
            self.running = True
            button = self.ids['run_toggler']
            button.text = "Pause"

    def ChangeLvlSrc(self, newSrc):
        self.levelSrc = newSrc
        self.ids['load_level'].remove_widget(self.mainButton)
        dropdown = DropDown()
        for level in listdir('levels/' + self.levelSrc):
            levelName = level[:-5]
            btn = Button(text=levelName, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            btn.bind(on_press=lambda btn: self.LoadLevel(btn.text))
            dropdown.add_widget(btn)
        self.mainButton = Button(text='Dropdown', pos=(100,500))
        self.mainButton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.mainButton, 'text', x))        
        self.ids['load_level'].add_widget(self.mainButton)

    def LoadLevel(self, levelName):
        with open('levels/' + self.levelSrc + '/' + levelName + '.json') as json_file:
            levelData = json.load(json_file)
        self.gameBoard = board.Board(levelData)
        canvas_img = self.gameBoard.drawnLevel
        data = BytesIO()
        canvas_img.save(data, format='png')
        data.seek(0)
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.image.texture = im.texture
        self.SolverAI = solver.Solver(self.gameBoard.GetData())
        self.running = False
        self.stopWatch.Reset()
        self.UpdateTimer()

class SokobanApp(App):
    def build(self):
        return SokobanLayout()

if __name__ == '__main__':
    SokobanApp().run()