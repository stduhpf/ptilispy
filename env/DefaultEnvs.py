# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:46:17 2021

@author: Stéphane du Hamel

En python car si j'ai bien compris il va falloir s'y habituer (et c'est plus simple)

Environnement par défaut
Appeller default_environement() crée un dictionnaire avec les fonctions de base
"""

from Parser import *
from Classes import *
from Interpreter import *

from env.MathEnv import *
from env.RandomEnv import *

# Définition de l'environement par défaut
import math as m
import operator as o


def noop(*args, **kw): pass


def default_environement(discard=None) -> Scope:
    EnvList = dict()
    EnvList.update({
        'math': math_environement,
        'random': random_environement,

        'new': Scope,
        'file': Scope
    })
    env = Scope()
    env.update({

        'if':   BuiltIn(_if),
        'cond': BuiltIn(_cond),
        'while': BuiltIn(_while),
        'for':  BuiltIn(_for),

        'defun':    BuiltIn(_defun),
        'define':   BuiltIn(_define),
        'set':      BuiltIn(_set),
        'incf':     BuiltIn(_postIncf),
        'decf':     BuiltIn(_postDecf),
        'inc':      BuiltIn(_postInc),
        'dec':      BuiltIn(_postDec),
        '++f':      BuiltIn(_preIncf),
        '--f':      BuiltIn(_preDecf),
        '++':       BuiltIn(_preInc),
        '--':       BuiltIn(_preDec),

        'load':     BuiltIn(_loadEnv),

        'try':  BuiltIn(_try),

        '>': o.gt,
        '<': o.lt,
        '>=': o.ge,
        '<=': o.le,
        '=': o.eq,
        '/=': o.ne,
        'and': lambda *x: all(x),
        'or': lambda *x: any(x),
        'not': lambda *x: not x[0],


        '+': o.add,
        '-': o.sub,
        '*': o.mul,
        '/': o.truediv,

        'max': max,
        'min': min,

        'logand': o.and_,
        'logor': o.or_,
        'logxor': o.xor,
        'lognor': lambda x, y: o.not_(o.or_(x, y)),
        'logeqv': lambda x, y: o.not_(o.xor(x, y)),

        'rem': o.mod,
        'abs': abs,
        'floor': lambda x: int(x) if (x >= 0 or x == int(x)) else int(x)-1,
        'ceil': lambda x: int(x) if (x <= 0 or x == int(x)) else int(x)+1,
        'fract': lambda x: m.modf(x)[0],


        'list': lambda *x:  list(x),
        'list?': lambda x:   isinstance(x, list),
        'elem': lambda l, n: l[n],
        'merge': lambda l1, l2: [*l1, *l2],
        'len': len,

        'noret': noop,  # on ne retourne aucune valeur
        # on retourne la derniere valeur de la liste
        'retlast': lambda *x: x[-1],
        # on retourne la premiere valeur de la liste
        'retfirst': lambda *x: x[0],


        'print': print,
        'input': input,

        'intcast': int,
        'floatcast': float,
        'stringcast': str,

        't': True,
        'nil': False,

        'ans': Symbol('Nil'),

        '_plispyEnvs': EnvList  # you are not supposed to access this one
    })
    return env


###################################################
# Built-in functions which need acces to local Env

def _if(args: list, env: Scope):
    a = len(args)
    if a == 3:
        (con, the, els) = args
        res = the if evaluate(con, env) else els
        value = evaluate(res, env)
        return value
    elif a == 2:
        (con, the) = args
        if evaluate(con, env):
            res = the
            value = evaluate(res, env)
            return value
        else:
            return Symbol('nil')
    else:
        raise argumentException('if', '2 or 3', a)


def _cond(args: list, env: Scope):
    for test in args:
        cond = evaluate(test[0], env)
        if cond:
            return evaluate(test[1], env)
            break
    return Symbol('t')


def _while(args: list, env: Scope):
    a = len(args)
    if a > 0:
        while evaluate(args[0], env):
            loopEnv = Scope(env)
            [evaluate(elem, loopEnv) for elem in args[1:]]
        return Symbol('t')
    else:
        raise argumentException('while', 'at least 1', a)


def _for(args: list, env: Scope):
    a = len(args)
    if a >= 3:
        (start, cond, inc) = args[:3]
        outerLoopEnv = Scope(env)
        evaluate(start, outerLoopEnv)
        while evaluate(cond, outerLoopEnv):
            loopEnv = Scope(outerLoopEnv)
            [evaluate(elem, loopEnv) for elem in args[3:]]
            evaluate(inc, outerLoopEnv)
        return Symbol('t')
    else:
        raise argumentException('for', 'at least 3', a)

# definitions de variables et fonctions


def _defun(args: list, env: Scope):
    a = len(args)
    if a == 3:
        (name, parameters, body) = args
        if env.searchVarScope(name) == env:
            raise redefinitionException(name)
        env[name] = Fun(env, name, parameters, body)
        return Symbol('t')
    else:
        raise argumentException('defun', 3, a)


def _define(args: list, env: Scope):
    a = len(args)
    if a > 2:
        raise argumentException('define', '1 or 2', a)
    elif a == 2:
        (var, exp) = args
        value = evaluate(exp, env)
    else:
        var = args[0]
        value = Symbol('nil')
    if env.searchVarScope(var) != env:
        env[var] = value
    else:
        raise redefinitionException(var)
    return value

# acces aux variables


def _set(args: list, env: Scope):
    a = len(args)
    if a != 2:
        raise argumentException('set', 2, a)
    (var, exp) = args
    value = evaluate(exp, env)
    e = env.searchVarScope(var)
    if e != None:
        e[var] = value
    else:
        raise undefinedSymbolExeption(var)
    return value


def _postIncf(args: list, env: Scope):
    a = len(args)
    if a != 2:
        raise argumentException('incf', 2, a)
    (var, exp) = args
    value = evaluate(exp, env)
    e = env.searchVarScope(var)
    if e == None:
        raise undefinedSymbolExeption(var)
    ret = e[var]
    e[var] += value
    return ret


def _postDecf(args: list, env: Scope):
    a = len(args)
    if a != 2:
        raise argumentException('decf', 2, a)
    (var, exp) = args
    value = evaluate(exp, env)
    e = env.searchVarScope(var)
    if e == None:
        raise undefinedSymbolExeption(var)
    ret = e[var]
    e[var] -= value
    return ret


def _postInc(args: list, env: Scope):
    a = len(args)
    if a != 1:
        raise argumentException('inc', 1, a)
    var = args[0]
    e = env.searchVarScope(var)
    if e == None:
        raise undefinedSymbolExeption(var)
    ret = e[var]
    e[var] += 1
    return ret


def _postDec(args: list, env: Scope):
    a = len(args)
    if a != 1:
        raise argumentException('dec', 1, a)
    var = args[0]
    e = env.searchVarScope(var)
    if e == None:
        raise undefinedSymbolExeption(var)
    ret = e[var]
    e[var] -= 1
    return ret


def _preIncf(args: list, env: Scope):
    a = len(args)
    if a != 2:
        raise argumentException('++f', 2, a)
    (var, exp) = args
    value = evaluate(exp, env)
    e = env.searchVarScope(var)
    if e == None:
        raise undefinedSymbolExeption(var)
    e[var] += value
    return e[var]


def _preDecf(args: list, env: Scope):
    a = len(args)
    if a != 2:
        raise argumentException('--f', 2, a)
    (var, exp) = args
    value = evaluate(exp, env)
    e = env.searchVarScope(var)
    if e == None:
        raise undefinedSymbolExeption(var)
    e[var] -= value
    return e[var]


def _preInc(args: list, env: Scope):
    a = len(args)
    if a != 1:
        raise argumentException('++', 1, a)
    var = args[0]
    e = env.searchVarScope(var)
    if e == None:
        raise undefinedSymbolExeption(var)
    e[var] += 1
    return e[var]


def _preDec(args: list, env: Scope):
    a = len(args)
    if a != 1:
        raise argumentException('--', 1, a)
    var = args[0]
    e = env.searchVarScope(var)
    if e == None:
        raise undefinedSymbolExeption(var)
    e[var] -= 1
    return e[var]

# gestion des exceptions


def _try(args: list, env: Scope):
    a = len(args)
    if a != 2:
        raise argumentException('try', 2, a)
    code = args[0]
    catch = args[1]
    try:
        return evaluate(code, env)
    except runException as ex:
        e = env.searchVarScope('ans')
        if e == None:
            raise undefinedSymbolExeption('ans')
        e['ans'] = ex.message
        return evaluate(catch, env)
    return e[var]

# chargement d'environement de variables


# to be callsed from Python
def loadEnv(name: Symbol, env: Scope = None, a: list = []) -> Scope:
    e = env.searchVarScope('_plispyEnvs')
    constructor = e['_plispyEnvs'][name]
    if isinstance(constructor, Scope):
        newEnv = constructor
        newEnv.parent = env
    else:
        newEnv = constructor(env)
        if name == 'new':
            newEnv = env
        elif name == 'file':
            if len(a) != 2:
                raise argumentException('load file', '2 or 3', a-1)
            if e['_plispyEnvs'].get(a[1]) == None:
                e['_plispyEnvs'][a[1]] = newEnv
                evaluate(parseFile(a[0]), newEnv)
            else:
                raise redefinitionException(a[1])
    return newEnv


def _loadEnv(code: list, env: Scope):
    a = len(code)
    if a < 2:
        raise argumentException('load', 2, a)
    name = code[0]
    truecode = code[1]
    e = env.searchVarScope('_plispyEnvs')
    constructor = e['_plispyEnvs'][name]
    if isinstance(constructor, Scope):
        if a > 2:
            raise argumentException('load', 2, a)
        newEnv = constructor
        newEnv.parent = env
    else:
        newEnv = constructor(env)
        if name == 'new':
            if a != 3:
                raise argumentException('load new', 2, a-1)
            if e['_plispyEnvs'].get(code[1]) == None:
                e['_plispyEnvs'][code[1]] = newEnv
            else:
                raise redefinitionException(code[1])
            truecode = code[2]
        elif name == 'file':
            if a != 4 and a != 3:
                raise argumentException('load file', '2 or 3', a-1)
            if e['_plispyEnvs'].get(code[2]) == None:
                e['_plispyEnvs'][code[2]] = newEnv
                evaluate(parseFile(code[1]), newEnv)
            else:
                raise redefinitionException(code[2])
            if a == 3:
                return Symbol('t')
            truecode = code[3]
        else:
            if a > 2:
                raise argumentException('load', 2, a)
    return evaluate(truecode, newEnv)
