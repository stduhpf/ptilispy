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

import math as m


def math_environement(parent: Scope = None) -> Scope:
    env = Scope(parent)
    env.update({
        'sqrt': m.sqrt,
        'pow': m.pow,

        'exp': m.exp,
        'exp2': lambda x: m.pow(2, x),
        'exp10': lambda x: m.pow(10, x),

        'log':  m.log,
        'log2': m.log2,
        'log10': m.log10,

        'sin': m.sin,
        'cos': m.cos,
        'tan': m.tan,

        'asin': m.asin,
        'acos': m.acos,
        'atan': m.atan,

        'pi': m.pi,
        'e': m.e,
        'tau': m.tau
    })
    return env

###################################################
# Built-in functions which need acces to local Env
