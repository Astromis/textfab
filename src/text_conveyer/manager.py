from . import units
from multiprocessing import Pool

class Conveyer:
    def __init__(self, config:list):
        self.conveyer = []
        for u in config:
            self.conveyer.append(getattr(units, u)())

    def _process(self, text:str):
        for u in self.conveyer:
            #texts = list(map(lambda x: u.process(x), texts))
            text = u.process(text)
        return text
    
    def start(self, texts, pool_size=None):
        if pool_size != None:
            with Pool(pool_size) as p:
                return p.map(self._process, texts)
        else:
            return list(map(lambda x: self._process(x), texts))

    def __repr__(self) -> str:
        conv_structure = '->\n'.join([str(x) for x in self.conveyer])
        return f"Conveyer sequence:\n{conv_structure}\n"
