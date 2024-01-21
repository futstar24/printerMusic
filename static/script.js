const midiInstruments = ['Acoustic Grand Piano', 'Bright Acoustic Piano', 'Electric Grand Piano', 'Honky-tonk Piano', 'Electric Piano 1', 'Electric Piano 2', 'Harpsichord', 'Clavinet', 'Celesta', 'Glockenspiel', 'Music Box', 'Vibraphone', 'Marimba', 'Xylophone', 'Tubular Bells', 'Dulcimer', 'Drawbar Organ', 'Percussive Organ', 'Rock Organ', 'Church Organ', 'Reed Organ', 'Accordion', 'Harmonica', 'Tango Accordion', 'Acoustic Guitar (nylon)', 'Acoustic Guitar (steel)', 'Electric Guitar (jazz)', 'Electric Guitar (clean)', 'Electric Guitar (muted)', 'Overdriven Guitar', 'Distortion Guitar', 'Guitar Harmonics', 'Acoustic Bass', 'Electric Bass (finger)', 'Electric Bass (pick)', 'Fretless Bass', 'Slap Bass 1', 'Slap Bass 2', 'Synth Bass 1', 'Synth Bass 2', 'Violin', 'Viola', 'Cello', 'Contrabass', 'Tremolo Strings', 'Pizzicato Strings', 'Orchestral Harp', 'Timpani', 'String Ensemble 1', 'String Ensemble 2', 'Synth Strings 1', 'Synth Strings 2', 'Choir Aahs', 'Voice Oohs', 'Synth Voice', 'Orchestra Hit', 'Trumpet', 'Trombone', 'Tuba', 'Muted Trumpet', 'French Horn', 'Brass Section', 'Synth Brass 1', 'Synth Brass 2', 'Soprano Sax', 'Alto Sax', 'Tenor Sax', 'Baritone Sax', 'Oboe', 'English Horn', 'Bassoon', 'Clarinet', 'Piccolo', 'Flute', 'Recorder', 'Pan Flute', 'Blown Bottle', 'Shakuhachi', 'Whistle', 'Ocarina', 'Lead 1 (Square)', 'Lead 2 (Sawtooth)', 'Lead 3 (Calliope)', 'Lead 4 (Chiff)', 'Lead 5 (Charang)', 'Lead 6 (Voice)', 'Lead 7 (Fifths)', 'Lead 8 (Bass + Lead)', 'Pad 1 (New Age)', 'Pad 2 (Warm)', 'Pad 3 (Polysynth)', 'Pad 4 (Choir)', 'Pad 5 (Bowed)', 'Pad 6 (Metallic)', 'Pad 7 (Halo)', 'Pad 8 (Sweep)', 'FX 1 (Rain)', 'FX 2 (Soundtrack)', 'FX 3 (Crystal)', 'FX 4 (Atmosphere)', 'FX 5 (Brightness)', 'FX 6 (Goblins)', 'FX 7 (Echoes)', 'FX 8 (Sci-fi)', 'Sitar', 'Banjo', 'Shamisen', 'Koto', 'Kalimba', 'Bagpipe', 'Fiddle', 'Shanai', 'Tinkle Bell', 'Agogo', 'Steel Drums', 'Woodblock', 'Taiko Drum', 'Melodic Tom', 'Synth Drum', 'Reverse Cymbal', 'Guitar Fret Noise', 'Breath Noise', 'Seashore', 'Bird Tweet', 'Telephone Ring', 'Helicopter', 'Applause', 'Gunshot'];

const note_frequencies = {
    'C3': 130.81, 'CS3': 138.59, 'D3': 146.83, 'DS3': 155.56, 'E3': 164.81, 'F3': 174.61, 'FS3': 185.00, 'G3': 196.00, 'GS3': 207.65, 'A3': 220.00, 'AS3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'CS4': 277.18, 'D4': 293.66, 'DS4': 311.13, 'E4': 329.63, 'F4': 349.23, 'FS4': 369.99, 'G4': 392.00, 'GS4': 415.30, 'A4': 440.00, 'AS4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'CS5': 554.37, 'D5': 587.33, 'DS5': 622.25, 'E5': 659.26, 'F5': 698.46, 'FS5': 739.99, 'G5': 783.99, 'GS5': 830.61, 'A5': 880.00, 'AS5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'CS6': 1108.73, 'D6': 1174.66, 'DS6': 1244.51, 'E6': 1318.51, 'F6': 1396.91, 'FS6': 1479.98, 'G6': 1567.98, 'GS6': 1661.22, 'A6': 1760.00, 'AS6': 1864.66, 'B6': 1975.53, "Rest": 0
}

midiInstruments.forEach((instrument) => {
    const option = document.createElement("option");
    option.value = instrument;
    option.text = instrument;
    instruments.add(option);
  });

playButton.addEventListener("click", function() {
    recieveMusic()
})

resetSong()

document.getElementById("button").addEventListener("click", function() {

    const formData = new FormData();
    formData.append("midiFile", fileInput.files[0]);
    formData.append("instrument", instruments.value)
    if (fileInput.files.length > 0) {
        fetch("/uploader", {
            method: "POST",
            body: formData,
        }).then(respone => respone.json()).then(function(data) {
            if (data["result"] == "success") {
                loadedSong.style.opacity = "1"
                downloadSong.style.pointerEvents="auto";
                downloadSong.style.cursor="pointer";
                alert("Success! Your Song File was Created!")
            }
            else {
                alert("Insturment Not Found in Song File")

            }
        })
    }

})

document.getElementById("fileInput").addEventListener("click", function() {
    resetSong()
})

instruments.addEventListener("change", function() {
    resetSong()
})

function resetSong() {
    loadedSong.style.opacity = "0"
    downloadSong.style.pointerEvents="none";
    downloadSong.style.cursor="default"
    fetch("/resetSong").then(respone => respone.json()).then(function(data) {
        console.log(data["result"])
    })
    ableToPlay = false
}


stopButton.addEventListener("click", function() {
    ableToPlay = false
})

maxNotes = 20
noteIndex = 0
timeFactor = 8
ableToPlay = true

function recieveMusic() {
    fetch("/sendMusicData").then(respone => respone.json()).then(function(data) {
        rawNoteList = data["noteList"]
        noteList = []
        for (var i = 0; i < rawNoteList.length; i++) {
            note = []
            note.push(rawNoteList[i][0])
            note.push(rawNoteList[i][1])
            noteList.push(note)
        }
        noteIndex = 0
        ableToPlay = true
        playSong(noteList)
    })
}

function playSong(noteList) {
    if (noteIndex < maxNotes && ableToPlay) {
        duration = 0
        if (noteIndex != 0) {
            duration = noteList[noteIndex-1][1]
        }
        console.log(duration)
        setTimeout(function() {
            note = noteList[noteIndex]
            duration = 1000
            playNote(note[0],note[1]/timeFactor)
            noteIndex += 1
            playSong(noteList)
        }, (duration*1000)/(timeFactor))
    }
} 


function playNote(note, duration = 1.0) {
    try {
        frequency = note_frequencies[note]
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime); // Adjust frequency
        oscillator.connect(audioContext.destination)
        oscillator.start();
        oscillator.stop(audioContext.currentTime + duration);
    }
    catch (error) {
        console.log("Rest")
    }

}
