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