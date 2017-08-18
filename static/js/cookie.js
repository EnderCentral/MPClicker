mpcookie = {};
mpcookie.incr_xhr = new XMLHttpRequest();
mpcookie.incr_xhr.onload = function () {
    document.getElementById("clicks").innerHTML = mpcookie.incr_xhr.response
};
mpcookie.handle_click = function () {
    mpcookie.incr_xhr.open("POST", "/incr/");
    mpcookie.incr_xhr.send(1)
};
