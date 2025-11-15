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
    #print("@ATTENTION: lexer.read_INT_to_EOI à finir !") # LIGNE A SUPPRIMER
    x=peek_char1()
    print("ici x=",x)
    number=['0','1','2','3','4','5','6','7','8','9']
    while x!= defs.EOI :
        if x in number:
            consume_char()
            x=peek_char1()
        else:
            return False
    return True


def read_FLOAT_to_EOI():
    #print("@ATTENTION: lexer.read_FLOAT_to_EOI à finir !") # LIGNE A SUPPRIMER
    c=peek_char1()
    number=['0','1','2','3','4','5','6','7','8','9']
    # Je fais le cas où l'on a un nombre comme .5
    if c== '.':
        consume_char()
        c=peek_char1()
        while c!=defs.EOI:
            if c in number:
                consume_char()
                c=peek_char1()
            else:
                return False
        return True
    #Je créer le cas où on a un chiffre comme 4.5
    elif c in number:
        consume_char()
        c=peek_char1()
        while c!='.':
            if c in number:
                consume_char()
                c=peek_char1()
            else:
                return False
        consume_char()
        c=peek_char1()
        while c!=defs.EOI:
            if c in number:
                consume_char()
                c=peek_char1()
            else:
                return False
        return True
    else:
        return False



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
    #print("@ATTENTION: lexer.read_INT à finir !") # LIGNE A SUPPRIMER
    c=peek_char1()
    number=['0','1','2','3','4','5','6','7','8','9']
    nombre=""
    while c in number:
        nombre+=c
        consume_char()
        c=peek_char1()
    return int(nombre)
    
    


global int_value
global exp_value
global sign_value


#Cette fonction prends les 3 éléments donné par peek_char3() et avance de 3
#Elle est surtout là pour eviter de réécrire du code
def recup_car():
    s=peek_char3()
    c=s[0]
    d=s[1]
    e=s[2]
    consume_char()
    consume_char()
    consume_char()
    return c,d,e

#Sous partie de A
def B(dernier_car,mot):
    interger=['0','1','2','3','4','5','6','7','8','9']
    pointfloat=['.','0','1','2','3','4','5','6','7','8','9']
    exposant=['e','E','+','-']
    mot = mot[1:]               #Q4
    c=mot[0]
    print("mot=",mot)
    if c in interger:               #Q6
        while c!=dernier_car:
            if c in interger:
                mot = mot[1:] 
                c=mot[0]
            else:
                return False
        if c=='.':
            return False
        else:
            return True
    elif c=='+' or c=='-':       #Q5
        if c==dernier_car:
            return False
        mot = mot[1:] 
        c=mot[0]
        if c in interger:       #Q6
            while c!=dernier_car:
                if c in interger:
                    mot = mot[1:] 
                    c=mot[0]
                else:
                    return False
            return True
    else:
        return False
#Sous partie de la fonction read_NUMBER_to_EOI
def A(dernier_car,mot):
    interger=['0','1','2','3','4','5','6','7','8','9']
    pointfloat=['.','0','1','2','3','4','5','6','7','8','9']
    exposant=['e','E','+','-']
    if mot==dernier_car:
        return False
    mot = mot[1:]  
    c=mot[0]
    if c=='.':
        return False
    while c!=dernier_car and c!='E' and c!='e': #Q2
        if c in interger:
            mot = mot[1:]  
            c=mot[0]
        else:
            return False
    if c==dernier_car:
        if c in pointfloat:
            return True
        else:
            return False
    return B(dernier_car,mot)
#Fonction qui implemte l'automate de number pour voir si un mot est accepté 
#L'automate étant long il sera divisé en sous partie 
def read_NUMBER_to_EOI(mot):
    interger=['0','1','2','3','4','5','6','7','8','9']
    pointfloat=['.','0','1','2','3','4','5','6','7','8','9']
    exposant=['e','E','+','-']
    c=mot[0]
    if c not in pointfloat:
        return False
    dernier_car=mot[-1]
    if c== '.':                     #Q1
        return A(dernier_car,mot)
    else:
        if c==dernier_car: #Cas ou ou l'entré est de longueur 1
            return True
        mot = mot[1:] 
        c=mot[0]
        while c!= dernier_car and c!='E' and c!='e' and c!='.':
            if c in interger:
                mot = mot[1:] 
                c=mot[0]
            else:
                return False
        if c==dernier_car:
            if c in pointfloat and len(mot)==1:
                return True
            else:
                return False
        elif c=='.':
            return A(dernier_car,mot)
        else:
            return B(dernier_car,mot)

#Cette fonction prends un chaine de caractères repreenteant un nombre et le calcul
def calcul(mot):
    mot1=""
    mot2=""
    deja_passe=False
    if 'E' in mot or 'e' in mot:
        for x in mot:
            if x!='E'and  x!='e' and deja_passe==False:
                mot1+=x
            if x!='E' and x!='e' and deja_passe==True:
                mot2+=x
            if x=='E' or x=='e':
                deja_passe=True
        if '.' in mot1:
            mot1=float(mot1)
        else:
            mot1=int(mot1)
        if '.' in mot2:
            mot2=float(mot2)
        else:
            mot2=int(mot2)
        return mot1*(10**(mot2))
    else:
        if '.' in mot:
            return float(mot)
        else:
            return int(mot)


# Lecture d'un nombre en renvoyant sa valeur
def read_NUM():
    #print("@ATTENTION: lexer.read_NUM à finir !") # LIGNE A SUPPRIMER
    # Number = (integer ∪ pointfloat) (exponent ∪ {ε})
    #J'utilise la fonc read_NUMBER_to_EOI pour validé ou pas un mot 

    #Je vais récupérér l'ensemble de l'entré
    mot_finale=""
    c=peek_char1()
    while c!=defs.EOI:
        mot_finale+=c
        consume_char() 
        c=peek_char1()
    mot_finale+=c
    print("mot_finale=",mot_finale)

    #Je pars de la fin du mot, si il n'est pas accepté alors je retire le dernier caractère et je le reteste
    #Et ainsi de suite jusqu'à trouver le mot le plus long qui est accepté
    while mot_finale!="" and not read_NUMBER_to_EOI(mot_finale):
        mot_finale=mot_finale[:-1]
    if mot_finale=="":
        print("Aucun préfixe accepté")
        return
    print("mot accpeté=",mot_finale)
    print("resultat=", calcul(mot_finale))
    return 

    
    
    


        

        
    


# Parse un lexème (sans séparateurs) de l'entrée et renvoie son token.
# Cela consomme tous les caractères du lexème lu.
def read_token_after_separators():
    print("@ATTENTION: lexer.read_token_after_separators à finir !") # LIGNE A SUPPRIMER
    return (defs.V_T.END, None) # par défaut, on renvoie la fin de l'entrée


# Donne le prochain token de l'entrée, en sautant les séparateurs éventuels en tête
# et en consommant les caractères du lexème reconnu.
def next_token():
    print("@ATTENTION: lexer.next_token à finir !") # LIGNE A SUPPRIMER
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
    #test_INT_to_EOI()
    #test_FLOAT_to_EOI()
    test_lexer()
