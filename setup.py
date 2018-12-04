from setuptools import setup, find_packages
setup(name='food_war',
      version='1.0',
      packages=setuptools.find_packages(),
      author='Joshua Carver',
      author_email='joshua.carver@wsu.edu',
      py_modules=[ 'combat', 'constants', 'enemy_class', 'joystick', 'main', 'mainmenu', 'maphandler', 'overworld', 'player_class' ], # modules in the package
      )
