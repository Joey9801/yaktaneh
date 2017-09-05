import collections

from .simple_wires import solve_simple_wires
from .complicated_wires import solve_complicated_wires
from .symbols import solve_symbols
from .button import solve_button
from .simon_says import solve_simon_says
from .memory import solve_memory
from .password import solve_password


solvers = collections.OrderedDict()
solvers["Simple Wires"] = solve_simple_wires
solvers["Complicated Wires"] = solve_complicated_wires
solvers["Keypad Symbols"] = solve_symbols
solvers["Button"] = solve_button
solvers["Simon says"] = solve_simon_says
solvers["Memory"] = solve_memory
solvers["Password"] = solve_password
