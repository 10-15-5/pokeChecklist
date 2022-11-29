function kantoSelectAll(source) {
    // Function to select all and deselect all Kanto Pokemon

    checkboxes = document.getElementsByName('pokemon');
    var checked = document.querySelectorAll('input:checked');

    if(checked.length == checkboxes.length){
        for(var i=0;i<checkboxes.length;i++) {
            checkboxes[i].checked = false;
        }
    }
    else{
        for(var i=0;i<checkboxes.length;i++) {
            checkboxes[i].checked = true;
        }
    }
}

function kantoHideCaught(source) {
    // Function to hide and show the Pokemon that have been checked

    var checked = document.querySelectorAll('input:checked');

    if(document.getElementById("hide-caught").value === "Hide Caught"){
        for(var i=0;i<checked.length;i++){
            div = document.getElementById('pokemon-div-' + checked[i].value);
            div.style.display = "none";
        }
        document.getElementById("hide-caught").value = "Show Caught";
    }
    else{
        for(var i=0;i<checked.length;i++){
            div = document.getElementById('pokemon-div-' + checked[i].value);
            div.style.display = "block";
        }
        document.getElementById("hide-caught").value = "Hide Caught";
    }
}

function validateSubmit() {
    // If none of the Pokemon have been checked, the submit button becomes disabled

    var checked = document.querySelectorAll('input:checked');
    
    if(checked.length === 0){
        document.getElementById('submitBtn').disabled = true;
    }
    else{
        document.getElementById('submitBtn').disabled = false;
    }
}