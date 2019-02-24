import pkgutil
import sys
import os


def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        if package_name not in sys.modules:    
            module = importer.find_module(package_name).load_module(package_name)


load_all_modules_from_dir(os.path.dirname(os.path.realpath(__file__)))
