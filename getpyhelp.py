import argparse
import importlib
import pkgutil
from colorama import Fore, Style, init

# Initialize colorama
init()

def get_help(item, switch, debug=False, filter_letter=None):
    def display_and_select(items):
        for i, item in enumerate(items, 1):
            print(f"{Fore.GREEN}{i}. {Fore.CYAN}{item}{Style.RESET_ALL}")
        try:
            choice = int(input("\nEnter the number of the item for which you want more details: "))
            if 1 <= choice <= len(items):
                return items[choice - 1]
            else:
                print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and {len(items)}.{Style.RESET_ALL}")
                return None
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")
            return None

    if switch == "show_all_modules":
        print(f"{Fore.YELLOW}Installed modules:{Style.RESET_ALL}")
        modules = sorted([module.name for module in pkgutil.iter_modules()])
        if filter_letter:
            modules = [module for module in modules if module.startswith(filter_letter)]

        # Print modules in a numbered list
        for i, module in enumerate(modules, 1):
            print(f"{Fore.CYAN}{i}. {Fore.YELLOW}{module}{Style.RESET_ALL}")
        print()  # New line after printing all modules

        selected_module = display_and_select(modules)
        if selected_module:
            print(f"{Fore.YELLOW}\nDetailed help for module {selected_module}:{Style.RESET_ALL}")
            help(importlib.import_module(selected_module))
        return

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
                print(f"{Fore.GREEN}Imported module {module_name} successfully.")
            if attr_name:
                if debug:
                    print(f"{Fore.RED}Getting attribute {attr_name} from module {module_name}")
                obj = getattr(module, attr_name)
                if debug:
                    print(f"{Fore.GREEN}Retrieved attribute {attr_name}. Object: {obj}")
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
            print(f"{Fore.RED}Unable to find the item: {item}{Style.RESET_ALL}")
        return

    if switch == "show_methods":
        print(f"{Fore.YELLOW}Methods for {item}:{Style.RESET_ALL}")
        methods = [method for method in dir(obj) if not method.startswith('__')]
        selected_method = display_and_select(methods)
        if selected_method:
            print(f"{Fore.YELLOW}\nDetailed help for method {selected_method}:{Style.RESET_ALL}")
            doc_string = getattr(obj, selected_method).__doc__
            if doc_string:
                print(f"{Fore.CYAN}{doc_string}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No description available{Style.RESET_ALL}")

    elif switch == "show_functions":
        if callable(obj):
            print(f"{Fore.YELLOW}Help for function {item}:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{obj.__doc__}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Functions for {item}:{Style.RESET_ALL}")
            functions = [func for func in dir(obj) if not func.startswith('__') and callable(getattr(obj, func))]
            selected_function = display_and_select(functions)
            if selected_function:
                print(f"{Fore.YELLOW}\nDetailed help for function {selected_function}:{Style.RESET_ALL}")
                doc_string = getattr(obj, selected_function).__doc__
                if doc_string:
                    print(f"{Fore.CYAN}{doc_string}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}No description available{Style.RESET_ALL}")

    elif switch == "show_dunders":
        print(f"{Fore.YELLOW}Dunder methods for {item}:{Style.RESET_ALL}")
        dunders = [method for method in dir(obj) if method.startswith('__')]
        selected_dunder = display_and_select(dunders)
        if selected_dunder:
            print(f"{Fore.YELLOW}\nDetailed help for dunder method {selected_dunder}:{Style.RESET_ALL}")
            doc_string = getattr(obj, selected_dunder).__doc__
            if doc_string:
                print(f"{Fore.CYAN}{doc_string}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No description available{Style.RESET_ALL}")

    elif switch == "show_class":
        print(f"{Fore.YELLOW}Class details for {item}:{Style.RESET_ALL}")
        help(obj)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Python help on methods, functions, dunders, or the entire class.")
    parser.add_argument("item", nargs="?", help="The item to look up", default=None)

    # Debug section
    debug_group = parser.add_argument_group('Debug options')
    debug_group.add_argument("--debug", action="store_true", help="Enable debug logging")

    # Module section
    module_group = parser.add_argument_group('Module options')
    module_group.add_argument("-am", "--show_all_modules", action="store_true", help="Show all Python modules installed")
    module_group.add_argument("-fm", "--show_filtered_modules", help="Show all Python modules starting with a letter")

    # Other options
    parser.add_argument("-c", "--show_class", action="store_true", help="Show the entire class details")
    parser.add_argument("-d", "--show_dunders", action="store_true", help="Look up dunder methods (__methods__)")
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
    elif args.show_dunders:
        get_help(args.item, "show_dunders", debug=args.debug)
    elif args.show_class:
        get_help(args.item, "show_class", debug=args.debug)
    else:
        print("Please type python gethelp.py -h for more information")
