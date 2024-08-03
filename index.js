const express = require('express');
const path = require('path')
const app = express();



app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname,'index.html'));
});

app.listen(8080, function () {
    console.log('Example app listening on port 8080!');
});