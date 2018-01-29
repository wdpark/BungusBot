var page = require('webpage').create();
var loadInProgress = false;
var testindex = 0;

console.log("hey")
page.onConsoleMessage = function(msg) {
    console.log(msg);
};

var steps = [
    function() {
        page.open('https://www.twitch.tv/lilypichu');
    },

    function() {
      page.includeJs('https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js', function() {
        page.evaluate(function() {
            $('#button.pl-clips-button').click();
            console.log('Clicked');
        });
      })
    },

    function() {
        page.evaluate(function() {
          console.log(document.body.getElementsByClassName("whatever"))
        });
    }
];

interval = setInterval(function() {
    if (!loadInProgress && typeof steps[testindex] == "function") {
        console.log("step " + (testindex + 1));
        steps[testindex]();
        testindex++;
    }
    if (typeof steps[testindex] != "function") {
        console.log("test complete!");
        phantom.exit();
    }
}, 500);
