function messageHandler(event) {
    if (event.source !== window) return;
    if (event.data) chrome.runtime.sendMessage(event.data);
}

window.addEventListener("message", messageHandler);


