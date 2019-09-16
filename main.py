import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from PIL import Image as PILIMAGE
import json
from io import BytesIO
from modules import resources, board, solver

class SokobanLayout(BoxLayout):
    def __init__(self, **kwargs):
        with open('levels/test-level.json') as json_file:
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

        super(SokobanLayout, self).__init__(**kwargs)

    def tempFunc(self):
        isSolved = 0
        counter = 0
        while isSolved == 0:
            if not counter == 3:
                self.gameBoard.Move(self.SolverAI.Decide())
                self.SolverAI.UpdateData(self.gameBoard.GetData())
                self.UpdateBoardImage()
                counter += 1
        self.gameBoard.Move(self.SolverAI.Decide())
        self.SolverAI.UpdateData(self.gameBoard.GetData())
        self.UpdateBoardImage()

    def UpdateBoardImage(self):
        canvas_img = self.gameBoard.drawnLevel
        data = BytesIO()
        canvas_img.save(data, format='png')
        data.seek(0)
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.image.texture = im.texture

Builder.load_file("Sokoban.kv")

class SokobanApp(App):
    def build(self):
        return SokobanLayout()

if __name__ == '__main__':
    SokobanApp().run()