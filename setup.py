%%481_Final_Project/setup.py
from setuptools import setup

setup(name='food_war', # the package/module name
      version='1.0', # the version (an arbitrary string)
      author='Joshua Carver',
      author_email='joshua.carver@wsu.edu',
      py_modules=[ 'combat', 'constants', 'enemy_class', 'joystick', 'main', 'mainmenu', 'maphandler', 'overworld', 'player_class' ], # modules in the package
      )