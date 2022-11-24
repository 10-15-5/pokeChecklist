function kantoSelectAll(source) {
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
    var checked = document.querySelectorAll('input:checked');
    
    if(checked.length === 0){
        document.getElementById('submitBtn').disabled = true;
    }
    else{
        document.getElementById('submitBtn').disabled = false;
    }
}