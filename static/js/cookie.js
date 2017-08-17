mpcookie={
    incr_xhr: new XMLHttpRequest(),
    handle_click: function(){
        incr_xhr.open("POST", '/incr/');
        incr_xhr.send(1)
    }
}
mpcookie.incr_xhr.onload: function (){
    document.getElementById("clicks").innerHTML = incr_xhr.response
}