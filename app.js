const express = require('express');
const path = require('path');
const app = express();



app.use('/images',express.static('images'));
app.use('/css', express.static('css'));

app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname,'index.html'));
});

app.listen(8080);