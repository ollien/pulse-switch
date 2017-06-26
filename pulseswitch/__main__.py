#! /usr/bin/env python3

from . import pulse
import sys

def print_menu_and_get_index(device_type):
    devices = None
    if device_type == "sink":
        devices = pulse.get_sinks()
        print("Available Pulse Audio sinks:")
    elif device_type == "source":
        devices = pulse.get_sources()
        print("Available Pulse Audio sources:")
    else:
        raise ValueError("device_type must be either sink or source")
    for index, device in enumerate(devices):
        print("\t{index}: {name}".format(index=index, name=device["device_name"]))
    valid_input = False
    selection = None
    while not valid_input:
        selection = input("? ")
        valid_input = is_int(selection) and 0 <= int(selection) < len(devices)
    selection = int(selection)
    return devices[selection]["pulse_index"]

def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

#Returns true if arg is "o", "output", "i", or "input"
def check_type_arg_validity(arg):
    return arg.lower() in ("o", "output", "i", "input")

def main():
    #Check if command is pulse-switcher.py i[nput] or o[utput]
    if len(sys.argv) == 2 and check_type_arg_validity(sys.argv[1]):
        if sys.argv[1].lower() in ("o", "output"):
            sink_index = print_menu_and_get_index("sink")
            pulse.switch_to_sink(sink_index)
        elif sys.argv[1].lower() in ("i", "input"):
            source_index = print_menu_and_get_index("source")
            pulse.switch_to_source(source_index)
    #Check if command is pulse-switcher.py i[nput] or o[utput] n
    elif len(sys.argv) == 3 and is_int(sys.argv[2]) and check_type_arg_validity(sys.argv[1]):
        if sys.argv[1].lower() in ("o", "output"):
            pulse.switch_to_sink(int(sys.argv[2]))
        elif sys.argv[1].lower() in ("i", "input"):
            pulse.switch_to_source(int(sys.argv[2]))
    else:
        print((
        "Usage: pulse-switcher type [index]\n"
        "Where:\n"
        "    type is i[nput] or o[utput]\n"
        "    index is a pulse audio sink index or source index"))

if __name__ == "__main__":
    main()