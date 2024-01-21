/*onst express = require('express');
const path = require('path');
const app = express();
const { exec } = require('child_process');

app.use(express.static(path.join(__dirname, 'public')));
app.get('/', async(req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
app.listen(8080, () => {
    console.log("Server successfully running on port 8080");
  });

// Route to call the function
app.post('/callFunction', (req, res) => {
    const data = req.body; // Assuming you use a middleware like bodyParser to parse JSON
    const result = runcode();
    res.json({ result });
  });
  
function runcode() {
    console.log("start")
    const pythonScriptPath = 'printerMusicConversion.py';


    exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing Python script: ${error}`);
        return;
    }

    console.log(`Python script output:\n${stdout}`);
    console.error(`Python script errors:\n${stderr}`);
    });
}
*/

const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
const multer  = require('multer')

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const fs = require('fs');

function removeFilesInFolder(folderPath) {
    if (fs.existsSync(folderPath)) {
        fs.readdirSync(folderPath).forEach((file) => {
        const filePath = path.join(folderPath, file);

        if (fs.statSync(filePath).isFile()) {
            // Remove the file
            fs.unlinkSync(filePath);
        }
        });
    }
}

// setup multer for file upload
var storage = multer.diskStorage(
    {
        destination: './public/song',
        filename: function (req, file, cb ) {
            cb( null, file.originalname);
        }
    }
);
const upload = multer({ storage: storage } )

const { exec } = require('child_process');

app.use(express.static(path.join(__dirname, 'public')));
app.get('/', async(req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const port = process.env.PORT || 8080

// Middleware to parse JSON data
app.use(bodyParser.json());

// Your function
function runcode() {
    output = ""
    console.log("start")
    const pythonScriptPath = 'public/printerMusicConversion.py';


    exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing Python script: ${error}`);
        return;
    }

    console.log(`Python script output:\n${stdout}`);
    console.error(`Python script errors:\n${stderr}`);
    
    });
    console.log(output)
    
}


// API endpoint to call the function
app.post('/makeSong', (req, res) => {
  var result = runcode();

  res.json({ result });
});

app.post("/saveInstrument", (req,res) => {
    console.log(req.body.data)
    fs.writeFileSync("public/song/instrument.txt",req.body.data)
    res.sendStatus(200)
})

app.post("/removeOldFiles", (req, res) => {
    const folderPathToRemoveFiles = 'public/song';
    removeFilesInFolder(folderPathToRemoveFiles);
})

app.post('/saveFile', upload.single("file"), (req, res) => {
    
    // Example usage
    console.log(req.file.originalname + " file successfully uploaded !!");
    res.sendStatus(200);
});
  

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
