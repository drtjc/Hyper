from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

from inspect import isclass
from sys import modules
from strategy import Strategy
from warnings import warn


# load all modules in directory
for _, mod_name, _ in iter_modules([Path(__file__).parent.name]):
    mod = import_module('.' + mod_name, package = __name__)

    # add any subclass of Strategy as an attribute of strategies
    for i in dir(mod):
        attribute = getattr(mod, i)
        if attribute in Strategy.__subclasses__():
            setattr(modules[__name__], attribute.__name__.split('.')[-1], attribute)
            break
    else:
        warn(f'Strategy module {mod_name} did not contain a subclass of Strategy')
