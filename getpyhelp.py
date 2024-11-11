import argparse
import importlib
from colorama import Fore, Style, init

# Initialize colorama
init()

def get_help(item, switch, debug=False):
    """
    Prints methods, functions, dunder methods, or the entire class details for a given item.

    Parameters:
    item (str): The item to look up.
    switch (str): The type of information to display ('show_methods', 'show_functions', 'show_dunders', 'show_class').
    debug (bool): If True, enables debug logging.

    Returns:
    None
    """
    if debug:
        print(f"Trying to get help for item: {item}")
    obj = None

    try:
        # Attempt to evaluate item directly
        if debug:
            print(f"{Fore.RED}Evaluating {item}")
        obj = eval(item)
        if debug:
            print(f"{Fore.RED}Evaluated {item} successfully. Object: {obj}")
    except (NameError, SyntaxError):
        if debug:
            print(f"{Fore.RED}Evaluation failed for {item}. Trying to import as module.")
        try:
            # If eval fails, try importing the item as a module
            module_name, _, attr_name = item.partition('.')
            if debug:
                print(f"{Fore.RED}Importing module {module_name}")
            module = importlib.import_module(module_name)
            if debug:
                print(f"{Fore.RED}Imported module {module_name} successfully.")
            if attr_name:
                if debug:
                    print(f"{Fore.RED}Getting attribute {attr_name} from module {module_name}")
                obj = getattr(module, attr_name)
                if debug:
                    print(f"{Fore.RED}Retrieved attribute {attr_name}. Object: {obj}")
            else:
                obj = module
        except ImportError as e:
            if debug:
                print(f"{Fore.RED}Module {module_name} not found. Error: {e}")
            return
        except AttributeError as e:
            if debug:
                print(f"{Fore.RED}Attribute {attr_name} not found in module {module_name}. Error: {e}")
            return

    if not obj:
        if debug:
            print(f"{Fore.RED}Unable to find the item: {item}")
        return

    if switch == "show_methods":
        print(f"Methods for {item}:")
        methods = [method for method in dir(obj) if not method.startswith('__')]
        for i, method in enumerate(methods, 1):
            doc = getattr(obj, method).__doc__
            print(f"{Fore.GREEN}{i}. {Fore.CYAN}{method} - {doc.splitlines()[0] if doc else 'No description available'}{Style.RESET_ALL}")
    elif switch == "show_functions":
        if callable(obj):
            print(f"Help for function {item}:")
            print(f"{Fore.CYAN}{obj.__doc__}{Style.RESET_ALL}")
        else:
            print(f"Functions for {item}:")
            functions = [func for func in dir(obj) if not func.startswith('__') and callable(getattr(obj, func))]
            for i, func in enumerate(functions, 1):
                doc = getattr(obj, func).__doc__
                print(f"{Fore.GREEN}{i}. {Fore.CYAN}{func} - {doc.splitlines()[0] if doc else 'No description available'}{Style.RESET_ALL}")
    elif switch == "show_dunders":
        print(f"Dunder methods for {item}:")
        dunders = [method for method in dir(obj) if method.startswith('__')]
        for i, dunder in enumerate(dunders, 1):
            doc = getattr(obj, dunder).__doc__
            print(f"{Fore.GREEN}{i}. {Fore.CYAN}{dunder} - {doc.splitlines()[0] if doc else 'No description available'}")
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
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.show_methods:
        get_help(args.item, "show_methods", debug=args.debug)
    elif args.show_functions:
        get_help(args.item, "show_functions", debug=args.debug)
    elif args.show_dunders:
        get_help(args.item, "show_dunders", debug=args.debug)
    elif args.show_class:
        get_help(args.item, "show_class", debug=args.debug)
    else:
        print("Please specify --show_methods, --show_functions, --show_dunders, or --show_class.")
