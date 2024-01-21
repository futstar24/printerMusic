
document.getElementById("fileInput").addEventListener("change", function() {
    fetch('/removeOldFiles', {
        method: "POST",
        })
    downloadButton.style.opacity = "0"
    downloadButton.style.pointerEvents="none";
    downloadButton.style.cursor="default"
})


downloadButton.style.pointerEvents="none";
downloadButton.style.cursor="default"

function handleResult() {
    setTimeout(fullyHandleResult, 1000)
}

function fullyHandleResult() {
    fetch("output.txt")
    .then(response => response.text()) 
    .then(textString => {
        if (textString == "FAIL") {
            alert("The instrument inputted is not in your song.")
            downloadButton.style.pointerEvents="none";
            downloadButton.style.cursor="default"
        } else {
            alert("Success! Download the output file to see your song code!")
            downloadButton.style.opacity = "1"
            downloadButton.style.pointerEvents="auto";
            downloadButton.style.cursor="pointer";
        }
    })     
    
}

const midiInstruments = ['Acoustic Grand Piano', 'Bright Acoustic Piano', 'Electric Grand Piano', 'Honky-tonk Piano', 'Electric Piano 1', 'Electric Piano 2', 'Harpsichord', 'Clavinet', 'Celesta', 'Glockenspiel', 'Music Box', 'Vibraphone', 'Marimba', 'Xylophone', 'Tubular Bells', 'Dulcimer', 'Drawbar Organ', 'Percussive Organ', 'Rock Organ', 'Church Organ', 'Reed Organ', 'Accordion', 'Harmonica', 'Tango Accordion', 'Acoustic Guitar (nylon)', 'Acoustic Guitar (steel)', 'Electric Guitar (jazz)', 'Electric Guitar (clean)', 'Electric Guitar (muted)', 'Overdriven Guitar', 'Distortion Guitar', 'Guitar Harmonics', 'Acoustic Bass', 'Electric Bass (finger)', 'Electric Bass (pick)', 'Fretless Bass', 'Slap Bass 1', 'Slap Bass 2', 'Synth Bass 1', 'Synth Bass 2', 'Violin', 'Viola', 'Cello', 'Contrabass', 'Tremolo Strings', 'Pizzicato Strings', 'Orchestral Harp', 'Timpani', 'String Ensemble 1', 'String Ensemble 2', 'Synth Strings 1', 'Synth Strings 2', 'Choir Aahs', 'Voice Oohs', 'Synth Voice', 'Orchestra Hit', 'Trumpet', 'Trombone', 'Tuba', 'Muted Trumpet', 'French Horn', 'Brass Section', 'Synth Brass 1', 'Synth Brass 2', 'Soprano Sax', 'Alto Sax', 'Tenor Sax', 'Baritone Sax', 'Oboe', 'English Horn', 'Bassoon', 'Clarinet', 'Piccolo', 'Flute', 'Recorder', 'Pan Flute', 'Blown Bottle', 'Shakuhachi', 'Whistle', 'Ocarina', 'Lead 1 (Square)', 'Lead 2 (Sawtooth)', 'Lead 3 (Calliope)', 'Lead 4 (Chiff)', 'Lead 5 (Charang)', 'Lead 6 (Voice)', 'Lead 7 (Fifths)', 'Lead 8 (Bass + Lead)', 'Pad 1 (New Age)', 'Pad 2 (Warm)', 'Pad 3 (Polysynth)', 'Pad 4 (Choir)', 'Pad 5 (Bowed)', 'Pad 6 (Metallic)', 'Pad 7 (Halo)', 'Pad 8 (Sweep)', 'FX 1 (Rain)', 'FX 2 (Soundtrack)', 'FX 3 (Crystal)', 'FX 4 (Atmosphere)', 'FX 5 (Brightness)', 'FX 6 (Goblins)', 'FX 7 (Echoes)', 'FX 8 (Sci-fi)', 'Sitar', 'Banjo', 'Shamisen', 'Koto', 'Kalimba', 'Bagpipe', 'Fiddle', 'Shanai', 'Tinkle Bell', 'Agogo', 'Steel Drums', 'Woodblock', 'Taiko Drum', 'Melodic Tom', 'Synth Drum', 'Reverse Cymbal', 'Guitar Fret Noise', 'Breath Noise', 'Seashore', 'Bird Tweet', 'Telephone Ring', 'Helicopter', 'Applause', 'Gunshot'];

midiInstruments.forEach((instrument) => {
    const option = document.createElement("option");
    option.value = instrument;
    option.text = instrument;
    instruments.add(option);
  });



document.getElementById("button").addEventListener("click", function() {
    

    if (fileInput.files.length > 0) {

        const fileInput = document.getElementById('fileInput');
        const uploadedFile = fileInput.files[0];
        const dataToSend = new FormData()
        dataToSend.append("file",uploadedFile)
        console.log(instruments.value)

        fetch('/saveFile', {
            method: "POST",
            
            body: dataToSend
            })
        
        

        fetch('/saveInstrument', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data:  instruments.value}),
        }) 
        
        
        
        
        
        
        
        
        fetch('/makeSong', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(),
            })
            .then(response => response.json())
            .then(data => {
            handleResult(data.result);
            })
            .catch(error => {
            console.error('Error:', error);
            });

    }
    /*const fileInput = document.getElementById('fileInput');
      
    if (fileInput.files.length > 0) {
      const uploadedFile = fileInput.files[0];

      const reader = new FileReader();
      reader.onload = function (event) {
        const fileContent = event.target.result;

        // Here, you can perform actions with the file content
        // For example, you can create a new file using Blob and download it

        //const dataToSend = {"file":new Blob([fileContent], { type: uploadedFile.type }),"type":uploadedFile.type}
        fetch('http://localhost:8080/saveFile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(),
        })
        .then(response => response.json())
        .then(data => {
        console.log('Result from server:', data.result);
        })
        .catch(error => {
        console.error('Error:', error);
        });
        fetch('http://localhost:8080/runCode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(),
        })
        .then(response => response.json())
        .then(data => {
        console.log('Result from server:', data.result);
        })
        .catch(error => {
        console.error('Error:', error);
        });
        }
    } else {
      alert('Please select a file to upload.');
    }*/


    
})

