import sys, mido, json

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
meta_data = []
total_time = 0

midi_file_name = f"input_byte_files/{sys.argv[1]}"
midi_file = mido.MidiFile(midi_file_name)

# Print MIDI file details
print(f"Format: {midi_file.type}, Tracks: {len(midi_file.tracks)}")

# Read and print MIDI messages
for i, track in enumerate(midi_file.tracks):
    print(f"\nTrack {i}: {track.name}")
    for msg in track:
        attributes = [attribute for attribute in msg.dict()]
        if "time" in attributes:
            total_time += msg.time

        if isinstance(msg, mido.Message):
            if msg.type == "note_on" or msg.type == "note_off":
                note_already_in_dict = False
                for note in note_lengths:
                    if note == msg.note:
                        note_lengths[msg.note] += 1
                        note_messages[msg.note].append({"time": total_time, "message": msg})
                        note_already_in_dict = True
                        break
                
                if not note_already_in_dict:
                    note_lengths[msg.note] = 1
                    note_messages[msg.note] = [{"time": total_time, "message": msg}]
            else:
                meta_data.append(msg)

populous_notes = {1: -1, 2: -1, 3: -1, 4: -1}
for note in note_lengths:
    for populous_note in populous_notes:
        if populous_notes[populous_note] == -1:
            populous_notes[populous_note] = note
            break
        elif note_lengths[note] > note_lengths[populous_notes[populous_note]]:
            populous_notes[populous_note] = note
            break

json_data = {"name": "", "artist": "", "seconds": 0, "units": 0, "notes": []}
for note in populous_notes:
    messages = note_messages[populous_notes[note]]
    for i, message in enumerate(messages):
        if message["message"].type == "note_on":
            json_data["notes"].append({"note": note - 1, "position": message["time"], "length": messages[i + 1]["time"] - message["time"]})

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



with open("output_bit_files/output.json", "w") as file:
    file.write(json.dump(json_data))


