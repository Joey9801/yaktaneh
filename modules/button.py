from interface import (
        ask_question,
        give_instruction,
        Color)

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
