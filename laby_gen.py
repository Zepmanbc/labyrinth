#! /usr/bin/env python3
# coding: utf-8
import os
import json
"""
generer le labirynth
faire un objet qui renvoi le labirynth sous forme de tableau
avec un caractère hexa pour définir la cellule
utiliser des labirynth prédéfini qui sont sauvegardé en json
pour l'instant

une classe qui ressort un tableau du labi

classe de génération de labi
on la défini par la taille x/y et ca nous renvoi un tableau 2 dimensions
on l'appel labi_gen(x,*y)
si il n'y a pas de y alors on ressort un labi existatne et sauvegardé
dans un json
"""


class Laby_gen():

    # { case : (Up,Right,Down,Left)}
    MOVES = {
        "0": (0, 0, 0, 0),
        "1": (0, 1, 0, 0),
        "2": (0, 0, 1, 0),
        "3": (0, 0, 0, 1),
        "4": (1, 0, 0, 0),
        "5": (1, 1, 0, 0),
        "6": (0, 1, 1, 0),
        "7": (0, 0, 1, 1),
        "8": (1, 0, 0, 1),
        "9": (1, 1, 1, 0),
        "A": (0, 1, 1, 1),
        "B": (1, 0, 1, 1),
        "C": (1, 1, 0, 1),
        "D": (1, 1, 1, 1),
        "E": (0, 1, 0, 1),
        "F": (1, 0, 1, 0)
    }

    def __init__(self):
        self.laby_data_file = "data/laby_data.json"
        if not os.path.exists(self.laby_data_file):
            file = open(self.laby_data_file, "w")
            json.dump({}, file)

    def generate(self, x, y):
        """
        generate a x/y laby
        """
        code = ["8B5", "741", "B6A"]
        return code

    def getout(self, number):
        """
        return the laby code
        """
        data = self.read_saved_laby()
        # faire un test si le numéro existe
        try:
            return data[str(number)]
        except KeyError:
            print("laby number does not exist")
            return False

    def save_laby(self, number, code):
        """
        save a existing laby in a json file
        """
        data = self.read_saved_laby()
        data[number] = code
        file = open(self.laby_data_file, "r+")
        json.dump(data, file)

    def read_saved_laby(self):
        """
        read the json file et return a list on laby number with x/y
        """
        with open(self.laby_data_file, "r") as json_data:
            data = json.load(json_data)
        return data


def main():
    # os.remove("data/laby_data.json")
    laby = Laby_gen()
    code = laby.generate(3, 3)
    laby.save_laby(1, code)
    laby.save_laby(2, code)
    laby.save_laby(3, code)
    print(laby.getout(5))

if __name__ == "__main__":
    main()
