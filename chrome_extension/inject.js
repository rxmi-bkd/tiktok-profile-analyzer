const originalFetch = window.fetch;

async function newFetch(...args) {
    const response = await originalFetch.apply(this, args);
    const url = typeof args[0] === 'string' ? args[0] : args[0]?.url;

    if (url && url.startsWith('https://www.tiktok.com/api/post/item_list/')) {
        response
            .clone()
            .json()
            .then(response => window.postMessage(response));
    }

    return response;
}

window.fetch = newFetch;