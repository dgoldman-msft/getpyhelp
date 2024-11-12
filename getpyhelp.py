import argparse
import importlib
import pkgutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def display_and_select(items, debug=False):
    if debug:
        print(f"{Fore.RED}Calling display_and_select{Style.RESET_ALL}")
    for i, item in enumerate(items, 1):
        print(f"{Fore.GREEN}{i}. {Fore.CYAN}{item}{Style.RESET_ALL}")
    try:
        choice = int(input("\nEnter the number of the item for which you want more details: "))
        if 1 <= choice <= len(items):
            return items[choice - 1]
        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and {len(items)}.{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")
    return None

def get_help(item, switch, debug=False, filter_letter=None):
    if debug:
        print(f"{Fore.RED}Calling get_help with switch: {switch}{Style.RESET_ALL}")
    if switch == "show_all_modules":
        show_all_modules(filter_letter, debug)
        return

    obj = get_object(item, debug)
    if not obj:
        return

    if switch == "show_methods":
        show_methods(item, obj, debug)
    elif switch == "show_functions":
        show_functions(item, obj, debug)
    elif switch == "show_special_methods":
        show_special_methods(item, obj, debug)
    elif switch == "show_class":
        show_class(obj, debug)

def show_all_modules(filter_letter, debug=False):
    if debug:
        print(f"{Fore.RED}Calling show_all_modules{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Installed modules:{Style.RESET_ALL}")
    modules = sorted([module.name for module in pkgutil.iter_modules()])
    if filter_letter:
        modules = [module for module in modules if module.startswith(filter_letter)]
    selected_module = display_and_select(modules, debug)
    if selected_module:
        print(f"{Fore.YELLOW}\nDetailed help for module {selected_module}:{Style.RESET_ALL}")
        help(importlib.import_module(selected_module))

def get_object(item, debug=False):
    if debug:
        print(f"{Fore.RED}Calling get_object for item: {item}{Style.RESET_ALL}")
    try:
        obj = eval(item)
        if debug:
            print(f"{Fore.RED}Evaluated {item} successfully. Object: {obj}{Style.RESET_ALL}")
        return obj
    except (NameError, SyntaxError):
        if debug:
            print(f"{Fore.RED}Evaluation failed for {item}. Trying to import as module.{Style.RESET_ALL}")
        return import_module(item, debug)

def import_module(item, debug=False):
    if debug:
        print(f"{Fore.RED}Calling import_module for item: {item}{Style.RESET_ALL}")
    try:
        module_name, _, attr_name = item.partition('.')
        module = importlib.import_module(module_name)
        if debug:
            print(f"{Fore.GREEN}Imported module {module_name} successfully.{Style.RESET_ALL}")
        if attr_name:
            obj = getattr(module, attr_name)
            if debug:
                print(f"{Fore.GREEN}Retrieved attribute {attr_name}. Object: {obj}{Style.RESET_ALL}")
            return obj
        return module
    except (ImportError, AttributeError) as e:
        if debug:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    return None

def show_methods(item, obj, debug=False):
    if debug:
        print(f"{Fore.RED}Calling show_methods for item: {item}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Methods for {item}:{Style.RESET_ALL}")
    methods = [method for method in dir(obj) if not method.startswith('__')]
    selected_method = display_and_select(methods, debug)
    if selected_method:
        print_detailed_help(obj, selected_method, debug)

def show_functions(item, obj, debug=False):
    if debug:
        print(f"{Fore.RED}Calling show_functions for item: {item}{Style.RESET_ALL}")
    if callable(obj):
        print(f"{Fore.YELLOW}Help for function {item}:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{obj.__doc__}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Functions for {item}:{Style.RESET_ALL}")
        functions = [func for func in dir(obj) if not func.startswith('__') and callable(getattr(obj, func))]
        selected_function = display_and_select(functions, debug)
        if selected_function:
            print_detailed_help(obj, selected_function, debug)

def show_special_methods(item, obj, debug=False):
    if debug:
        print(f"{Fore.RED}Calling show_special_methods for item: {item}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Special methods for {item}:{Style.RESET_ALL}")
    special_methods = [method for method in dir(obj) if method.startswith('__')]
    selected_special_method = display_and_select(special_methods, debug)
    if selected_special_method:
        print_detailed_help(obj, selected_special_method, debug)

def show_class(obj, debug=False):
    if debug:
        print(f"{Fore.RED}Calling show_class{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Class details:{Style.RESET_ALL}")
    help(obj)

def print_detailed_help(obj, attribute, debug=False):
    if debug:
        print(f"{Fore.RED}Calling print_detailed_help for attribute: {attribute}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}\nDetailed help for {attribute}:{Style.RESET_ALL}")
    doc_string = getattr(obj, attribute).__doc__
    if doc_string:
        print(f"{Fore.CYAN}{doc_string}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No description available{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Python help on methods, functions, dunders, or the entire class.")
    parser.add_argument("item", nargs="?", help="The item to look up", default=None)

    debug_group = parser.add_argument_group('Debug options')
    debug_group.add_argument("-dbg", "--debug", action="store_true", help="Enable debug logging")

    module_group = parser.add_argument_group('Module options')
    module_group.add_argument("-am", "--show_all_modules", action="store_true", help="Show all Python modules installed")
    module_group.add_argument("-fm", "--show_filtered_modules", help="Show all Python modules starting with a letter")

    parser.add_argument("-c", "--show_class", action="store_true", help="Show the entire class details")
    parser.add_argument("-d", "--show_special_methods", action="store_true", help="Look up special 'Dunder' methods (__methods__)")
    parser.add_argument("-f", "--show_functions", action="store_true", help="Look up functions in a class")
    parser.add_argument("-m", "--show_methods", action="store_true", help="Look up methods in a class")

    args = parser.parse_args()

    if args.show_all_modules:
        get_help(None, "show_all_modules", debug=args.debug)
    elif args.show_filtered_modules:
        get_help(None, "show_all_modules", debug=args.debug, filter_letter=args.show_filtered_modules)
    elif args.show_methods:
        get_help(args.item, "show_methods", debug=args.debug)
    elif args.show_functions:
        get_help(args.item, "show_functions", debug=args.debug)
    elif args.show_special_methods:
        get_help(args.item, "show_special_methods", debug=args.debug)
    elif args.show_class:
        get_help(args.item, "show_class", debug=args.debug)
    else:
        print("Please type python getpyhelp.py -h for more information")
