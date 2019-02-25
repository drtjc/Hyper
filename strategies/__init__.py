from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from inspect import isclass, isabstract
from sys import modules
from warnings import warn
from typing import Tuple, Dict, Type

from strategy import Strategy

strategies_cls: Dict[str, Type[Strategy]] = {}

# load all modules in directory
for _, mod_name, _ in iter_modules([Path(__file__).parent.name]):
    mod = import_module('.' + mod_name, package = __name__)

    # add any subclass of Strategy as an attribute of strategies
    # and to the strategies dictionary attribute
    protocol_found = False
    for i in dir(mod):
        attribute = getattr(mod, i)        

        if isclass(attribute) and issubclass(attribute, Strategy) and not isabstract(attribute):
            class_name = attribute.__name__.split('.')[-1]
            # setattr(modules[__name__], class_name, attribute)
            strategies_cls[class_name] = attribute
            protocol_found = True
            continue

    if not protocol_found:
        warn(f'Strategy module {mod_name} did not contain a Strategy class')


