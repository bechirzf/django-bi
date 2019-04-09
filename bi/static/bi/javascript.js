async function flushCache() {
    let response = await fetch('/api/flush-cache/');
    return await response.json();
}