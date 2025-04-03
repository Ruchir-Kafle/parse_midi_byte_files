import sys

try:
    parse_file: str = sys.argv[1]

    if type(parse_file) == "<class 'str'>" and ".mid" in parse_file:
        with open(parse_file, "rb") as midi_file:
            data = midi_file.read()
    else:
        print("Please properly enter the path and ensure it has a file extension of .mid.")

except IndexError:
    print("Please enter the MIDI file as the first argument.")