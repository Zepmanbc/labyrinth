#! /usr/bin/env python3
# coding: utf-8

from window import Window
from menu import Menu
from laby_ui import *

"""
generer le labyrinth
faire un objet qui renvoi le labirynth sous forme de tableau
avec un caractère hexa pour définir la cellule
utiliser des labirynth prédéfini qui sont sauvegardé en json
pour l'instant

la partie principale est la gestion du jeu
une representation graphique en utilisant pygame
un personnage qui doit aller d'un bout à l'autre, on le déplace avec
les fleches du clavier
on chronometre le temps qu'il met et le nombre de pas
on montre le nombre de pas mini possible pour faire un high score
qui peut etre enregistrer dans un json
on fait plusieurs niveaux avec une difficulté croissante (taille du labi)

une classe qui ressort un tableau du labi
une classe qui s'occupe de la représentation graphique
une classe qui s'occupe des fondements du jeu

"""


def main():
    window = Window()
    runnin_game = True
    while runnin_game:
        game_choice = Menu(window).run
        if game_choice:
            laby = LabyGenerator()
            laby_data = laby.generate(game_choice[0], game_choice[1])
            game = LabyGUI()
            game.game_loop(laby_data)
            print(laby_data)
        else:
            runnin_game = False

    # je créé une fenetre
    # j'affiche le menu pour choisir la taille souaitée de labyrinthe
    # je balance le labyrinth dans la fenetre
    # je balance le personnage dans la fenetre
    # je balance la barre de dialogue
    # j'écoute les touches
    # si une touche est appuyé je vérifie si le mouvement est possible
    # si le mouvement est possible je change la position du personnage
    # je met a jour la barre de dialogue
    # je rafraichie la fenetre

    # les différents cas
    # le personnage ne peut pas bouger
    # le personnage bouge
    # il ne reste plus de mouvement, il faut indiquer que c'est perdu et
    # revenir au menu
    # le personnage est arrivé à la cible dans le nombre de pas imparti,
    # c'est gagné, et revenir au menu
    # dans ces 2 cas le personnage ne doit plus bouger et il faut appuyer
    # sur entrer pour revenir au menu

if __name__ == "__main__":
    main()
