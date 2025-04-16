import sys, mido, json

# py -m convert_midi_to_bits {Song MIDI File Path} {Song Name} {Artist}

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

note_lengths = {}
note_messages = {}
track_velocities = {}
times = {}

populous_notes = {1: -1, 2: -1, 3: -1, 4: -1}

midi_file_path = f"input_byte_files/{sys.argv[1]}"
midi_file = mido.MidiFile(midi_file_path)

# Print MIDI file details
print(f"Format: {midi_file.type}, Tracks: {len(midi_file.tracks)}")

# Read and print MIDI messages
for i, track in enumerate(midi_file.tracks):
    meta_data = []
    total_ticks = 0
    velocity_changes = {}
    print(f"\nTrack {i}: {track.name}")

    for msg in track:
        attributes = [attribute for attribute in msg.dict()]
        if "time" in attributes:
            total_ticks += msg.time

        if isinstance(msg, mido.Message):
            if msg.type == "note_on" or msg.type == "note_off":
                note_already_in_dict = False
                for note in note_lengths:
                    if note == msg.note:
                        note_lengths[msg.note] += 1
                        note_messages[msg.note].append({"time": total_ticks, "message": msg})
                        note_already_in_dict = True
                        break
                
                if not note_already_in_dict:
                    note_lengths[msg.note] = 1
                    note_messages[msg.note] = [{"time": total_ticks, "message": msg}]

            else:
                meta_data.append(msg)
        else:
            meta_attributes = [meta_attribute for meta_attribute in msg.dict()]
            if "tempo" in attributes:
                velocity_changes[total_ticks] = midi_file.ticks_per_beat / (msg.tempo / 1_000_000)
            
            meta_data.append(msg)

    track_velocities[i] = velocity_changes
    times[i] = total_ticks

for note in note_lengths:
    for populous_note in populous_notes:
        if populous_notes[populous_note] == -1:
            populous_notes[populous_note] = note
            break
        elif note_lengths[note] > note_lengths[populous_notes[populous_note]]:
            populous_notes[populous_note] = note
            break

json_data = {"name": sys.argv[2], "artist": sys.argv[3], "units": times, "track_velocities": track_velocities, "notes": []}
for note in populous_notes:
    messages = note_messages[populous_notes[note]]
    for i, message in enumerate(messages):
        if message["message"].type == "note_on":
            json_data["notes"].append({"note": note - 1, "position": message["time"], "length": (messages[i + 1]["time"] - message["time"])})

        # Not in use code, was working off the assumption that channels were being parsed instead of individual note channels.
        # As such, much of the code makes the assumption that there are multiple note on and offs simultaneously happen.
        # Might be useful in the future?
        # unclosed_on_messages = []
        # unclosed_off_messages = []
        # if message["message"].type == "note_on":
        #     unclosed_on_messages.append(message)
        # elif message["message"].type == "note_off":
        #     for i, unclosed_message in enumerate(unclosed_on_messages):
        #         if unclosed_message.note == message["message"].note:
        #             json_data["notes"].append({"note": note - 1, "position": unclosed_message["time"], "length": message["time"] - unclosed_message["time"]})
        #             unclosed_on_messages.pop(i)
        #             break
        #     else:
        #         json_data["notes"].append({"note": note - 1, "position": message["time"], "length": 0})

output_file_path = f"output_bit_files/{sys.argv[2]}.json"
with open(output_file_path, "w") as file:
    json.dump(json_data, file, indent=4)