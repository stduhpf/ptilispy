# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:46:17 2021

@author: Stéphane du Hamel

En python car si j'ai bien compris il va falloir s'y habituer (et c'est plus simple)

Étape d'analyse syntaxique
"""

from Classes import *
from sys import stderr, setrecursionlimit

# https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python


def isfloat(value) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


""""""


def tokenize(chars: str) -> list:
    # séparation des lignes
    rawlines = chars.split("\n")
    lines = []
    for line in rawlines:
        # allocation récursion
        if line.lower().startswith(';recursion_depth'):
            try:
                setrecursionlimit(int(line.split(' ')[1]))
            except:
                print('bad recursion depth', stderr)
        # suppression des commentaires
        lines.append(line.split(";")[0].strip())
    # fusion des lignes
    chars = " ".join(lines)
    # Séparation des différents tokens, en supprimant les espaces
    return list(filter(lambda x: x != "", chars.replace('(', ' ( ').replace(')', ' ) ').replace('"', ' " ').split(' ')))


def read_tokens(tokens: list) -> list:
    token = tokens.pop(0)
    if token == '(':  # si le token est le début d'une liste
        out = []
        while(tokens[0] != ')'):
            out.append(read_tokens(tokens))
            if len(tokens) == 0:
                print("Mismatched parentheses, attempting a fix...", file=stderr)
                tokens = [')']
        tokens.pop(0)
        return out
    elif token == "\"":  # si le token est le début d'une chaîne
        string = ""
        while tokens[0] != "\"":
            mot = tokens.pop(0)
            string += mot + " "
        tokens.pop(0)
        return string[:-1]
    elif token.lstrip("-").isdigit():  # si le token est un entier
        return int(token)
    elif isfloat(token):  # si le token est un rééel
        return float(token)
    else:
        return Symbol(token)  # le token est donc un symbole


def unparse(tree: list) -> str:
    s = "( "
    for elem in tree:
        if isinstance(elem, list):
            s += unparse(elem)
        elif isinstance(elem, Symbol):
            s += str(elem) + " "
        elif isinstance(elem, str):
            s += "\"" + elem + "\" "
        else:
            s += str(elem) + " "
    s += ") "
    return s


def parse(program: str) -> list:
    tree = read_tokens(tokenize(program))
    return tree


def parseFile(fileName: str) -> list:
    return parse(open(fileName, "r").read())
