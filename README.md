# preprocess_conveyer


A tiny library for personal usage. I really tired rewriting all functions each time when I need to preprocess some text. Ridicilous thing is that when I need to preprocess the same text in a different manners it sometimes become hard to traverse where and what I applied for a particular text. 

This code is intended to end up this by orginizing all kind of preprocess functions in understandble conveyrs. The basic idea is to represent all functions as process units and then convert it to manager that can guide the text through the user-defined sequence of units to process the text according to user needs. Moreover the manager has a representation string where the user can see the organization of units. It should be helpful when working in Jypiter Notebook.

# Usage

The available units can be found in `units.py` module. To create a conveyer, you just need to define the sequence of units:
```python
from text_conveyer.manager import Conveyer

config = ["swap_enter_to_space", "remove_punct", "collapse_spaces",]
conv = Conveyer(config)
```

You can specify the pool size when you process the text in order to enable multiprocess execution. Note that conveyer takes a list of texts.
```python
# single process
conv.start(["This text, is\n\n for test"])
# multiprocess
conv.start(["This text, is\n\n for test"], pool_size=5)
```

# Extention

The code is intended to be extendeble in order to collect as more functions as can be. In order to add function, you need to use an abstract class `ProcessUnit`. Also the next requarinments must be met:
* The function must do only one step
* The name function must start with a verb
* The function must have text representation (it's name should be enough)
* The test for the function must be presented 