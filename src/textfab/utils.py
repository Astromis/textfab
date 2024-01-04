from inspect import getmembers, isclass
from . import units

def see_available_units():
    for name, obj in getmembers(units, isclass)[3:]:
        print(name, obj.__doc__)