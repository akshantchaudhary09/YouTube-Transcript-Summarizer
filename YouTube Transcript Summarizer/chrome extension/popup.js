const summarizeBtn = document.getElementById("summarize-btn");
summarizeBtn.onclick = function(e){
    e.preventDefault();
    document.getElementById("load").classList.add("loader");
    // console.log("working...");
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let url = tabs[0].url;
        chrome.tabs.sendMessage(tabs[0].id, {action: "generate", currUrl: url});
				// window.close();
    });
}
chrome.runtime.onMessage.addListener(function(message){
    if(message.action === 'result'){
        document.getElementById("load").classList.remove("loader");
        document.querySelector(".text").innerHTML = message.summary;
    }
});