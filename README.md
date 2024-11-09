# getpyhelp
A custom python helper function to extend the default help command

## Getting Started with getpyhelp

This is a helper script that will extend the default help() in python

### DESCRIPTION

This helper script will allow you to import modules, dump methods, functions and dunders.

### Examples

- EXAMPLE

    python getpyhelp.py
    usage: getpyhelp.py [-h] [-m] [-f] [-d] [-c] [--debug] item
    getpyhelp.py: error: the following arguments are required: item

- EXAMPLE

    python getpyhelp.py str -m

    Display all string methods

- EXAMPLE

    python getpyhelp.py str -f

    Display all string functions

- EXAMPLE

    python getpyhelp.py str -d

    Display all string dunders

- EXAMPLE

    python getpyhelp.py str -c

    Display string class object (full help)