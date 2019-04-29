var express = require('express');
var app = express();

app.get('/', function (req, res) {
    res.sendFile('D:/Users/jose.herrera/Documents/www/PersonalWebPage/home.html');
});

app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});