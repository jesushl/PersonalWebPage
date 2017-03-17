function openTab(tabToShow) {
    var i;
    var x = document.getElementsByClassName("tabsInPersonalWeb");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none"; 
    }
    document.getElementById(tabToShow).style.display = "block"; 
}