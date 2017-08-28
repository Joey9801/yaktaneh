#!/usr/bin/python3


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
