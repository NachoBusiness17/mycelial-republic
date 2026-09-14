// deep extraction payload - runs IN the page via evaluate
(() => {
  const html = document.documentElement.outerHTML;
  const fetches = [...new Set((html.match(/fetch\((['"`])([^'"`]+)\1/g) || [])
    .map(m => m.replace(/fetch\((['"`])/, '').replace(/['"`]$/, '')))].slice(0, 14);
  const apiRefs = [...new Set(html.match(/\/api\/[a-z0-9\/_\-\.]*/g) || [])].slice(0, 12);
  const wsRefs = [...new Set(html.match(/(ws|wss):\/\/[^\s'"`]+/g) || [])].slice(0, 5);
  return {
    title: document.title,
    links: [...new Set([...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')))].slice(0, 30),
    scripts: [...document.querySelectorAll('script[src]')].map(s => s.getAttribute('src')),
    inlineScripts: document.querySelectorAll('script:not([src])').length,
    fetches: fetches,
    apiRefs: apiRefs,
    wsRefs: wsRefs,
    iframes: [...document.querySelectorAll('iframe')].map(f => f.src).slice(0, 5),
    bodyChars: document.body.innerText.length,
    elements: document.querySelectorAll('*').length,
    intervals: (html.match(/setInterval\(/g) || []).length,
    eventSource: html.includes('EventSource'),
    websockets: html.includes('WebSocket')
  };
})()
