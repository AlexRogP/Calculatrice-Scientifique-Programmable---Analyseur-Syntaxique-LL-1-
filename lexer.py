#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet TL : lexer de la calculatrice
"""

import sys
import enum
import definitions as defs


# Pour lever une erreur, utiliser: raise LexerError("message décrivant l'erreur dans le lexer")
class LexerError(Exception):
    pass


#################################
# Variables et fonctions internes (privées)

# Variables privées : les trois prochains caractères de l'entrée
current_char1 = ''
current_char2 = ''
current_char3 = ''

# Initialisation: on vérifie que EOI n'est pas dans V_C et on initialise les prochains caractères
def init_char():
    global current_char1, current_char2, current_char3
    # Vérification de cohérence: EOI n'est pas dans V_C ni dans SEP
    if defs.EOI in defs.V_C:
        raise LexerError('character ' + repr(defs.EOI) + ' in V_C')
    defs.SEP = {' ', '\n', '\t'} - set(defs.EOI)
    defs.V = set(tuple(defs.V_C) + (defs.EOI,) + tuple(defs.SEP))
    current_char1 = defs.INPUT_STREAM.read(1)
    # print("@", repr(current_char1))  # decomment this line may help debugging
    if current_char1 not in defs.V:
        raise LexerError('Character ' + repr(current_char1) + ' unsupported')
    if current_char1 == defs.EOI:
        current_char2 = defs.EOI
        current_char3 = defs.EOI
    else:
        current_char2 = defs.INPUT_STREAM.read(1)
        # print("@", repr(current_char2))  # decomment this line may help debugging
        if current_char2 not in defs.V:
            raise LexerError('Character ' + repr(current_char2) + ' unsupported')
        if current_char2 == defs.EOI:
            current_char3 = defs.EOI
        else:
            current_char3 = defs.INPUT_STREAM.read(1)
            # print("@", repr(current_char3))  # decomment this line may help debugging
            if current_char3 not in defs.V:
                raise LexerError('Character ' + repr(current_char3) + ' unsupported')

    return

# Accès aux caractères de prévision
def peek_char3():
    global current_char1, current_char2, current_char3
    return (current_char1 + current_char2 + current_char3)

def peek_char1():
    global current_char1
    return current_char1

# Avancée d'un caractère dans l'entrée
def consume_char():
    global current_char1, current_char2, current_char3
    if current_char2 == defs.EOI: # pour ne pas lire au delà du dernier caractère
        current_char1 = defs.EOI
        return
    if current_char3 == defs.EOI: # pour ne pas lire au delà du dernier caractère
        current_char1 = current_char2
        current_char2 = defs.EOI
        return
    next_char = defs.INPUT_STREAM.read(1)
    # print("@", repr(next_char))  # decommenting this line may help debugging
    if next_char in defs.V:
        current_char1 = current_char2
        current_char2 = current_char3
        current_char3 = next_char
        return
    raise LexerError('Character ' + repr(next_char) + ' unsupported')

def expected_digit_error(char):
    return LexerError('Expected a digit, but found ' + repr(char))

def unknown_token_error(char):
    return LexerError('Unknown start of token ' + repr(char))

# Initialisation de l'entrée
def reinit(stream=sys.stdin):
    global input_stream, current_char1, current_char2, current_char3
    assert stream.readable()
    defs.INPUT_STREAM = stream
    current_char1 = ''
    current_char2 = ''
    current_char3 = ''
    init_char()


#################################
## Automates pour les entiers et les flottants


def read_INT_to_EOI():
    # print("@ATTENTION: lexer.read_INT_to_EOI à finir !") # LIGNE A SUPPRIMER
    etat = 0
    next = peek_char1()
    while next != defs.EOI:
        if etat == 0 or etat == 1:
            if next in defs.DIGITS:
                etat = 1
            else:
                etat = 2
        consume_char()
        next = peek_char1()
    return etat==1


def read_FLOAT_to_EOI():
    # print("@ATTENTION: lexer.read_FLOAT_to_EOI à finir !") # LIGNE A SUPPRIMER
    state = 0
    next = peek_char1()
    while next != defs.EOI:
        if state == 0:
            if next == '.': 
                state = 1
            elif next in defs.DIGITS:
                state = 2
            else: 
                state = 4
        elif state == 1:
            if next in defs.DIGITS:
                state = 3
            else:
                state = 4
        elif state == 2:
            if next == '.':
                state = 3
            elif next in defs.DIGITS:
                state = 2 
            else:
                state = 4
        elif state == 3:
            if next in defs.DIGITS:
                state = 3 
            else: 
                state = 4
        consume_char()
        next = peek_char1()
    return (state == 3)


#################################
## Lecture de l'entrée: entiers, nombres, tokens


# Lecture d'un chiffre, puis avancée et renvoi de sa valeur
def read_digit():
    current_char = peek_char1()
    if current_char not in defs.DIGITS:
        raise expected_digit_error(current_char)
    value = eval(current_char)
    consume_char()
    return value


# Lecture d'un entier en renvoyant sa valeur
def read_INT():
    # print("@ATTENTION: lexer.read_INT à finir !") # LIGNE A SUPPRIMER
    next = peek_char1()
    valeur = 0
    if next not in defs.DIGITS:
        return None
    while next in defs.DIGITS:
        digit = read_digit()
        # print(digit*10)
        valeur = valeur*10 + digit
        next = peek_char1()
    return valeur;


global int_value
global exp_value
global sign_value

def automate_num(etat, input):
    flottant_sym = ['e', 'E']
    match etat:
        case 0:
            if input in defs.DIGITS:
                etat = 3
            elif next == '.':
                etat = 1
            else:
                etat = 7
        case 1:
            if next in defs.DIGITS:
                etat = 2
            else:
                etat = 7
        case 2:
            if next in defs.DIGITS:
                etat = 2
            elif next in flottant_sym:
                etat = 4
            else:
                etat = 7
        case 3:
            if next in defs.DIGITS:
                etat = 3
            elif next in flottant_sym:
                etat = 4
            elif next == '.':
                etat = 2
            else: 
                etat = 7
        case 4:
            if next in defs.DIGITS:
                etat = 6
            elif next in ['+','-']:
                etat = 5
            else:
                etat = 7
        case 5:
            if next in defs.DIGITS:
                etat = 6
            else:
                etat = 7
        case 6:
            if next in defs.DIGITS:
                etat = 6
            else:
                etat = 7
    print(f"etat = {etat}")
    return etat



# Lecture d'un nombre en renvoyant sa valeur
def read_NUM():
    etat = 0
    next = peek_char1()
    mantisse = 0
    flottant_sym = ['e', 'E']
    i_flott = -1
    pow = 0
    sign = 1
    while True:
        match etat:
            case 0:
                if next in defs.DIGITS:
                    etat = 3
                    mantisse = mantisse*10 + read_digit()
                elif next == '.':
                    etat = 1
                    consume_char()
                else:
                    return None
            case 1:
                if next in defs.DIGITS:
                    etat = 2
                    mantisse = mantisse + read_digit()*10**i_flott
                    i_flott -= 1
                else:
                    return None
            case 2:
                if next in defs.DIGITS:
                    etat = 2
                    mantisse = mantisse + read_digit()*10**i_flott
                    i_flott -= 1
                elif next in flottant_sym:
                    etat = 4
                    consume_char()
                else:
                    return mantisse
            case 3:
                if next in defs.DIGITS:
                    etat = 3
                    mantisse = mantisse * 10 + read_digit()
                elif next in flottant_sym:
                    etat = 4
                    consume_char()
                elif next == '.':
                    etat = 2
                    consume_char()
                else: 
                    return mantisse
            case 4:
                if next in defs.DIGITS:
                    etat = 6
                    pow = pow * 10 + read_digit()
                elif next in ['+','-']:
                    etat = 5
                    if next == '-':
                        sign = -1
                    consume_char()
                else:
                    return mantisse
            case 5:
                if next in defs.DIGITS:
                    etat = 6
                    pow = pow*10 + read_digit()
                else:
                    return mantisse
            case 6:
                if next in defs.DIGITS:
                    etat = 6
                    pow = pow*10 + read_digit()
                else:
                    return mantisse*10**(pow*sign)
        next = peek_char1()
    # return mantisse*10**(pow*sign);
    return None


# Parse un lexème (sans séparateurs) de l'entrée et renvoie son token.
# Cela consomme tous les caractères du lexème lu.
def read_token_after_separators():
    # print("@ATTENTION: lexer.read_token_after_separators à finir !") # LIGNE A SUPPRIMER
    # n = peek_char1()
    # tokens = []
    # while n != defs.EOI:
    #     if n in defs.DIGITS:
    #         num = read_NUM()
    #         if num != None:
    #             tokens.append((defs.V_T.NUM, num))
    #     consume_char()
    #     n = peek_char1()
    #     print(num)
    # # return (defs.V_T.END, None) # par défaut, on renvoie la fin de l'entrée
    # return tokens
    num = read_NUM()
    if num != None:
        return (defs.V_T.NUM, num)
    else:
        n = peek_char1()
        consume_char()
        if n == '#':
            num = read_NUM()
            return (defs.V_T.CALC, num)
        elif n == '+':
             return (defs.V_T.ADD, None)
        elif n == '-':
            return (defs.V_T.SUB, None)
        elif n == '*':
            return (defs.V_T.MUL, None)
        elif n == '/':
            return (defs.V_T.DIV, None)
        elif n == '^':
            return (defs.V_T.POW, None)
        elif n == '!':
            return (defs.V_T.FACT, None)
        elif n == '(':
            return (defs.V_T.OPAR, None)
        elif n == ')':
            return (defs.V_T.CPAR, None)
        elif n == ';':
            return (defs.V_T.SEQ, None)
    return (defs.V_T.END, None)

# Donne le prochain token de l'entrée, en sautant les séparateurs éventuels en tête
# et en consommant les caractères du lexème reconnu.
def next_token():
    # print("@ATTENTION: lexer.next_token à finir !") # LIGNE A SUPPRIMER
    n = peek_char1()
    while n in defs.SEP:
        consume_char()
        n = peek_char1()
    return read_token_after_separators()


#################################
## Fonctions de tests

def test_INT_to_EOI():
    print("@ Testing read_INT_to_EOI. Type a word to recognize.")
    reinit()
    if read_INT_to_EOI():
        print("Recognized")
    else:
        print("Not recognized")

def test_FLOAT_to_EOI():
    print("@ Testing read_FLOAT_to_EOI. Type a word to recognize.")
    reinit()
    if read_FLOAT_to_EOI():
        print("Recognized")
    else:
        print("Not recognized")

def test_lexer():
    print("@ Testing the lexer. Just type tokens and separators on one line")
    reinit()
    token, value = next_token()
    while token != defs.V_T.END:
        print("@", defs.str_attr_token(token, value))
        token, value = next_token()

if __name__ == "__main__":
    ## Choisir une seule ligne à décommenter
    # test_INT_to_EOI()
    test_FLOAT_to_EOI()
    # test_lexer()
