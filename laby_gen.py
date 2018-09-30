#! /usr/bin/env python3
# coding: utf-8
import os
import json
from random import choice

import numpy

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

    def generate(self, columns, rows):
        """
        generate a x/y laby
        """
        # generate empty good dimension table
        cell_type = [1, 1, 1, 1, 0]  # North, Est, South, West, Visisted
        table = numpy.array([[cell_type] * columns] * rows)

        # starting point
        pointer = (0, 0)
        path = []  # record the path
        path.append(pointer)

        while not self.test_all_visited(table):
            # return non visited possible cases around
            possible_cases = self.get_around_cases(pointer, table)
            if possible_cases == []:
                # go back
                pointer = path.pop()
            else:
                # choose a random direction not visited
                go_to = choice(possible_cases)
                table = self.break_the_wall(pointer, go_to, table)
                pointer = go_to
                path.append(pointer)
            print(pointer)
        return self.translate_table(table)

    def get_around_cases(self, pointer, table):
        """
        get the non visited possible cases around the pointer
        """
        row_max, column_max = len(table), len(table[0])
        all_cases = [self.go_north(pointer), self.go_est(pointer),
                     self.go_south(pointer), self.go_west(pointer)]
        cases = []
        for case in all_cases:
            # stay in the table
            if case[0] in range(0, column_max) and \
               case[1] in range(0, row_max):
                # test if visited or not
                if table[case[1], case[0]][4] == 0:
                    cases.append(case)
        return cases

    def test_all_visited(self, table):
        for row in table:
            for column in row:
                if column[4] == 0:
                    return False
        return True

    def break_the_wall(self, from_case, to_case, table):
        """
        make the wall disapear in the 2 visited cases
        """
        # to the North
        if from_case[1] - to_case[1] == -1:
            table[(self.coord(from_case))][2] = 0
            table[(self.coord(to_case))][0] = 0
        # to the Est
        elif from_case[0] - to_case[0] == -1:
            table[(self.coord(from_case))][1] = 0
            table[(self.coord(to_case))][3] = 0
        # to the South
        elif from_case[1] - to_case[1] == 1:
            table[(self.coord(from_case))][0] = 0
            table[(self.coord(to_case))][2] = 0
        # to the West
        elif from_case[0] - to_case[0] == 1:
            table[(self.coord(from_case))][3] = 0
            table[(self.coord(to_case))][1] = 0
        # say that the destination has been visited
        table[(self.coord(to_case))][4] = 1
        table[(self.coord(from_case))][4] = 1
        return table

    def translate_table(self, table):
        translate_table = []
        x_pos, y_pos = 0, 0
        for rows in table:
            translate_row = ""
            for case in rows:
                for case_type in self.MOVES.keys():
                    current_case = case[:4]
                    # need to numpy the tuple to compare same things
                    model_case = numpy.array(self.MOVES[case_type])
                    if numpy.array_equal(current_case, model_case):
                        translate_row += case_type
            translate_table.append(translate_row)
        return translate_table

    def coord(self, pointer):
        """
        invert pointer to be (x,y) coordonates
        """
        return (pointer[1], pointer[0])

    def go_north(self, pointer):
        return (pointer[0], pointer[1] - 1)

    def go_est(self, pointer):
        return (pointer[0] + 1, pointer[1])

    def go_south(self, pointer):
        return (pointer[0], pointer[1] + 1)

    def go_west(self, pointer):
        return (pointer[0] - 1, pointer[1])

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
    code = laby.generate(20, 15)
    laby.save_laby(4, code)
    print(laby.getout(4))

if __name__ == "__main__":
    main()
