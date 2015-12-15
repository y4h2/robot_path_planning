# NOTICE
This project forks from pysimiam project and remove some unneccessary file <br/>
PySimiam documents http://pysimiam.sourceforge.net/index.html

# robot_path_planning
Path planning of dynamic environment with genetic algorithm and Finite State Machine


# Running Project
## Prerequest Library
- Numpy
- PyQt
Recommend installing Anaconda Package which include all common library

## Running
cd into robot_path_planning root folder, run command ```python qtpysimim.py```

# My Works
## three supervisors
- /supervisors/ga.py (state machine for Quickbot)
- /supervisors/ga_k3.py (state machine for khepera3)
- /supervisors/movingobstacle.py (state machine for moving obstacle)

## Three controllers
- /controllers/followpath.py (used in ga.py and ga_k3.py)
- /controllers/movingtopoint1.py (used in movingobstacle.py)
- /controllers/movingtopoint2.py (used in movingobstacle.py)

## Genetic algorithm with optimal operation
- /scripts/genetic_algorithm.py

## Collision detect algorithm
- /scripts/collision_detect.py
