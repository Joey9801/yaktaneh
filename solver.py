#!/usr/bin/python3

import collections

from interface import (
        ask_question,
        give_instruction,
        Color,
        ColorList,
        default_ranged_colorlist)
from bomb import Bomb

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

    give_instruction("Cut the {} wire".format(wire))


def solve_button(bomb):
    Color.print_color_reminder()

    def solve_releasing_held_button():
        give_instruction("Press and hold the button")

        color = ask_question("What color is the lit strip?", Color)

        time_requirement = {
            "U": 4,
            "B": 1,
            "Y": 5,
            "G": 1,
            "R": 1,
            "W": 1,
        }[color.color_code]

        give_instruction(
                "Release the buton when there is a {} in any position".format(time_requirement))

    def immediately_release():
        give_instruction("Press and immediately release the button")

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


def solve_memory(bomb):
    Stage = collections.namedtuple('Stage', ['label', 'position'])

    stage_record = list()

    def literal_label(label):
        def f():
            give_instruction("Press the button with label \"{}\"".format(label))

            pos = ask_question("What was the position of that button?", int)
            stage_record.append(Stage(label=label, position=pos))

        return f

    def literal_position(pos):
        def f():
            position_words = [
                "first",
                "second",
                "third",
                "fourth"
            ]

            give_instruction("Press the button in the {} position".format(
                position_words[pos - 1]))

            label = ask_question("What was the label of that button?", int)
            stage_record.append(Stage(label=label, position=pos))

        return f

    def same_position(stage_index):
        def f():
            pos = stage_record[stage_index - 1].position
            literal_position(pos)()

        return f

    def same_label(stage_index):
        def f():
            label = stage_record[stage_index - 1].label
            literal_label(label)()

        return f

    instructions = [
        {
            1: literal_position(2),
            2: literal_position(2),
            3: literal_position(3),
            4: literal_position(4),
        },
        {
            1: literal_label(4),
            2: same_position(1),
            3: literal_position(1),
            4: same_position(1),
        },
        {
            1: same_label(2),
            2: same_label(1),
            3: literal_position(3),
            4: literal_label(4),
        },
        {
            1: same_position(1),
            2: literal_position(1),
            3: same_position(2),
            4: same_position(2),
        },
        {
            1: same_label(1),
            2: same_label(2),
            3: same_label(4),
            4: same_label(3),
        },
    ]

    try:
        for i in range(5):
            # @@@ No bounds checking done here yet..
            display = ask_question("What is the number on the display?", int)
            instructions[i][display]()
    except KeyboardInterrupt:
        print()
        print("Stopping Memory solver early")
        return

    print("Finished memory game")


def solve_complicated_wires(bomb):
    def cut():
        give_instruction("Cut the wire")

    def no_cut():
        give_instruction("Do not cut the wire")

    def cut_if(condition):
        if condition:
            return cut
        else:
            return no_cut

    C = cut
    D = no_cut
    S = cut_if(bomb.even_serial_number)
    P = cut_if(bomb.has_parallel_port)
    B = cut_if(bomb.num_batteries >= 2)

    Wire = collections.namedtuple('Cond', ['red', 'blue', 'star', 'led'])
    cases = {
        Wire(False, False, False, False): C,
        Wire(False, False, False, True ): D,
        Wire(False, False, True , False): C,
        Wire(False, False, True , True ): B,
        Wire(False, True , False, False): S,
        Wire(False, True , False, True ): P,
        Wire(False, True , True , False): D,
        Wire(False, True , True , True ): P,
        Wire(True , False, False, False): S,
        Wire(True , False, False, True ): B,
        Wire(True , False, True , False): C,
        Wire(True , False, True , True ): B,
        Wire(True , True , False, False): S,
        Wire(True , True , False, True ): S,
        Wire(True , True , True , False): P,
        Wire(True , True , True , True ): D,
    }

    Color.print_color_reminder()

    while True:
        # @@@ This interface feels too clunky
        red  = ask_question("Doest the wire have red?", bool)
        blue = ask_question("Doest the wire have blue?", bool)
        led  = ask_question("Doest the wire have a lit led?", bool)
        star = ask_question("Doest the wire have a star?", bool)

        wire = Wire(red=red, blue=blue, star=star, led=led)
        cases[wire]()


module_solvers = collections.OrderedDict()
module_solvers["Simple Wires"] = solve_simple_wires
module_solvers["Complicated Wires"] = solve_complicated_wires
module_solvers["Button"] = solve_button
module_solvers["Simon Says"] = solve_simon_says
module_solvers["Memory"] = solve_memory


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
        selection = module_names[sel_num]

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
