#!/usr/bin/env python3

from interface import ask_question

from bomb import Bomb
import modules

def solve_bomb():
    module_names = list(modules.solvers.keys())

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
            modules.solvers[selection](bomb)
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
