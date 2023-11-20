import pretty_midi
import numpy as np
import sounddevice as sd
from math import floor

note_lines = {   "C3" : "               U               I               K    *            T  1   C3  130\n1            M               9                    ⌑            L    2   C3  130",  
                "CS3" : "                                                                    1   CS3 138\n16#UZKP*E&38                                                        2   CS3 138", 
                "D3" : "  $            T            D               X            .          1   D3  146\n1            K            3            P               0            2   D3  146", 
                "DS3" : "         K             U           3          C              M      1   DS3 155\n1⌑          *             K           /          1              B   2   DS3 155", 
                "E3" : "   M         P            *      A         D            I      &    1   E3  164\n1                  /         U         X         ‡         J        2   E3  164", 
                "F3" : "           F    $       O       J                        M       ,  1   F3  174\n1                      /    6    .       F       A                  2   F3  174", 
                "FS3" : "              A     V          S     F                X     .       1   FS3 185\n1             ⌑     M                5     R          O     0       2   FS3 185", 
                "G3" : "           H    Q    Y                   X    7 E                   1   G3  196\n1                   ⌑ -    ‡                   Z    9    I          2   G3  196", 
                "GS3" : "  O    F                              J $    .    #    ,    $       1   GS3 207\n1    /    J $       1 #                              F    6    W    2   GS3 207", 
                "A3" : "    $         M   V              9      ⌑         E           P     1   A3  220\n1       2   C         Q      ,    ‡         T   4         I         2   A3  220", 
                "AS3" : "   4      A       Q             P   S      M      /          0      1   AS3 233\n1   Q          N      S      M   #             0          7      D  2   AS3 233", 
                "B3" : " -    /           B    V      T    F           X    &           ,   1   B3  246\n1      . %           1       O           7 Q         Q 9            2   B3  246", 
                "C4" : "    #       A        Y       &        N       7     *       S       1   C4  261\n1 &     L       5     -       @        G       Z        4       O   2   C4  261", 
                "CS4" : "         50TYJO$DI27                                                1   CS4 277\n16#UZKP*E&38                                                        2   CS4 277",  
                "D4" : "  $    %       T       3    D       P       X    8       .    R     1   D4  293\n1    $       K    T  S    3       F    P       X       0    .       2   D4  293", 
                "DS4" : "  P   %         Z      U    8      3   H      C      -    K      Z  1   DS4 311\n1    E   -         P      K U         /   6      1      H    *      2   DS4 311", 
                "E4" : "   M 2       P         -       T A         DY      Z    I      &K   1   E4  329\n1          Q      R/        *U      V    E      F‡         J .      2   E4  329", 
                "F4" : "      6    F    $    M          J #    4       .       F M       ,  1   F4  349\n1    A    O    ,       /  Y 6    .       F    O  A ,       W    #   2   F4  349", 
                "FS4" : " V     8&     A     M     X9     ⌑     C     OY     #     2     E   1   FS4 369\n1C     O     Z      2        G   ‡ -   /     4     G   $     K      2   FS4 369",
                "G4" : "       1   HA   Q   LY   T               X@   7 E 2 *               1   G4  392\n1               5   ⌑E-   N‡               K   ZS   9   4I          2   G4  392", 
                "GS4" : "  O$   F.                           M J $   F.   6#U   ,   O$       1   GS4 415\n16   /W   JO$   F   16#   W                         AF.   6   /W,   2   GS4 415", 
                "A4" : "    $7        M   V .   *        9N     ⌑        ZE     @     P3    1   A4  440\n1    ⌑Y     C#    0   Q     3,    ‡F      R T   4 -   ,   I     U   2   A4  440",
                "AS4" : "1 2 Q S      . N      S H    M   #    G   K    0 D      J 7      D  2   AS4 466\n ‡ 4      A X   2 Q       W.    P   S    & M      / G      M 0 D    1   AS4 466",
                "B4" : " -    /    A    U B    V C    W  V F U    G    X    & Y       1 ,   1   B4  493\n1    J . %    ⌑    L 1       O 4    P    7 Q  P 8    Q 9 P       @  2   B4  493",
                "C5" : "&           I *UL            6-I   L          TK6 I *        R % T  1   C5  526\n1@       &   MCX           W 9A⌑M           L7W  A⌑         J*  7W  2   C5  526",
                "CS5" : "         50TYJO$DI27                         O$DI27@V‡LQ            1   CS5 554\n16#UZKP*E&38                        KP*E&38/W,M                     2   CS5 554",
                "D5" : "  $6   %   F   T   R1   ‡   D   0   P   1V   B   8   K   .T   R     1   D5  587\n1V   $3  8   K 0 HT   R   3   %   F0   P   1   X   D8   K   .   V   2   D5  587",
                "DS5" : "  P     7KI     Z   F  U$   8  O   3  JH   V  C   @  -5   K     2Z  1   DS5 622\n1Y  2E   - V 7     P   4  KI   W  D   /  $6   L  1   ‡  HT   *  0   2   DS5 622",
                "E5" : "   MT2  I   HPW       . Z *      A%4 X    5DL  ‡   Z   0I      &K/  1   E5  689\n1 UH   G V Q      RY⌑ T    1*U  J      X6E      F‡9      0BJ .      2   E5  689",
                "F5" : "  O   6,   F   W$   6M / .    D J #    4 A ,  O.U      F#M      6,  1   F5  698\n1W   A#   O   1,   F   /$ Y 6   O.   W   F#   O  A6,   .   W$   #   2   F5  698",
                "FS5" : "$V    K8&   V A    &M    AX9     ⌑OY   C #   OY2   N#E    2 ‡   E   1   FS5 739\n1CZ   ⌑O@   CZ    O 2   Z   /G   ‡4-   /G    4-%   G T $   6 K   I  2   FS5 739",
                "G5" : "U J #  16  HA   Q   LY  0T  5&C   -   N  X@   7 E 2 *  K   ZS   9   1   G5  783\n1 &CQ   LY   T  5   ⌑E-   N‡ X@   7   2G   B  MRS , 9   4I  $   O   2   G5  783",
                "GS5" : "  O$D   .5   @ ‡ X N   *E&   50   V M J $   F.4   #U   , R O E   ⌑  1   GS5 860\n16 2 /W   JO$   F 4 1 #   X% Y P*E   ⌑ 0 7 V   %N   AF.   6 U / ,   2   GS5 860",
                "A5" : "   Y$   9   E/M   VQ.      B5J   9NH    ⌑T$     6ZE   JI@      3WR  1   A5  880\n1U &  Y$7  4C#K 8    VQ.S  *3,  Y7‡F N    R⌑TO  4XC  *   JI@   1UP  2   A5  880",
                "AS5" : " ‡/4  H   AMX0  2 Q G J   W. 0 DP‡  S   7&AM     ‡/4G   *  MX0 D 3  1   AS5 932\n1 @EQ4S J   8. N D ‡  S H 7 AM  Y#2   G-  KV . 0 D  Q S J 7&   N D  2   AS5 932",
                "B5" : ",-   2/%1& A    ULB1   VMC   4W  VPF5U    G - 8XR   &9YP  * 0 1 ,-  1   B5  987\n1@ - J . % T A⌑   UL 1 D S C O 4T   PF U 7 Q  PI8X   Q&9 P ‡    1@  2   B5  987",
                "C6" : "&9 $&  VM8  I *UL    7$&K V    I8* L  UH7  KA TK6 I * SJ  H7   %$   1   C6  1046"
}



# Note frequencies (for testing)
note_frequencies = {
    'C3': 130.81, 'CS3': 138.59, 'D3': 146.83, 'DS3': 155.56, 'E3': 164.81, 'F3': 174.61, 'FS3': 185.00, 'G3': 196.00, 'GS3': 207.65, 'A3': 220.00, 'AS3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'CS4': 277.18, 'D4': 293.66, 'DS4': 311.13, 'E4': 329.63, 'F4': 349.23, 'FS4': 369.99, 'G4': 392.00, 'GS4': 415.30, 'A4': 440.00, 'AS4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'CS5': 554.37, 'D5': 587.33, 'DS5': 622.25, 'E5': 659.26, 'F5': 698.46, 'FS5': 739.99, 'G5': 783.99, 'GS5': 830.61, 'A5': 880.00, 'AS5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'CS6': 1108.73, 'D6': 1174.66, 'DS6': 1244.51, 'E6': 1318.51, 'F6': 1396.91, 'FS6': 1479.98, 'G6': 1567.98, 'GS6': 1661.22, 'A6': 1760.00, 'AS6': 1864.66, 'B6': 1975.53, "Rest": 0
}

instruments_midiNumbers = {
    'Acoustic Grand Piano': 0, 'Bright Acoustic Piano': 1, 'Electric Grand Piano': 2, 'Honky-tonk Piano': 3, 'Electric Piano 1': 4, 'Electric Piano 2': 5, 'Harpsichord': 6, 'Clavinet': 7, 'Celesta': 8, 'Glockenspiel': 9, 'Music Box': 10, 'Vibraphone': 11, 'Marimba': 12, 'Xylophone': 13, 'Tubular Bells': 14, 'Dulcimer': 15, 'Drawbar Organ': 16, 'Percussive Organ': 17, 'Rock Organ': 18, 'Church Organ': 19, 'Reed Organ': 20, 'Accordion': 21, 'Harmonica': 22, 'Tango Accordion': 23, 'Acoustic Guitar (nylon)': 24, 'Acoustic Guitar (steel)': 25, 'Electric Guitar (jazz)': 26, 'Electric Guitar (clean)': 27, 'Electric Guitar (muted)': 28, 'Overdriven Guitar': 29, 'Distortion Guitar': 30, 'Guitar Harmonics': 31, 'Acoustic Bass': 32, 'Electric Bass (finger)': 33, 'Electric Bass (pick)': 34, 'Fretless Bass': 35, 'Slap Bass 1': 36, 'Slap Bass 2': 37, 'Synth Bass 1': 38, 'Synth Bass 2': 39, 'Violin': 40, 'Viola': 41, 'Cello': 42, 'Contrabass': 43, 'Tremolo Strings': 44, 'Pizzicato Strings': 45, 'Orchestral Harp': 46, 'Timpani': 47, 'String Ensemble 1': 48, 'String Ensemble 2': 49, 'SynthStrings 1': 50, 'SynthStrings 2': 51, 'Choir Aahs': 52, 'Voice Oohs': 53, 'Synth Voice': 54, 'Orchestra Hit': 55, 'Trumpet': 56, 'Trombone': 57, 'Tuba': 58, 'Muted Trumpet': 59, 'French Horn': 60, 'Brass Section': 61, 'SynthBrass 1': 62, 'SynthBrass 2': 63, 'Soprano Sax': 64, 'Alto Sax': 65, 'Tenor Sax': 66, 'Baritone Sax': 67, 'Oboe': 68, 'English Horn': 69, 'Bassoon': 70, 'Clarinet': 71, 'Piccolo': 72, 'Flute': 73, 'Recorder': 74, 'Pan Flute': 75, 'Blown Bottle': 76, 'Shakuhachi': 77, 'Whistle': 78, 'Ocarina': 79, 'Lead 1 (square)': 80, 'Lead 2 (sawtooth)': 81, 'Lead 3 (calliope)': 82, 'Lead 4 (chiff)': 83, 'Lead 5 (charang)': 84, 'Lead 6 (voice)': 85, 'Lead 7 (fifths)': 86, 'Lead 8 (bass + lead)': 87, 'Pad 1 (new age)': 88, 'Pad 2 (warm)': 89, 'Pad 3 (polysynth)': 90, 'Pad 4 (choir)': 91, 'Pad 5 (bowed)': 92, 'Pad 6 (metallic)': 93, 'Pad 7 (halo)': 94, 'Pad 8 (sweep)': 95, 'FX 1 (rain)': 96, 'FX 2 (soundtrack)': 97, 'FX 3 (crystal)': 98, 'FX 4 (atmosphere)': 99, 'FX 5 (brightness)': 100, 'FX 6 (goblins)': 101, 'FX 7 (echoes)': 102, 'FX 8 (sci-fi)': 103, 'Sitar': 104, 'Banjo': 105, 'Shamisen': 106, 'Koto': 107, 'Kalimba': 108, 'Bagpipe': 109, 'Fiddle': 110, 'Shanai': 111, 'Tinkle Bell': 112, 'Agogo': 113, 'Steel Drums': 114, 'Woodblock': 115, 'Taiko Drum': 116, 'Melodic Tom': 117, 'Synth Drum': 118, 'Reverse Cymbal': 119, 'Guitar Fret Noise': 120, 'Breath Noise': 121, 'Seashore': 122, 'Bird Tweet': 123, 'Telephone Ring': 124, 'Helicopter': 125, 'Applause': 126, 'Gunshot': 127
}

noteNames = set([]) #Set of unique frequencies

def extract_melody_notes(file_path, instrumentName):
    # Load MIDI file
    midi_data = pretty_midi.PrettyMIDI("test_songs/"+file_path)

    # Get the instrument (assuming it's the first instrument)
    # You may need to modify this based on your MIDI file structure

    melody_notes = []
    instrument = pretty_midi.Instrument(0)
    try:
        selectedInstrument = instruments_midiNumbers[instrumentName]
        instruments = midi_data.instruments
        for possibleInstrument in instruments:
            if possibleInstrument.program == selectedInstrument and len(possibleInstrument.notes) > len(instrument.notes):
                instrument = possibleInstrument
    except:
        pass

    if len(instrument.notes) == 0:
        print("instrument could not be found")
        return melody_notes


    # Extract notes and their properties
    tempoChanges = midi_data.get_tempo_changes()
    tempoTimes = tempoChanges[0].tolist()
    tempos = tempoChanges[1].tolist()
    currentTempoIndex = 0
    currentTempo = tempos[currentTempoIndex]
    removeableNotes = []

    for i in range(len(instrument.notes)): #If multiple notes start at a time while another note is already playing, reduce to only playing the highest note
        j = i+1
        while j < len(instrument.notes):
            note1 = instrument.notes[i]
            note2 = instrument.notes[j]
            if note1.start >= note2.start:
                if note1.pitch > note2.pitch:
                    removeableNotes.append(note2)
                else:
                    removeableNotes.append(note1)
            j+=1

    pastNote = None

    durationFactor = 1

    for i in range(len(instrument.notes)):
        note = instrument.notes[i]
        duration = ((note.end-note.start)*(currentTempo/60))*4
        if round(duration) == 0:
            durationFactor = 2

    for i in range(len(instrument.notes)):
        
        note = instrument.notes[i]

        currentTempo = tempos[currentTempoIndex]

        if note.pitch < 48 or note.pitch > 84 or note in removeableNotes: #removes unneeded or unplayable notes
            instrument.notes[i] = None
            continue
        
        if i == 0 or pastNote == None or i == len(instrument.notes)-1 or (i < len(instrument.notes)-1 and (pastNote.end <= note.start or note.end != pastNote.start and abs(pastNote.pitch-note.pitch) < 12)): #remove any notes that start during a rest but then overlap another note
            
            note_name = pretty_midi.note_number_to_name(note.pitch)
            
            if currentTempoIndex < len(tempos)-1 and note.start >= tempoTimes[currentTempoIndex]+1: #switch tempos if the song switches tempo
                currentTempoIndex+=1

            noteNames.add(note_name)
            duration = ((note.end-note.start)*(currentTempo/60))*4*durationFactor

            if pastNote is not None and round((note.start)*(currentTempo/60),2)-round((pastNote.end)*(currentTempo/60),2) > 0.5: #add rests if the time between notes is greater than 0.2; this is a margin I made up but is necessary
                
                restDuration = round((note.start-pastNote.end)*(currentTempo/60)*4*durationFactor)

                while restDuration-8 >= 0: #split the rest into multiple rests so that the computer can process them correctly
                    restDuration-=8
                    melody_notes.append(["Rest",8,round((pastNote.end)*(currentTempo/60),2),round((note.start)*(currentTempo/60),2)])
                
                while restDuration-4 >= 0: #split the rest into multiple rests so that the computer can process them correctly
                    restDuration-=4
                    melody_notes.append(["Rest",4,round((pastNote.end)*(currentTempo/60),2),round((note.start)*(currentTempo/60),2)])

                if restDuration > 0:
                    melody_notes.append(["Rest",restDuration, round((pastNote.end)*(currentTempo/60),2),round((note.start)*(currentTempo/60),2)])
            
            melody_notes.append([note_name, round(duration), round((note.start)*(currentTempo/60),2),round((note.end)*(currentTempo/60),2)])
            pastNote = note  

    return melody_notes

# Specify the path to your MIDI file
midi_file_path = "Michael Jackson - Beat It.mid"

# Extract the melody notes from the MIDI file
melody_notes = extract_melody_notes(midi_file_path,"Lead 8 (bass + lead)")

def sortFreqs(freqSet):
    tempList = list(freqSet)
    tempList.sort(key=pretty_midi.note_name_to_number)
    return tempList

def convert_to_print(noteList):
    #Converts list of notes to print format, write to output file
    #Parameters: List of notes (each note is a list of [str: note name, int: duration])
    #Returns: None
    freqList = sortFreqs(noteNames)

    for idx, note in enumerate(freqList):
        if note[1] == '#':
            freqList[idx] = note[0] + 'S' + note[2:]

    for idx, note in enumerate(noteList): #Check that all notes are between C3 and C6
        name = note[0]
        if name != "Rest":
            if (int(name[-1]) < 3) or (int(name[-1]) >= 6):
                if not (name == "C4" or name == "C6" or name == "BS3"): #Edges of playable range
                    print(f'Error: note {name} out of range')
                    return
        if name[1] == '#':
            noteList[idx][0] = name[0] + 'S' + name[2:]

    with open("output.txt", 'w', encoding="utf-8") as output:
        for freq in freqList:
            line = note_lines[freq]
            output.write(f'{line}\n')
        
        diffFrequencies = len(freqList)
        maxNumberOfNotes = floor((4000-75*diffFrequencies)/11)
        print("Max Number of Notes: ", maxNumberOfNotes)
        output.write("END\n")
        for i, note in enumerate(noteList):
            if i > maxNumberOfNotes:
                print("SONG LIMIT REACHED")
                return
            output.write(f'{note[0]} {note[1]}\n')

def play_note(note, duration=1.0): #for testing the music output
    print(note)
    frequency = note_frequencies[note]
    t = np.linspace(0, duration, int(44100 * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(wave, samplerate=44100)
    sd.wait()


for note in melody_notes:
    print(f"{note[0]} {note[1]}")
convert_to_print(melody_notes)



for note in melody_notes: #for testing the music output
    play_note(note[0],note[1]/8)


