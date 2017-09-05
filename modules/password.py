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

        password_shortlist = set([p for p in passwords if p[pos] in characters])

        if len(password_shortlist) == 0:
            print("Error: there are no passwords which match the given " + 
                  "character set...")

            return

        password_shortlist = password_shortlist.intersection(self.possibilities)

        if len(password_shortlist) == 0:
            print("Error: there are no passwords which match the combination " +
                  " of the given character set + the previously given " +
                  " character sets..")

            return

        self.possibilities = password_shortlist


def solve_password(bomb):
    p = Password()


    print("There are {} possible passwords.".format(len(p.possibilities)))

    for i in range(5):
        p.ask_letter(i)
        print("There are now {} possible passwords.".format(len(p.possibilities)))

        if len(p.possibilities) <= 2:
            break


    if len(p.possibilities) == 1:
        give_instruction("The password is {}".format(
            ", ".join(p.possibilities)))

    elif len(p.possibilities) > 1:
        give_instruction("The password is one of ({})".format(
            ", ".join(p.possibilities)))

