#! /usr/bin/env python3

import subprocess
import re

#Get all sinks from pulse and return an array of the sinks
def get_sinks():
    pacmd_output, _ = subprocess.Popen("pacmd list-sinks",
                shell=True, stdout=subprocess.PIPE).communicate()
    raw_sinks = re.split(r"\s\s(\s|\*)\sindex:\s(\d+)",
            pacmd_output.decode("utf-8"))[1:]
    sinks = []
    current_index = None
    is_current_active = False
    for index, item in enumerate(raw_sinks):
        if index % 3 == 0:
            is_current_active = item == "*"
            continue
        elif index % 3 == 1:
            current_index = int(item)
            continue
        elif index % 3 == 2:
            #pacmd mixes tabs and spaces in its output. Go figure.
            device_name_match = re.search(r"\t\tdevice.description\s=\s\"(.*)\"", item)
            device_name = device_name_match.groups()[0]
            sink = {"pulse_index": current_index, "device_name": device_name}
            sinks.append(sink)
    return sinks

def get_sink_input_indexes():
        pacmd_output, _ = subprocess.Popen("pacmd list-sink-inputs",
                    shell = True, stdout=subprocess.PIPE).communicate()
        index_matches = re.finditer(r"\s{4}index:\s(\d+)", pacmd_output.decode("utf-8"))
        return [int(index.groups()[0]) for index in index_matches]

def set_sink_input(input_index, sink_index):
    if type(input_index) == int:
        input_index = str(input_index)
    if type(sink_index) == int:
        sink_index = str(sink_index)
    subprocess.Popen(["pacmd", "move-sink-input", input_index, sink_index])

def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    sinks = get_sinks()
    print("Available Pulse Audio sink:")
    for index, sink in enumerate(sinks):
        print("\t{index}: {name}".format(index=index, name=sink["device_name"]))
    valid_input = False
    selection = None
    while not valid_input:
        selection = input("? ")
        valid_input = is_int(selection) and 0 <= int(selection) < len(sinks)
    selection = int(selection)
    selected_sink = sinks[selection]
    print("Selected {}".format(selected_sink["device_name"]))
    #TODO: Switch audio sinks
