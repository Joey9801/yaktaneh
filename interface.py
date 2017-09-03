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
            print("Try again")

    if expected_type not in (int, str):
        print("Answered: {}".format(result))

    print()
    return result


def give_instructions(instructions):
    max_len = max(map(len, instructions))
    cap = '=' * max_len

    print("    =={}==".format(cap))

    for line in instructions:
        print("    # {line:{width}} #".format(line=line, width=max_len))

    print("    =={}==".format(cap))

def give_instruction(instruction):
    give_instructions([instruction])

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
