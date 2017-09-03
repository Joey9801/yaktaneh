from interface import (
        ask_question,
        give_instruction,
        Color,
        default_ranged_colorlist)

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


