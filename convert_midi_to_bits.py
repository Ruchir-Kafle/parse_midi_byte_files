import sys, mido

note_data = []

# try:
#     parse_file: str = sys.argv[1]

#     try:
#         if ".mid" in parse_file:
#             # Load MIDI file
            
#         else:
#             print("Please ensure: \n\tYour file has the file extension of .mid.")

#     except FileNotFoundError:
#         print("Please ensure: \n\tYour MIDI file is in the input_byte_files folder, \n\tYou properly input the MIDI file's name.")

# except IndexError:
#     print("Please enter the MIDI file as the first argument.")

# print(note_data)

midi_file_name = f"input_byte_files/{sys.argv[1]}"
midi_file = mido.MidiFile(midi_file_name)

# Print MIDI file details
print(f"Format: {midi_file.type}, Tracks: {len(midi_file.tracks)}")

# Read and print MIDI messages
for i, track in enumerate(midi_file.tracks):
    print(f"\nTrack {i}: {track.name}")
    for msg in track:
        note_data.append(msg)

print(note_data)