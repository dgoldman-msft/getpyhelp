import argparse
import pydoc
import importlib

def get_help(item, switch):
    """
    Prints methods, functions, dunder methods, or the entire class details for a given item.

    Parameters:
    item (str): The item to look up.
    switch (str): The type of information to display ('show_methods', 'show_functions', 'show_dunders', 'show_class>

    Returns:
    None
    """

    try:
        obj = eval(item)
    except NameError:
        try:
            module_name, _, func_name = item.partition('.')
            module = importlib.import_module(module_name)
            obj = getattr(module, func_name, module)
        except ImportError:
            print(f"Module {item} not found.")
            return

    if switch == "show_methods":
        print(f"Methods for {item}:")
        methods = [method for method in dir(obj) if not method.startswith('__')]
        for i, method in enumerate(methods, 1):
            print(f"{i}. {method} - {getattr(obj, method).__doc__.splitlines()[0]}")
    elif switch == "show_functions":
        print(f"Functions for {item}:")
        functions = [func for func in dir(obj) if not func.startswith('__') and callable(getattr(obj, func))]
        for i, func in enumerate(functions, 1):
            print(f"{i}. {func} - {getattr(obj, func).__doc__.splitlines()[0]}")
    elif switch == "show_dunders":
        print(f"Dunder methods for {item}:")
        dunders = [method for method in dir(obj) if method.startswith('__')]
        for i, dunder in enumerate(dunders, 1):
            print(f"{i}. {dunder} - {getattr(obj, dunder).__doc__.splitlines()[0]}")
    elif switch == "show_class":
        print(f"Class details for {item}:")
        help(obj)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Python help on methods, functions, dunders, or the entire class.")
    parser.add_argument("item", help="The item to look up")
    parser.add_argument("-m", "--show_methods", action="store_true", help="Look up methods")
    parser.add_argument("-f", "--show_functions", action="store_true", help="Look up functions")
    parser.add_argument("-d", "--show_dunders", action="store_true", help="Look up dunder methods")
    parser.add_argument("-c", "--show_class", action="store_true", help="Show the entire class")
    args = parser.parse_args()

    if args.show_methods:
        get_help(args.item, "show_methods")
    elif args.show_functions:
        get_help(args.item, "show_functions")
    elif args.show_dunders:
        get_help(args.item, "show_dunders")
    elif args.show_class:
        get_help(args.item, "show_class")
    else:
        print("Please specify --show_methods, --show_functions, --show_dunders, or --show_class.")
