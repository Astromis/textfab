from . import units
from .base import ProcessUnit, ParamChangingProcessUnit, ParamProcessUnit
from multiprocessing import Pool
from omegaconf.dictconfig import DictConfig
from omegaconf.listconfig import ListConfig
from omegaconf import OmegaConf
import importlib
import pandas as pd

class Fabric:
    def __init__(self, config: list):
        self.conveyer = []
        if not (isinstance(config, list) or isinstance(config, ListConfig)):
            raise ValueError("The config is not a list")
        for u in config:
            if isinstance(u, str):
                if "." in u:
                    path = u.split(".")
                    u = getattr(importlib.import_module(".".join(path[:-1])), path[-1])
                    self.conveyer.append(u())
                else:
                    self.conveyer.append(getattr(units, u)())
            elif isinstance(u, dict) or isinstance(u, DictConfig):
                unit_name = list(u.keys())[0]
                arguments = list(u.values())[0]
                if "." in unit_name:
                    path = unit_name.split(".")
                    unit_name = getattr(importlib.import_module(".".join(path[:-1])), path[-1])
                    self.conveyer.append(unit_name(arguments))
                else:
                    self.conveyer.append(getattr(units, unit_name)(arguments))
            elif isinstance(u, ProcessUnit):
                self.conveyer.append(u)
            else:
                raise ValueError("Unknown type of unit")


    def _process(self, text: str):
        for u in self.conveyer:
            text = u.process(text)
        return text

    def __call__(self, texts: str | list | pd.Series, ensure_amount_integrity=True, pool_size=None):
        if isinstance(texts, str):
            texts = [texts]
        elif isinstance(texts, pd.Series):
            texts = texts.to_list()
        else:
            pass
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
    def load_from_config(cls, cfg_path: str):
        conf = OmegaConf.load(cfg_path)
        return cls(conf)
    
    def save_to_config(self, cfg_path: str):
        conf_list = []
        for u in self.conveyer:
            module = u.__class__.__module__
            if module.startswith("textfab."):
                if isinstance(u, ParamChangingProcessUnit) or isinstance(u, ParamProcessUnit):
                    conf_list.append({u.__class__.__name__: u.param})
                else:
                    conf_list.append(u.__class__.__name__)
            else:
                if isinstance(u, ParamChangingProcessUnit) or isinstance(u, ParamProcessUnit):
                    conf_list.append({f"{u.__class__.__module__}.{u.__class__.__name__}": u.param})
                else:
                    conf_list.append(f"{u.__class__.__module__}.{u.__class__.__name__}")
        conf_list = OmegaConf.create(conf_list)
        with open(cfg_path, 'w') as f:
            OmegaConf.save(conf_list, f)