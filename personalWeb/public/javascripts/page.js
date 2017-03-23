function openTab(tabToShow) {
    var i;
    var x = document.getElementsByClassName("tabsInPersonalWeb");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none"; 
    }
    document.getElementById(tabToShow).style.display = "block"; 
}

var slideProyectIndex;
function initSlides(){
    slideProyectIndex = 1;
    showProyectsDivs(slideProyectIndex);    
}


function proyectsDivs(n){
    showProyectsDivs(slideProyectIndex += n);
}

function showProyectsDivs(n){
    var i;
    var proyectsSlides = document.getElementsByClassName("proyectsSlides"); 
    if(n > proyectsSlides.length){ slideProyectIndex = 1 }
    if(n < 1) { slideProyectIndex = proyectsSlides.length }
    for(i = 0 ; i < proyectsSlides.length ; i++) {
        proyectsSlides[i].style.display="none";
    }
    proyectsSlides[slideProyectIndex-1].style.display = "block";
}