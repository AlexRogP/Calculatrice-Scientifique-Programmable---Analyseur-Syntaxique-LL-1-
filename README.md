Calculatrice Scientifique : Analyseur Syntaxique LL(1)
Ce projet, réalisé durant le premier semestre à l'ENSIMAG, consiste en la conception et 
l'implémentation d'une chaîne de compilation complète pour une calculatrice capable de 
traiter des expressions arithmétiques complexes.

FonctionnalitésCalculs avancés : Support des nombres entiers, flottants et de la notation scientifique.

Opérateurs : Addition, soustraction, multiplication, division, puissances et factorielles.

Mémoire de calcul : Possibilité de réutiliser les résultats des calculs précédents via la syntaxe #i.

Gestion d'erreurs : Implémentation d'un mécanisme de rattrapage (error recovery) pour poursuivre l'analyse 
malgré des erreurs de syntaxe.

🛠 Architecture Technique
Le projet est divisé en deux phases majeures qui forment un analyseur syntaxique

1. Analyse Lexicale (Lexer)L'analyseur lexical transforme le flux de caractères en une suite de tokens:
-Utilisation d'automates finis déterministes pour la reconnaissance des nombres.
-Gestion d'un lookahead de 3 caractères (peek_char3) pour résoudre les ambiguïtés de segmentation 
(choix du lexème le plus long).

2. Analyse Grammaticale (Parser)L'analyseur grammatical vérifie la structure de la suite de tokens selon une grammaire 
hors-contexte.
Grammaire LL(1) : Transformation d'une grammaire ambiguë pour lever les priorités et les associativités des opérateurs.
Calcul d'attributs : L'évaluation mathématique est effectuée de manière récursive pendant l'analyse grammaticale.

📁 Structure du Projet

lexer.py : Logique des automates et segmentation du flux d'entrée.

parser.py : Analyseur syntaxique descendant et gestion de la grammaire.

calc.py : Extension du parser intégrant le calcul effectif des valeurs.

definitions.py : Définition des tokens et des vocabulaires terminaux.

rattrapage.py : Module dédié à la résilience face aux erreurs de saisie.

🧪 Tests
Le projet inclut une suite de tests unitaires pour valider chaque étape :
python3 tests/test_lexer.py  => Validation de l'automate
python3 tests/test_parser.py => Validation de la syntaxe
python3 tests/test_calc.py   => Validation des résultats mathématiques

Explication des fichiers complémentaires

test.txt :
Ce fichier regroupe des tests supplémentaires pour le lexer, en plus de ceux fournis par le professeur.

test_rattrapage :
Ce fichier rassemble tous les tests effectués sur rattrapage.py. 
On y trouve aussi bien les tests réussis que ceux qui ont échoué.