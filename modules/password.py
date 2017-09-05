from interface import (
        ask_question,
        give_instruction)

passwords = [
    "about", "after", "again", "below", "could",
    "every", "first", "found", "great", "house",
    "large", "learn", "never", "other", "place",
    "plant", "point", "right", "small", "sound",
    "spell", "still", "study", "their", "there",
    "these", "thing", "think", "three", "water",
    "where", "which", "world", "would", "write"
]

class Password():
    def __init__(self):
        self.possibilities = set(passwords)

    def ask_letter(self, pos):
        characters = ask_question(
                "What letters can go in position {}?".format(pos + 1), str)
        characters = characters.lower()

        password_shortlist = set([p for p in passwords if p[pos] in characters])

        if len(password_shortlist) == 0:
            print("Error: there are no passwords which match the given " + 
                  "character set...")

            return False

        password_shortlist = password_shortlist.intersection(self.possibilities)

        if len(password_shortlist) == 0:
            print("Error: there are no passwords which match the combination " +
                  " of the given character set + the previously given " +
                  " character sets..")

            return False

        self.possibilities = password_shortlist
        return True

    def possibilities_str(self):
        if len(self.possibilities) == 0:
            return "There are no solutions"
        elif len(self.possibilities) == 1:
            only_remaining = next(iter(self.possibilities))
            return "The password is \"{}\"".format(only_remaining)
        else:
            options_string = ", ".join(map(lambda x: "\"{}\"".format(x),
                self.possibilities))
            return "The password is one of ({})".format(options_string)

def solve_password(bomb):
    p = Password()

    print("There are {} possible passwords.".format(len(p.possibilities)))
    print()
    print("When entering characters:")
    print("   - Repeats are fine")
    print("   - Upper/lowercase doesn't matter")
    print()
    print("Press <ctrl>+c at any point to give up")

    for i in range(5):
        while not p.ask_letter(i):
            pass

        print("{} possible solution(s) remain".format(len(p.possibilities)))

        if len(p.possibilities) <= 2:
            break

    print()
    give_instruction(p.possibilities_str())
    print()

    input("Press enter to continue..")
