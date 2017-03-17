var canva = document.getElementById("desighCanvas");
var lienzo = canva.getContext("2d");

console.log(canva)
var grd = lienzo.createLinearGradient(0,0,canva.width,0);
grd.addColorStop(0,"red");
grd.addColorStop(1,"white");

// Fill with gradient
lienzo.fillStyle = grd;
lienzo.fillRect(10,10,150,80);