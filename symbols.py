#!venv/bin/python3

import math
import os.path

from PIL import Image
import numpy as np

from interface import ask_question, give_instructions

def map_float_to_greyscale(value):
    chars = list("W&%=^~:-. ")
    value = int(value * (len(chars) - 0))
    if value == len(chars):
        value = value - 1

    return chars[value]

class Symbol():
    # Normal sort of aspect ratio for a monospaced font:
    # Our 'pixels' are not square, so if we treat them as square we'll get
    # a squashed image.
    char_aspect = 7 / 4

    def __init__(self, filename, name, print_size=32):
        self.filename = os.path.join("symbols/", filename)
        self.name = name
        self._print_size = print_size

        self.img = None

    def __eq__(self, other):
        if type(other) != Symbol:
            return False

        return self.name == other.name and self.filename == other.filename

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name
        return hash(self.name)

    def __repr__(self):
        return "<Symbol '{}'>".format(self.name)

    @property
    def print_size(self):
        return self._print_size

    @print_size.setter
    def print_size(self, new_size):
        # Modifying the print size means the image will have to be reloaded
        if self.img is not None:
            self.img = None

        self._print_size = new_size

    def load_img(self):
        img = Image.open(self.filename)

        # Trim whitespace
        img = img.crop(img.getbbox())

        # Resize the image for ascii pixels
        lines = self.print_size
        columns = (lines / img.size[1]) * img.size[0] * self.char_aspect
        columns = round(columns)
        scaled_size = (columns, lines)
        img = img.resize(scaled_size)

        # Currently each pixel is an array of component values. Sum these for a
        # basic grayscale conversion.
        img = np.sum(img, axis=2)

        # Subtract the minimum value and divide by the maximum value - each pixel
        # is then in the range [0, 1]
        # Then invert the image
        img -= img.min()
        img = 1 - (img / img.max())

        self.img = img
        self.num_rows = lines
        self.num_columns = columns

    def print_ascii(self, padding=5):
        if self.img is None:
            self.load_img()

        for row in self.img:
            print(" " * padding, end="")
            for pixel in row:
                print("{}".format(map_float_to_greyscale(pixel)), end="")

            print()

        print()
        print("{:{padding}}{name:^{width}}".format("", padding=padding,
            width=self.num_columns, name=self.name))
        print()

class SymbolList():
    symbols = [
        Symbol("14-ae.png",           "ae"),
        Symbol("13-at.png",           "AT"),
        Symbol("28-balloon.png",      "Balloon"),
        Symbol("31-bt.png",           "bT"),
        Symbol("1-copyright.png",     "Copyright"),
        Symbol("26-cursive.png",      "Cursive"),
        Symbol("5-doublek.png",       "Double K"),
        Symbol("19-dragon.png",       "Dragon"),
        Symbol("16-euro.png",         "Euro"),
        Symbol("2-filledstar.png",    "Filled Star"),
        Symbol("3-hollowstar.png",    "Hollow Star"),
        Symbol("9-hookn.png",         "Hook N"),
        Symbol("23-leftc.png",        "Left C"),
        Symbol("15-meltedthree.png",  "Melted 3"),
        Symbol("18-nwithhat.png",     "N with hat"),
        Symbol("6-omega.png",         "Omega"),
        Symbol("21-paragraph.png",    "Paragraph"),
        Symbol("24-pitchfork.png",    "Pitchfork"),
        Symbol("8-pumpkin.png",       "Pumpkin"),
        Symbol("20-questionmark.png", "Question Mark"),
        Symbol("22-rightc.png",       "Right C"),
        Symbol("11-six.png",          "Six"),
        Symbol("4-smileyface.png",    "Smiley Face"),
        Symbol("7-squidknife.png",    "Squidknife"),
        Symbol("12-squigglyn.png",    "Squiggly N"),
        Symbol("27-tracks.png",       "Tracks"),
        Symbol("30-upsidedowny.png",  "Upside-down Y"),
    ]

    max_symbol_name_len = max(map(lambda x: len(x.name), symbols))

    @classmethod
    def print_symbol_options(cls, num_columns=3):
        num_rows = math.ceil(len(cls.symbols) / num_columns)

        indicies = range(len(cls.symbols))
        rows = [indicies[i::num_rows] for i in range(num_rows)]
        for row in rows:
            for i in row:
                print("{index:2}. {name:{name_width}}  ".format(
                        index=i + 1,
                        name_width=cls.max_symbol_name_len,
                        name=cls.symbols[i].name),
                    end="")

            print()

    @classmethod
    def render_symbol(cls, index=None):
        if index is None:
            cls.print_symbol_options()
            index = ask_question("Which symbol would you like to render?", int)
            index = index - 1

        cls.symbols[index].print_ascii()

    @classmethod
    def ask_symbol(cls, index):
        index = int(index) - 1
        cls.render_symbol(index)
        confirmed = ask_question("Is this the one you meant?", bool)

        if not confirmed:
            # Make the user try again
            cls.print_symbol_options()
            print()
            raise ValueError

        else:
            return cls.symbols[index]

    @classmethod
    def get_symbol(cls, name):
        for sym in cls.symbols:
            if sym.name == name:
                return sym

        return None
