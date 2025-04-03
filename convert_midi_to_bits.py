import sys

byte_data = []

try:
    parse_file: str = sys.argv[1]

    try:
        if ".mid" in parse_file:
            with open(f"input_byte_files/{parse_file}", "rb") as data:
                byte_data = [*(format(byte, '08b') for byte in data.read())]
        else:
            print("Please ensure: \n\tYour file has the file extension of .mid.")

    except FileNotFoundError:
        print("Please ensure: \n\tYour MIDI file is in the input_byte_files folder, \n\tYou properly input the MIDI file's name.")

except IndexError:
    print("Please enter the MIDI file as the first argument.")

print(byte_data)