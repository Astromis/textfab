from . import units
from multiprocessing import Pool
from inspect import getmembers, isclass

class Conveyer:
    def __init__(self, config:list):
        self.conveyer = []
        if not isinstance(config, list):
            raise ValueError("The config is not a list")
        for u in config:
            if isinstance(u, str):
                self.conveyer.append(getattr(units, u)())
            elif isinstance(u, tuple):
                self.conveyer.append(getattr(units, u[0])(*u[1:]))
            else:
                raise ValueError("Unknown type of unit")

    def _process(self, text:str):
        for u in self.conveyer:
            #texts = list(map(lambda x: u.process(x), texts))
            text = u.process(text)
        return text
    
    def start(self, texts:list, pool_size=None):
        if pool_size != None:
            with Pool(pool_size) as p:
                return p.map(self._process, texts)
        else:
            return list(map(lambda x: self._process(x), texts))

    def __repr__(self) -> str:
        conv_structure = '->\n'.join([str(x) for x in self.conveyer])
        return f"Conveyer sequence:\n{conv_structure}\n"

def see_available_units():
    for name, obj in getmembers(units, isclass)[3:]:
        print(name, obj.__doc__)