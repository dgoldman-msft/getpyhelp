# getpyhelp
A custom python helper function to extend the default help command

## Getting Started with getpyhelp

This is a helper script that will extend the default help() in python

### DESCRIPTION

This helper script will allow you to import modules, dump methods, functions and dunders.

### Examples

usage: gethelp.py [-h] [--debug] [-am] [-fm SHOW_FILTERED_MODULES] [-c] [-d] [-f] [-m] [item]

Get Python help on methods, functions, dunders, or the entire class.

positional arguments:
  item                  The item to look up

options:
    -c,     --show_class                        Show the entire class details.
    -d,     --show_special_methods              Look up special methods (__methods__).
    -dbg    --debug                             Enable debug logging.
    -h,     --help                              Show this help message and exit.
    -f,     --show_functions                    Look up functions in a class.
    -m,     --show_methods                      Look up methods in a class.

Debug options:
    -dbg    --debug                             Enable debug logging

Module options:
    -am,    --show_all_modules                  Show all Python modules installed.
    -fm,    --show_filtered_modules <letter>    Show all Python modules starting with a letter.


NOTE: If you want to run this as an override function you can do the following:
1. Edit your .bashrc or .zshrc file where you have your aliases defined.
2. Add --> alias youralias='python3 ~/scripts/getpyhelp.py'
3. Source your profile file.
