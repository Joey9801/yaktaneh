import collections

from interface import (
    ask_question,
    give_instruction)


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
