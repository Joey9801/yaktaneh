from interface import (
        Color,
        ask_question,
        give_instruction)

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


