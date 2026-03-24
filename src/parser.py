#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet TL : parser - requires Python version >= 3.10
"""

import sys
from math import factorial
assert sys.version_info >= (3, 10), "Use Python 3.10 or newer !"

import lexer
from definitions import V_T, str_attr_token
import definitions as defs

#####
# Variables internes (à ne pas utiliser directement)

_current_token = V_T.END
_value = None  # attribut du token renvoyé par le lexer

#####
# Fonctions génériques

class ParserError(Exception):
    pass

def unexpected_token(expected):
    return ParserError("Found token '" + str_attr_token(_current_token, _value) + "' but expected " + expected)

def get_current():
    return _current_token

def init_parser(stream):
    global _current_token, _value
    lexer.reinit(stream)
    _current_token, _value = lexer.next_token()
    #print("@ init parser on",  repr(str_attr_token(_current, _value)))  # for DEBUGGING

def consume_token(tok):
    # Vérifie que le prochain token est tok ;
    # si oui, le consomme et renvoie son attribut ; si non, lève une exception
    global _current_token, _value
    if _current_token != tok:
        raise unexpected_token(tok.name)
    if _current_token != V_T.END:
        old = _value
        _current_token, _value = lexer.next_token()
        return old

#Cette fonction recevra une tableau où il y aura ";" et créerra plusieurs tableau avec ceci
#Ex: separe([45,"+",74;12,"*",3,";"])=["45+74","12*3"]

#########################
## Parsing de input et exp

def parse_input():
    #print("@ATTENTION: parser.parse_input à corriger !") # LIGNE A SUPPRIMER
    current=get_current()
    if current in [V_T.NUM,V_T.SUB,V_T.CALC,V_T.OPAR,V_T.END]:
        parse_S()
        return None
    raise ParserError("Input")

def parse_S():
    current=get_current()
    if current in [V_T.SUB,V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_T() #Là
        parse_S()
        return
    elif current==V_T.END:
        return
    else:
        raise ParserError("S")

def parse_T():
    current=get_current()
    if current in [V_T.SUB,V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_E5()#là
        consume_token(V_T.SEQ)
        return
    else:
        raise ParserError("T")
    
def parse_E5():
    current=get_current()
    if current in [V_T.SUB,V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_E4()#là
        parse_X()
        return
    else:
        raise ParserError("E5")

def parse_X():
    current=get_current()
    if current in [V_T.ADD, V_T.SUB]:
        parse_A()
        parse_X()
        return
    elif current in [V_T.SEQ,V_T.CPAR]:
        return
    else:
        raise ParserError("X")

def parse_A():
    current=get_current()
    if current==V_T.ADD:
        consume_token(V_T.ADD)
        parse_E4()
        return
    elif current==V_T.SUB:
        consume_token(V_T.SUB)
        parse_E4()
        return
    else:
        raise ParserError("A")

def parse_E4():
    current=get_current()
    if current in [V_T.SUB,V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_E3()#là
        parse_Y()
        return
    else:
        raise ParserError("E4")

def parse_Y():
    current=get_current()
    if current in [V_T.MUL,V_T.DIV]:
        parse_B()
        parse_Y()
        return
    elif current in [V_T.ADD,V_T.SUB,V_T.SEQ,V_T.CPAR]:
        return
    else:
        raise ParserError("Y")

def parse_B():
    current=get_current()
    if current==V_T.MUL:
        consume_token(V_T.MUL)
        parse_E3()
        return
    elif current==V_T.DIV:
        consume_token(V_T.DIV)
        parse_E3()
        return
    else:
        raise ParserError("B")

def parse_E3():
    current=get_current()
    if current==V_T.SUB:
        consume_token(V_T.SUB)
        parse_E3()
        return
    elif current in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_E2()#là
        return
    else:
        raise ParserError("E3")

def parse_E2():
    current=get_current()
    if current in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_E1()#là
        parse_C()
        return
    else:
        raise ParserError("E2")

def parse_C():
    current=get_current()
    if current==V_T.FACT:
        consume_token(V_T.FACT)
        parse_C()
        return
    elif current in [V_T.MUL,V_T.DIV,V_T.ADD,V_T.SUB,V_T.SEQ,V_T.CPAR]:
        return
    else:
        raise ParserError("C")

def parse_E1():
    current=get_current()
    if current in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        parse_E0()#là #fini
        parse_D()#ici, il reste ";"
        return
    else:
        raise ParserError("E1")

def parse_D():
    current=get_current()
    if current==V_T.POW:
        consume_token(V_T.POW)
        parse_E1()
        return
    elif current in [V_T.FACT,V_T.MUL,V_T.DIV,V_T.ADD,V_T.SUB,V_T.SEQ,V_T.CPAR]:
        return
    else:
        raise ParserError("D")

def parse_E0():
    current=get_current()
    if current==V_T.NUM:
        consume_token(V_T.NUM)
        return
    elif current==V_T.CALC:
        consume_token(V_T.CALC)#là fin , il nous reste ";"
        return
    elif current==V_T.OPAR:
        consume_token(V_T.OPAR)
        parse_E5()
        consume_token(V_T.CPAR)
        return
    else:
        raise ParserError("E0")

    

#####################################
## Fonction principale de la calculatrice
## Appelle l'analyseur grammatical et retourne
## - None sans les attributs
## - la liste des valeurs des calculs avec les attributs

def parse(stream=sys.stdin):
    init_parser(stream)
    l = parse_input()
    print("l=",l)
    consume_token(V_T.END)
    return l

#####################################
## Test depuis la ligne de commande


if __name__ == "__main__":
    print("@ Testing the calculator in infix syntax.")
    result = parse()
    if result is None:
        print("@ Input OK ")
    else:
        print("@ result = ", repr(result))
