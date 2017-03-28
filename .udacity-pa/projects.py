import argparse
from udacity_pa import udacity

nanodegree = 'nd889'
projects = ['sudoku']

def submit(args):
  filenames = ['solution.py']

  udacity.submit(nanodegree, projects[0], filenames, 
                 environment = args.environment,
                 jwt_path = args.jwt_path)
