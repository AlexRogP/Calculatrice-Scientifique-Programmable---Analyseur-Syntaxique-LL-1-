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


#########################
## Parsing de input et exp

def parse_input():
    #print("@ATTENTION: parser.parse_input à corriger !") # LIGNE A SUPPRIMER
    current=get_current()
    if current in [V_T.NUM,V_T.SUB,V_T.CALC,V_T.OPAR,V_T.END]:
        return parse_S(current,[])
    raise ParserError("Input")

def parse_S(current,tab):
    if current in [V_T.SUB,V_T.NUM,V_T.CALC,V_T.OPAR]:
        n1=parse_T(current,tab)#là
        current=get_current()
        n2=parse_S(current,tab+[n1])
        return [n1]+n2
    elif current==V_T.END:
        return []
    else:
        raise ParserError("S")

def parse_T(current,l):
    if current in [V_T.SUB,V_T.NUM,V_T.CALC,V_T.OPAR]:
        n1=parse_E5(current,l)#là
        consume_token(V_T.SEQ)
        return n1
    else:
        raise ParserError("T")
    
def parse_E5(current,l):
    if current in [V_T.SUB,V_T.NUM,V_T.CALC,V_T.OPAR]:
        n1=parse_E4(current,l)#là
        current=get_current()
        n2=parse_X(current,n1,l)
        return n2
    else:
        raise ParserError("E5")

def parse_X(current,n1,l):
    if current in [V_T.ADD, V_T.SUB]:
        n2=parse_A(current,n1,l)#ici
        current=get_current()
        n3=parse_X(current,n2,l)
        return n3
    elif current in [V_T.SEQ,V_T.CPAR]:
        return n1
    else:
        raise ParserError("X")

def parse_A(current,n1,l):
    if current==V_T.ADD:
        consume_token(V_T.ADD)
        current=get_current()
        n2=parse_E4(current,l)#ici current =#9
        return n1+n2
    elif current==V_T.SUB:
        consume_token(V_T.SUB)
        current=get_current()
        n2=parse_E4(current,l)
        return n1-n2
    else:
        raise ParserError("A")

def parse_E4(current,l):
    if current in [V_T.SUB,V_T.NUM,V_T.CALC,V_T.OPAR]:
        n1=parse_E3(current,l)#là #ici
        current=get_current()
        n2=parse_Y(current,n1,l)#ici
        return n2
    else:
        raise ParserError("E4")

def parse_Y(current,n1,l):
    if current in [V_T.MUL,V_T.DIV]:
        n2=parse_B(current,n1,l)
        current=get_current()
        n3=parse_Y(current,n2,l)
        return n3
    elif current in [V_T.ADD,V_T.SUB,V_T.SEQ,V_T.CPAR]:
        return n1
    else:
        raise ParserError("Y")

def parse_B(current,n1,l):
    if current==V_T.MUL:
        consume_token(V_T.MUL)
        current=get_current()
        n2=parse_E3(current,l)
        return n1*n2
    elif current==V_T.DIV:
        consume_token(V_T.DIV)
        current=get_current()
        n2=parse_E3(current,l)
        return n1/n2
    else:
        raise ParserError("B")

def parse_E3(current,l):
    if current==V_T.SUB:
        consume_token(V_T.SUB)
        current=get_current()
        n1=parse_E3(current,l)
        return -n1
    elif current in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        n1=parse_E2(current,l)#là #ici
        return n1
    else:
        raise ParserError("E3")

def parse_E2(current,l):
    if current in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        n1=parse_E1(current,l)#là #ici
        current=get_current()
        n2=parse_C(current,n1,l)
        return n2
    else:
        raise ParserError("E2")

def parse_C(current,n1,l):
    if current==V_T.FACT:
        consume_token(V_T.FACT)
        current=get_current()
        n2=parse_C(current,factorial(n1),l)
        return n2
    elif current in [V_T.MUL,V_T.DIV,V_T.ADD,V_T.SUB,V_T.SEQ,V_T.CPAR]:
        return n1
    else:
        raise ParserError("C")

def parse_E1(current,l):
    if current in [V_T.NUM,V_T.CALC,V_T.OPAR]:
        n1=parse_E0(current,l)#=10 #ici
        current=get_current()
        n2=parse_D(current,n1,l)
        return n2
    else:
        raise ParserError("E1")

def parse_D(current,n1,l):
    if current==V_T.POW:
        consume_token(V_T.POW)
        current=get_current()
        n2=parse_E1(current,l)
        return pow(n1,n2)
    elif current in [V_T.FACT,V_T.MUL,V_T.DIV,V_T.ADD,V_T.SUB,V_T.SEQ,V_T.CPAR]:
        return n1
    else:
        raise ParserError("D")

def parse_E0(current,l):
    if current==V_T.NUM:
        return consume_token(V_T.NUM)# donne 10
    elif current==V_T.CALC:
        i=consume_token(V_T.CALC) #=9
        #print("i=",i,"l=",l) #i=9
        return l[i-1]
    elif current==V_T.OPAR:
        consume_token(V_T.OPAR)
        current=get_current()
        res=parse_E5(current,l)
        consume_token(V_T.CPAR)
        return res
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
