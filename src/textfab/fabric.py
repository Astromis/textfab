from . import units
from .base import ProcessUnit
from multiprocessing import Pool
from omegaconf.dictconfig import DictConfig
from omegaconf.listconfig import ListConfig
from omegaconf import OmegaConf


class Fabric:
    def __init__(self, config: list):
        self.conveyer = []
        if not (isinstance(config, list) or isinstance(config, ListConfig)):
            raise ValueError("The config is not a list")
        for u in config:
            if isinstance(u, str):
                self.conveyer.append(getattr(units, u)())
            elif isinstance(u, dict) or isinstance(u, DictConfig):
                unit_name = list(u.keys())[0]
                arguments = list(u.values())[0]
                self.conveyer.append(getattr(units, unit_name)(arguments))
            elif isinstance(u, ProcessUnit):
                self.conveyer.append(u)
            else:
                raise ValueError("Unknown type of unit")

    def _process(self, text: str):
        for u in self.conveyer:
            text = u.process(text)
        return text

    def __call__(self, texts: list, ensure_amount_integrity=True, pool_size=None):
        source_text_amount = len(texts)
        if pool_size is not None:
            with Pool(pool_size) as p:
                processed_texts = p.map(self._process, texts)
        else:
            processed_texts = list(map(lambda x: self._process(x), texts))
        if ensure_amount_integrity and len(processed_texts) != source_text_amount:
            raise ValueError(
                "Text amount integrity  violated: the source text amount doesn't match with processed text."
            )
        return processed_texts

    def __repr__(self) -> str:
        conv_structure = "->\n".join([str(x) for x in self.conveyer])
        return f"Conveyer sequence:\n{conv_structure}\n"

    @classmethod
    def from_config(cls, cfg_path: str):
        conf = OmegaConf.load(cfg_path)
        return cls(conf)
