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
  -h, --help            show this help message and exit
  -c, --show_class      Show the entire class details
  -d, --show_dunders    Look up dunder methods (__methods__)
  -f, --show_functions  Look up functions in a class
  -m, --show_methods    Look up methods in a class

Debug options:
  --debug               Enable debug logging

Module options:
  -am, --show_all_modules
                        Show all Python modules installed
  -fm SHOW_FILTERED_MODULES, --show_filtered_modules SHOW_FILTERED_MODULES
                        Show all Python modules starting with a letter