import sys, mido

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

channel_lengths = {}
channel_notes = {}
meta_data = []

midi_file_name = f"input_byte_files/{sys.argv[1]}"
midi_file = mido.MidiFile(midi_file_name)

# Print MIDI file details
print(f"Format: {midi_file.type}, Tracks: {len(midi_file.tracks)}")

# Read and print MIDI messages
for i, track in enumerate(midi_file.tracks):
    print(f"\nTrack {i}: {track.name}")
    for msg in track:
        if isinstance(msg, mido.Message):
            if msg.type == "note_on" or msg.type == "note_off":
                channel_already_in_dict = False
                for channel in channel_lengths:
                    if channel == msg.note:
                        channel_lengths[msg.note] += 1
                        channel_notes[msg.note].append(msg)
                        channel_already_in_dict = True
                        break
                
                if not channel_already_in_dict:
                    channel_lengths[msg.note] = 1
                    channel_notes[msg.note] = [msg]
            else:
                meta_data.append(msg)

populous_channels = {1: -1, 2: -1, 3: -1, 4: -1}
for channel in channel_lengths:
    for populous_channel in populous_channels:
        if populous_channels[populous_channel] == -1:
            populous_channels[populous_channel] = channel
            break
        elif channel_lengths[channel] > channel_lengths[populous_channels[populous_channel]]:
            populous_channels[populous_channel] = channel
            break
