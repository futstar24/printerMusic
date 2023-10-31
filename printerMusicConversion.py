import pretty_midi


noteNames = []

def extract_melody_notes(file_path):
    # Load MIDI file
    midi_data = pretty_midi.PrettyMIDI("test_songs/"+file_path)

    # Get the instrument (assuming it's the first instrument)
    # You may need to modify this based on your MIDI file structure
    instrument = midi_data.instruments[0]
    keySigs = midi_data.key_signature_changes
    print(keySigs)
    for key in keySigs:
        print(pretty_midi.key_number_to_key_name((key.key_number)))
        print(key.key_number)
        keyDifference = key.key_number-7

    # Extract notes and their properties
    melody_notes = []
    tempoChanges = midi_data.get_tempo_changes()
    tempoTimes = tempoChanges[0].tolist()
    tempos = tempoChanges[1].tolist()
    currentTempo = tempos[0] #could be 1
    for i in range(len(instrument.notes)): #If multiple notes played at a time, reduce to just the highest
        j = i+1
        while j < len(instrument.notes):
            note1 = instrument.notes[i]
            note2 = instrument.notes[j]
            if note1.start >= note2.start:
                if note1.pitch > note2.pitch:
                    instrument.notes.remove(note2)
                    j-=1
                else:
                    instrument.notes.remove(note1)
                    j-=1
            j+=1


    pastNote = None

    for note in instrument.notes:
        if pastNote == None or not (pastNote.end > note.start):
            note_name = pretty_midi.note_number_to_name(note.pitch) #Offset to account for different keys
            try:
                i = tempoTimes.index(note.start)
                currentTempo = tempos[i]
            except:
                pass

            duration = ((note.end-note.start)*(currentTempo/60))*4
            #print(note.end-note.start)
            if note_name not in noteNames:
                noteNames.append(note_name)
            


            if pastNote is not None and round((note.start)*(currentTempo/60),2)-round((pastNote.end)*(currentTempo/60),2) > 0:
                restDuration = round((note.start-pastNote.end)*(currentTempo/60)*4)

                while restDuration-4 >= 0:
                    restDuration-=4
                    melody_notes.append(["Rest",4,round((pastNote.end)*(currentTempo/60),2),round((note.start)*(currentTempo/60),2)])
                #melody_notes.append(("Rest", round(pastNote.end*(currentTempo/60),2), restDuration, currentTempo))
                if restDuration > 0:
                    melody_notes.append(["Rest",restDuration, round((pastNote.end)*(currentTempo/60),2),round((note.start)*(currentTempo/60),2)])
            
            melody_notes.append([note_name, round(duration), round((note.start)*(currentTempo/60),2),round((note.end)*(currentTempo/60),2)])
            pastNote = note    

    return melody_notes

# Specify the path to your MIDI file
midi_file_path = "hot-cross-buns.mid"

# Extract the melody notes from the MIDI file
melody_notes = extract_melody_notes(midi_file_path)

# Print the extracted melody notes
'''for note in melody_notes:
    print(f"Note: {note[0]}, Duration: {note[1]}, Start Time: {note[2]}, End Time: {note[3]}")
    #print(f"{note[0]} {(round(note[1]))}")'''

def convert_to_print(noteList):
    #Converts list of notes to print format, write to output file
    #Parameters: List of notes (each note is a list of [str: note name, int: duration])
    #Returns: None

    freqSet = set([])
    for note in noteList: #Check that all notes are between C3 and C6
        name = note[0]
        if name != "Rest":
            if (int(name[-1]) <= 3) or (int(name[-1]) >= 6):
                if not (name == "C3" or name == "C6" or name == "BS3"): #Edges of playable range
                    print(f'Error: note {name} out of range')
                    return
            if note[0][1] == '#':
                note[0][1] == 'S'
            freqSet.add(name)

    print(freqSet)
        

#melody_notes = [["BS3", 3], ["D5", 2], ["E5", 3]]

for note in melody_notes:
    print(f"{note[0]} {note[1]}")

convert_to_print(melody_notes)
