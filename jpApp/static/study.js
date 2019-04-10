"use strict";

function updateStudyDb() {
    console.log("hey");
    let req = new XMLHttpRequest();
    let query = "id=" + id;
    console.log(id);
    console.log(query);

    
    req.open('POST', 'http://localhost:5000/study/addStudiedWord?'+query, true);
    req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    req.onload = function(data, code) {
	document.location.reload(true);
    }
    req.send(query);    
    
}

function loadPage(url) {
    let req = new XMLHttpRequest();
    req.open('GET', url, true);
    req.send();
    return req.responseText;
}



function goNext() {
    updateStudyDb('http://localhost:5000/study/' + level);
}
