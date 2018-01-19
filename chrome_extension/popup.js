
chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    var url = tabs[0].url;
    console.log(url);
    document.getElementById("myText").innerHTML = url;
    
    //Extract youtube video id if on youtube, nothing otherwise
    var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
var match = url.match(regExp);
    if (match && match[2].length == 11) {
      document.getElementById("vidID").innerHTML = match[2];
    } else {
      document.getElementById("vidID").innerHTML = 'NONE DETECTED';//error
    }
});



document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('checkPage').addEventListener('click', function(){
      chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
        
        //get current url
    var url = tabs[0].url;

    //Extract youtube video id if on youtube, nothing otherwise
    var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
var match = url.match(regExp);
    if (match && match[2].length == 11) {
      var newURL = "http://localhost:5000/output?video_id=" + match[2];
         chrome.tabs.create({ url: newURL });
    } else {
    }
    
    
         
      });
});
});