import pyglet
from pyglet import resource

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()


floorImage = pyglet.resource.image('floor.png')
wallImage = pyglet.resource.image('wall.png')
goalImage = pyglet.resource.image('goal.png')
boxFloorImage = pyglet.resource.image('box-floor.png')
boxGoalImage = pyglet.resource.image('box-goal.png')
playerFloorImage = pyglet.resource.image('player-floor.png')
playerGoalImage = pyglet.resource.image('player-goal.png')