mpcookie = {
    'counter': 0,
    'question': true
};

mpcookie.incr_xhr = new XMLHttpRequest();
mpcookie.incr_xhr.onload = function() {
    console.log(this.response);
    mpcookie.clicks.innerHTML = JSON.parse(this.response).clicks
};

mpcookie.save_clicks = function() {
    if (mpcookie.counter > 0) {
        mpcookie.incr_xhr.open("POST", "/incr/");
        mpcookie.incr_xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8')
        mpcookie.incr_xhr.send(JSON.stringify({'clicks' : mpcookie.counter}))
        mpcookie.counter = 0;
    }
};

mpcookie.handle_click = function() {
    mpcookie.counter++;
    mpcookie.clicks.innerHTML = parseInt(mpcookie.clicks.innerHTML) + 1;
};

window.onload = function(){
    mpcookie.clicks = document.getElementById("clicks");
    setInterval(mpcookie.save_clicks, 2000)
}

window.onbeforeunload = function() {
    if (mpcookie.counter != 0){
        if (mpcookie.question) {
            mpcookie.save_clicks();
            mpcookie.question = !mpcookie.question;
            return "Do you really want to stop clicking?"
        }
        return "Please wait while we save your progress"
    }
}