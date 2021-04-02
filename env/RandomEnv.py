# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:46:17 2021

@author: Stéphane du Hamel

En python car si j'ai bien compris il va falloir s'y habituer (et c'est plus simple)

Environnement par défaut
Appeller default_environement() crée un dictionnaire avec les fonctions de base
"""

from Classes import *
from Interpreter import *

import random as rd


def random_environement(parent : Scope = None) -> Scope:
    env = Scope(parent)
    env.update({
        'randSeed': rd.seed,
        'randRange':rd.randrange,
        'randInt':rd.randint
        })
    return env

###################################################
# Built-in functions which need acces to local Env
