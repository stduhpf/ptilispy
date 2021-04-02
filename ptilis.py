# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:46:17 2021

@author: Stéphane du Hamel

En python car si j'ai bien compris il va falloir s'y habituer (et c'est plus simple)

Fichier principal, les autres sont directement importés
"""


from Parser import *

from env.DefaultEnvs import *

from Interpreter import *


def parseAndRunFile(filePath: str, args: list = [], env: Scope = default_environement(), repl: bool = False):
    parseTree = parseFile(filePath)
    if repl:
        run(parseTree, args, env)
        return REPL(Scope(env))
    return run(parseTree, [[Symbol('list'), *args]], env)


def parseAndRunString(program: str, args: list = [], env: Scope = default_environement()):
    parseTree = parse(program)
    # print(unparse(parseTree))
    return run(parseTree, [[Symbol('list'), *args]], env)


def REPL(env: Scope = default_environement(), ans=Symbol('Nil'), libs: list = [], libFiles: list = []):
    A = Symbol('ans')
    env.searchVarScope(A)[A] = ans
    for lib in libs:
        libname = Symbol(lib)
        env = loadEnv(libname, env)
    for lib in libFiles:
        libname = str(lib)
        env = loadEnv('file', env, [libname, libname])
    input1 = ''
    while True:
        input1 = ''
        while input1 == '':
            input1 = input('<<<\t: ')
        if input1.lower() == 'quit':
            break
        input1.strip()
        complete = False
        if input1[0] != '(':
            input1 = '('+input1
            complete = True
        if input1[-1] != ')':
            input1 = input1+')'
            complete = True
        if complete:
            print("Missing outer parenthesis, guessing: " + input1 + "\n", stderr)
        try:
            ret = parseAndRunString(input1, env=env)
            env[A] = ret
            print('>>>\t: ' + str(ret))
        except runException as ex:
            print(ex.message + '\n', stderr)


def run(program: list, args: list = [list], env: Scope = default_environement()):
    ret = evaluate(program, env)
    mainfun = env.get('main')
    if (mainfun != None):
        if(isinstance(mainfun, Fun)):
            return mainfun.execute(args, env)
    return ret

################################################################
### -----------------------  Tests  ------------------------ ###


if __name__ == "__main__":
    REPL()
