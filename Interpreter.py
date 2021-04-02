# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:46:17 2021

@author: Stéphane du Hamel

En python car si j'ai bien compris il va falloir s'y habituer (et c'est plus simple)

Interpréteur récursif avec les classes nécessaires
"""

from Classes import *
from typing import Any, Callable


class runException(Exception):
    pass

class argumentException(runException):
    def __init__(self,name :str ,expected, got : int):
        self.name = name
        self.expected = expected
        self.got = got
        self.message = type(self).__name__+': Error when calling function \'' + str(name) + '\'No matching arguments, expected '+str(expected)+' got '+str(got)

class redefinitionException(runException):
    def __init__(self,name :str ):
        self.name = name
        self.message =  type(self).__name__+': Redefinition of variable \'' + str(name) + '\'\n\''+str(name)+'\' already exists in this scope'
        
class undefinedSymbolExeption(runException):
    def __init__(self,name :str ):
        self.name = name
        self.message =  type(self).__name__+': No variable or function named \'' + str(name) + '\' found in this scope or in parent scopes'
        
class indexException(runException):
    def __init__(self,name :str):
        self.name = name
        self.message =  type(self).__name__+': Index out of range for \'' + str(name) + '\''

class unCallableException(runException):
    def __init__(self,name :str):
        self.name = name
        self.message = type(self).__name__+':\'' + str(name) + '\' is not callable'

class unIterableException(runException):
    def __init__(self,name :str):
        self.name = name
        self.message = type(self).__name__+': When calling \'' + str(name) + '\'. One argument is not a list'

class castException(runException):
    def __init__(self,name :str):
        self.name = name
        self.message = type(self).__name__+': Cant cast \'' + str(name) + '\' to desired type'

class Scope(dict):
    def __init__(self,parent : dict = None, fusion : bool = False):
        self.parent=parent
        if fusion:
            self = parent.copy()
    def searchVarScope(self,var):
        return self if (var in self) else (self.parent.searchVarScope(var) if (self.parent != None) else None)


class Fun:
    def __init__(self,Env : Scope,name : str, ArgNames :list, body : list):
        self.Env = Env
        self.name = name
        self.ArgNames = ArgNames
        self.body = body
    def execute(self,ars,pEnv):
        i=0
        fEnv = Scope(self.Env)
        a = len(ars)
        A = len(self.ArgNames)
        #print(A)
        #print(self.ArgNames)
        #print(a)
        #print(ars)
        if a!= A:
            raise argumentException(self.name,a,A)
        for arg in ars:
            if self.ArgNames[i] != None:
                fEnv[self.ArgNames[i]] = evaluate(arg,pEnv)
            else:
                print("No matching argument: " + str(self.ArgNames[i]))
            i+=1
        #Exécution de la fonctioon dans un nouvel environnement contenant les valeurs nécessaires (permet les appels récurifs!)
        return evaluate(self.body,fEnv)

class BuiltIn(Fun):
    def __init__(self,fun : Callable[[list,Scope], Any]):
        self.fun = fun
        self.Env = None
    def execute(self,ars,pEnv):
        return self.fun(ars,pEnv)





def evaluate(tree : list, env : Scope):
    if isinstance(tree, Symbol):
        e =env.searchVarScope(tree)
        if e==None:
            raise undefinedSymbolExeption(tree)
        return e[tree]
    elif isinstance(tree,list):
        statement = tree[0]
        stat = evaluate(statement, env)
        if isinstance(stat,Fun):
            return stat.execute(tree[1:],env)
        else:
            ars = [evaluate(elem, env) for elem in tree[1:]]
            try:
                return stat(*ars)
            except TypeError as err:
                message = str(err).split(' ')
                if message[-1] == 'callable':
                    raise unCallableException(stat)
                if message[-1] == 'iterable':
                    raise unIterableException(stat)
                raise argumentException(statement, message[2], int(message[5]))
            except IndexError as err:
                raise indexException(statement)
            except ValueError as err:
                raise castException(ars)
    else:
        return tree
