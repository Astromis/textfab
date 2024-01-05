# Textfab


I really tired rewriting all functions each time when I need to preprocess some text. Ridiculous thing is that when I need to preprocess the same text in different manners it sometimes become hard to traverse where and what I applied for a particular text. Recently, the augmentations has the same effect. 

This code is intended to end up this by organizing all kind of preprocess or augmenting functions in understandable conveyer-like structure. The basic idea is to represent all functions as process units with manager that can guide the text through the user-defined sequence of units to process the text according to user needs. Moreover the manager has a representation string where the user can see the organization of units. It should be helpful when working in Jupiter Notebook.

# Installation

```bash
pip install textfab
```

# Usage

The basic block of the `textfab` is units that does the work. The available units can be found in `units.py` module of by calling the next function:
```python
from textfab.utils import show_available_units
show_available_units()
```

All these units can be organized in `Fabric` class through which the text is processed. To create the `Fabric` object, you just need to define the sequence of units:
```python
from textfab.fabric import Fabric

config = ["swap_enter_to_space", "remove_punct", {"remove_custom_regex": {"regex" : "[A-Z]*"}}, "collapse_spaces"]
fab = Fabric(config)
print(fab)
# >>> Conveyer sequence:
# >>> swap_enter_to_space->
# >>> remove_punct->
# >>> remove_custom_regex:{'regex': '[A-Z]*'}->
# >>> collapse_spaces
```

It also can be the `OmegaConf` config, so it means the `textfab` can work with `Hydra`, which also means that you can log you preprocess steps in tools like DVC or ClearML. 
```python
config = OmegaConf.create(["swap_enter_to_space", "remove_punct", "collapse_spaces"])
fab = Fabric(config)
```

The fabric can be instantiated from config directly:
```python
fab = Fabric.from_config("configs/simple_config.yaml")
```

When the object is ready, simply call it on the text list. You can also specify the pool size when you process the text in order to enable multiprocess execution.
```python
# single process
fab(["This text, is\n\n for test"])
# multiprocess
fab(["This text, is\n\n for test"], pool_size=5)
```

By default, the fab watches on the amount integrity: the amount of output text must be the same as input. It's important when the particular text has the label. You don't want suddenly lose or create some object. Mind that for today it doesn't save you from situations when you unexpectedly remove in one place and add in another, where the shifts are possible. Sometimes you don't need this, for example, when you create a corpus for the language model training, so you can turn it off:
```python
fab(["This text, is\n\n for test"], ensure_amount_integrity=False)
```    

# Extension

The code is intended to be extendable in order to collect as more functions as can be. In order to add function, you need to use an abstract class of the appropriate unit. Also the next requirements must be met:

* The unit must do only one step
* The unit name must start with a verb
* The unit name has a snake case
* The unit must have a docstring
  * The parametrized unit doc must includes the parameters description. 
* The test for the unit must be presented 

There are four types of units with corresponding abstract classes:
* ProcessUnit - unit that consume text and produce the text as string.
* ChangingProcessUnit - these units can modify the objects e,g `str -> List[str]`, `List[str] -> List[List[str]]`, `List[str] -> str`. Generally, they consume anything and produce anything.
* ParamProcessUnit - this is parametrized version of the ProcessUnit. It initialized with parameters as dictionary.
* ParamChangingProcessUnit - this is parametrized version of the ChangingProcessUnit. It initialized with parameters as dictionary.

For easy reading and writing, the unit class implementations are named in the snake case (like_this_writing). By this time they don't play much role in functionality and serve more for the orientation while writing the code.

When you work in the Notebook, you can define a custom unit and use it object in the config. Note that It's important to implement `process` and `__str__` methods:

```python
class custom_unit(ProcessUnit):
        
    def process(self, text):
        return text
    
    def __str__(self):
        return "test"

custom_u = custom_unit()
Fabric(config = ["swap_enter_to_space", "remove_punct", "collapse_spaces", custom_u])
```
The possibility of reading the units from custom scripts is in development.
