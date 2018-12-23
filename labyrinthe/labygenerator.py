#! /usr/bin/env python3
# coding: utf-8
"""
librairie that generates a labyrinth in a list
see MOVES for the formating

"""
from pprint import pprint
import os
import json
from random import choice

import numpy

# generer le labirynthe
# faire un objet qui renvoi le labirynth sous forme de tableau
# avec un caractère hexa pour définir la cellule
# utiliser des labirynth prédéfini qui sont sauvegardé en json
# pour l'instant
#
# une classe qui ressort un tableau du labi
#
# classe de génération de labi
# on la défini par la taille x/y et ca nous renvoi un tableau 2 dimensions
# on l'appel labi_gen(x,*y)
# si il n'y a pas de y alors on ressort un labi existatne et sauvegardé
# dans un json


class LabyGenerator():
    """
        Generate a labyrinth
        object = LabyGenerator()
        object.generate(x, y) => return a list
        ["123456",
        "123456"]
        each string is a line (x), each char is a case (y)
        see MOVES for walls position
    """
    # { case : (Up, Right, Down, Left)}
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
        self.path_record = []

    def generate(self, columns, rows):
        """
        generate a x/y laby
        return : laby_code, longuest_path
        """
        # generate empty good dimension table
        cell_type = [1, 1, 1, 1, 0]  # North, Est, South, West, Visisted
        table = numpy.array([[cell_type] * columns] * rows)

        # starting point
        pointer = (0, 0)
        path = []  # record the path
        path.append(pointer)
        go_back = False

        while not self.test_all_visited(table):
            # return non visited possible cases around
            possible_cases = self.get_around_cases(pointer, table)
            if possible_cases == []:
                # go back
                if not go_back:
                    self.path_record.append(path[:])
                    path.pop()
                    # record a ended path
                go_back = True
                pointer = path.pop()
            else:
                if go_back:
                    path.append(pointer)
                go_back = False
                # choose a random direction not visited
                go_to = choice(possible_cases)
                table = self.break_the_wall(pointer, go_to, table)
                pointer = go_to
                path.append(pointer)
            # print(pointer)  #print the path
        self.longuest_path()
        return self.translate_table(table), self.longuest_path()

    def longuest_path(self):
        self.path_record.sort(key=len)
        longuest = self.path_record[-1]
        print(len(longuest))
        print(longuest[-1])
        return longuest

    def get_around_cases(self, pointer, table):
        """
        get the non visited possible cases around the pointer
        """
        row_max, column_max = len(table), len(table[0])
        all_cases = [self.go_north(pointer), self.go_east(pointer),
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

    @staticmethod
    def test_all_visited(table):
        """ test if all cases have been 'visited' """
        for row in table:
            for column in row:
                if column[4] == 0:
                    return False
        return True

    def break_the_wall(self, from_case, to_case, table):
        """make the wall disapear in the 2 visited cases"""
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
        """translate the table into the MOVES code"""
        translate_table = []
        for rows in table:
            translate_row = ""
            for case in rows:
                for case_type in self.MOVES:
                    current_case = case[:4]
                    # need to numpy the tuple to compare same things
                    model_case = numpy.array(self.MOVES[case_type])
                    if numpy.array_equal(current_case, model_case):
                        translate_row += case_type
            translate_table.append(translate_row)
        return translate_table

    @staticmethod
    def coord(pointer):
        """
        invert pointer to be (x,y) coordonates
        """
        return (pointer[1], pointer[0])

    @staticmethod
    def go_north(pointer):
        """return the pointer one case to the north"""
        return (pointer[0], pointer[1] - 1)

    @staticmethod
    def go_east(pointer):
        """return the pointer one case to the east"""
        return (pointer[0] + 1, pointer[1])

    @staticmethod
    def go_south(pointer):
        """return the pointer one case to the south"""
        return (pointer[0], pointer[1] + 1)

    @staticmethod
    def go_west(pointer):
        """return the pointer one case to the west"""
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

    def save_laby(self, number, code, longuest):
        """ save a existing laby in a json file """
        data = self.read_saved_laby()
        data[str(number)] = code, longuest
        file = open(self.laby_data_file, "w")
        json.dump(data, file)

    def read_saved_laby(self):
        """
        read the json file et return a list on laby number with x/y
        """
        with open(self.laby_data_file, "r") as json_data:
            data = json.load(json_data)
        return data


def main():
    """test function"""
    # os.remove("data/laby_data.json")
    laby = LabyGenerator()
    code, longuest = laby.generate(10, 10)
    laby.save_laby(0, code, longuest)
    # print(laby.getout(0))

if __name__ == "__main__":
    main()
