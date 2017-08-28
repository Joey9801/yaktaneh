#!/usr/bin/python3

import collections


def ask_question(question, expected_type):
    if expected_type == bool:
        type_hint = "y/n"
    else:
        type_hint = expected_type.__name__

    print()
    print("{} [{}]".format(question, type_hint))

    result = None
    while result == None:
        raw_result = input("> ")
        try:
            if expected_type == bool:
                result = raw_result.lower() in ("y", "yes")
            else:
                result = expected_type(raw_result)
        except (TypeError, ValueError):
            print("Couldn't parse input, try again")

    print("Answered: {}".format(result))
    print()

    return result


class Color():
    color_codes = collections.OrderedDict()
    color_codes["U"] = "Blue"
    color_codes["B"] = "Black"
    color_codes["Y"] = "Yellow"
    color_codes["G"] = "Green"
    color_codes["R"] = "Red"
    color_codes["W"] = "White"

    @classmethod
    def print_color_reminder(cls):
        print("Color codes reminder:")
        for key, value in cls.color_codes.items():
            print("  {} = {}".format(key, value))

    def __init__(self, color_code):
        if color_code.upper() not in Color.color_codes:
            print("'{}' is not a valid color code".format(color_code))
            raise ValueError

        self.color_code = color_code.upper()

    def __eq__(self, other):
        if type(other) == str:
            return self.color_code == other
        elif type(other) == Color:
            return self.color_code == other.color_code
        elif other is None:
            return False
        else:
            raise TypeError

    def __neq__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.color_code)

    def __str__(self):
        return Color.color_codes[self.color_code]

    def __repr__(self):
        return "<Color {}>".format(Color.color_codes[self.color_code])


class ColorList():
    def __init__(self, color_code_str=None, min_elements=None, max_elements=None):
        if color_code_str is None:
            self.colors = list()
            return

        if min_elements is not None and len(color_code_str) < min_elements:
            print("Expected at least {} elements".format(min_elements))
            raise ValueError

        if max_elements is not None and len(color_code_str) > max_elements:
            print("Expected at most {} elements".format(max_elements))
            raise ValueError

        self.colors = list(map(Color, color_code_str))

    def __len__(self):
        return len(self.colors)

    def __contains__(self, x):
        return Color(x) in self.colors

    def __getitem__(self, index):
        if not type(index) == int:
            raise TypeError

        return self.colors[index]

    def __str__(self):
        return "({})".format(", ".join(map(str, self.colors)))

    def __repr__(self):
        return "<ColorList ({})>".format(", ".join(map(str, self.colors)))

    def count(self, color):
        return self.colors.count(color)

    def append(self, new_color):
        if type(new_color) != Color:
            new_color = Color(new_color)

        self.colors.append(new_color)


def default_ranged_colorlist(min_elements, max_elements):
    def f(color_code_str):
        return ColorList(color_code_str, min_elements, max_elements)
    f.__name__ = "ColorList<{}, {}>".format(min_elements, max_elements)
    return f


class Indicators():
    def __init__(self):
        self._known_indicators = dict()

    def __getitem__(self, label):
        """Returns True iff there is a lit indicator with the given label"""
        label = label.upper()
        if label in self._known_indicators:
            return self._known_indicators[label]
        else:
            question = "Is there a lit indicator with label {}?".format(label)
            result = ask_question(question, bool)
            self._known_indicators[label] = result
            return result


class Bomb():
    def __init__(self):
        self._serial_number     = None
        self._num_batteries     = None
        self._has_parallel_port = None

        self.indicators = Indicators()

    @property
    def serial_number(self):
        if self._serial_number is None:
            self._serial_number = ask_question(
                    "What is the serial number?", str)

        return self._serial_number

    @property
    def even_serial_number(self):
        final_char = self.serial_number[-1]
        return final_char in map(str, range(0, 9, 2))

    @property
    def odd_serial_number(self):
        final_char = self.serial_number[-1]
        return final_char in map(str, range(1, 10, 2))

    @property
    def vowel_serial_number(self):
        for vowel in ("a", "e", "i", "o", "u"):
            if vowel in self.serial_number.lower():
                return True

        return False

    @property
    def num_batteries(self):
        if self._num_batteries is None:
            self._num_batteries = ask_question(
                    "How many batteries are there?", int)

        return self._num_batteries

    @property
    def has_parallel_port(self):
        if self._has_parallel_port is None:
            self._has_parallel_port = ask_question(
                    "Does the bomb have a parallel port?", bool)

        return self._has_parallel_port


def solve_simple_wires(bomb):
    Color.print_color_reminder()

    colorlist_type = default_ranged_colorlist(3, 6)
    wires = ask_question("From top to bottom, which wires are there?", colorlist_type)

    wire = "?????"
    if len(wires) == 3:
        if "R" not in wires:
            wire = "second"
        elif wires[-1] == "W":
            wire = "last"
        elif wires.count("U") > 1:
            wire = "last blue"
        else:
            wire = "last"
    elif len(wires) == 4:
        if wires.count("R") > 1 and bomb.odd_serial_number:
            wire = "last red"
        elif wires[-1] == "Y" and "R" not in wires:
            wire = "first"
        elif wires.count("U") == 1:
            wire = "first"
        elif wires.count("Y") > 1:
            wire = "last"
        else:
            wire = "second"
    elif len(wires) == 5:
        if wires[-1] == "B" and bomb.odd_serial_number:
            wire = "fourth"
        elif wires.count("R") and wires.count("Y") > 1:
            wire = "first"
        elif "B" not in wires:
            wire = "second"
        else:
            wire = "first"
    elif len(wires) == 6:
        if "Y" not in wires and bomb.odd_serial_number:
            wire = "third"
        elif wires.count("Y") == 1 and wires.count("W") > 1:
            wire = "fourth"
        elif "R" not in wires:
            wire = "last"
        else:
            wire = "fourth"
    else:
        print("Theres a bug in the simple wires solver")
        print("Don't know what to do")

    print("Cut the {} wire".format(wire))
    print()
    input("Press enter to continue...")


def solve_button(bomb):
    Color.print_color_reminder()

    def solve_releasing_held_button():
        print("Press and hold the button")

        color = ask_question("What color is the lit strip?", Color)

        time_requirement = {
            "U": 4,
            "B": 1,
            "Y": 5,
            "G": 1,
            "R": 1,
            "W": 1,
        }[color.color_code]

        print("Release the buton when there is a {} in any position".format(time_requirement))

    def immediately_release():
        print("Press and immediately release the button")

    color = ask_question("What color is the button?", Color)

    text = ask_question("What does the button say?", str)
    text = text.upper()

    if color == "U" and text == "ABORT":
        solve_releasing_held_button()
    elif bomb.num_batteries > 1 and text == "DETONATE":
        immediately_release()
    elif color == "W" and bomb.indicators["CAR"]:
        solve_releasing_held_button()
    elif bomb.num_batteries > 2 and bomb.indicators["FRK"]:
        immediately_release()
    elif color == "Y":
        solve_releasing_held_button()
    elif color == "R" and text == "HOLD":
        immediately_release()
    else:
        solve_releasing_held_button()


def solve_simon_says(bomb):
    def translate_color(input_color):
        no_vowel = {
            Color("R"): Color("U"),
            Color("U"): Color("R"),
            Color("G"): Color("Y"),
            Color("Y"): Color("G")
        }

        vowel = {
            Color("R"): Color("U"),
            Color("U"): Color("Y"),
            Color("G"): Color("G"),
            Color("Y"): Color("R")
        }

        if bomb.vowel_serial_number:
            return vowel[input_color]
        else:
            return no_vowel[input_color]

    # Make sure the serial number is known before starting
    bomb.serial_number

    Color.print_color_reminder()

    print()
    print("At each step, give the last color flashed")
    print("Press <ctrl>+c to finish the module")

    input_colors = list()
    while True:
        last_color = ask_question(
                "What color was the final flash?", Color)
        if last_color.color_code not in ("R", "U", "G", "Y"):
            print("Don't know how to do simon says for a " +
                  "{} flash".format(last_color.color_code))
            continue

        else:
            input_colors.append(last_color)

        output_colors = list(map(translate_color, input_colors))

        print("Input sequence  : {}".format(
            " - ".join(map(str, input_colors))))
        print("Output sequence : {}".format(
            " - ".join(map(str, output_colors))))


module_solvers = collections.OrderedDict()
module_solvers["Simple Wires"] = solve_simple_wires
module_solvers["Button"] = solve_button
module_solvers["Simon Says"] = solve_simon_says


def solve_bomb():
    module_names = list(module_solvers.keys())

    print("<ctrl>+c to finish the bomb")

    bomb = Bomb()

    while True:
        print("--------------------------------------------------")
        print()
        for i, name in enumerate(module_names):
            print("{}. {}".format(i, name))

        sel_num = ask_question("Which module are we defusing now?", int)
        if sel_num >= 0 and sel_num < len(module_names):
            try:
                selection = module_names[sel_num]
            except KeyboardInterrupt:
                break

            try:
                module_solvers[selection](bomb)
            except KeyboardInterrupt:
                print()
                continue


def print_header():
    print()
    print("      ====================================")
    print("      #    Joe's amazing KTANE expert    #")
    print("      #                                  #")
    print("      #     Manual verification code:    #")
    print("      #               241                #")
    print("      ====================================")
    print()

def main():
    print_header()

    try:
        solve_bomb()
    except KeyboardInterrupt:
        print()
        print("Well done (presumably)")
        print("Exiting...")

    print_header()

if __name__ == "__main__":
    main()
