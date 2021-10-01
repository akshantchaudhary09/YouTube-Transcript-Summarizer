function generateSummary(url){
    function reqListener () {
        chrome.runtime.sendMessage({action: "result", summary: this.responseText});
        // console.log(this.responseText);
    }
    var _url = "http://127.0.0.1:5000/api/summarize?youtube_url=" + url
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("GET", _url);
    oReq.send();
    // console.log(_url);
}

chrome.runtime.onMessage.addListener(function(message){
    if(message.action === 'generate'){
        // console.log("inside contentScirpt...");
        generateSummary(message.currUrl);
    }
});