from interface import (
    ask_question,
    give_instruction)


def solve_complicated_wires(bomb):
    def cut():
        give_instruction("Cut the wire")

    def no_cut():
        give_instruction("Do not cut the wire")

    def cut_if(condition):
        if condition:
            return cut
        else:
            return no_cut

    C = cut
    D = no_cut
    S = cut_if(bomb.even_serial_number)
    P = cut_if(bomb.has_parallel_port)
    B = cut_if(bomb.num_batteries >= 2)

    Wire = collections.namedtuple('Cond', ['red', 'blue', 'star', 'led'])
    cases = {
        Wire(False, False, False, False): C,
        Wire(False, False, False, True ): D,
        Wire(False, False, True , False): C,
        Wire(False, False, True , True ): B,
        Wire(False, True , False, False): S,
        Wire(False, True , False, True ): P,
        Wire(False, True , True , False): D,
        Wire(False, True , True , True ): P,
        Wire(True , False, False, False): S,
        Wire(True , False, False, True ): B,
        Wire(True , False, True , False): C,
        Wire(True , False, True , True ): B,
        Wire(True , True , False, False): S,
        Wire(True , True , False, True ): S,
        Wire(True , True , True , False): P,
        Wire(True , True , True , True ): D,
    }

    Color.print_color_reminder()

    while True:
        # @@@ This interface feels too clunky
        red  = ask_question("Doest the wire have red?", bool)
        blue = ask_question("Doest the wire have blue?", bool)
        led  = ask_question("Doest the wire have a lit led?", bool)
        star = ask_question("Doest the wire have a star?", bool)

        wire = Wire(red=red, blue=blue, star=star, led=led)
        cases[wire]()
