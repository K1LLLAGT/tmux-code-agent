const terminal=document.querySelector('#terminal');
const viewport=window.visualViewport;
function fit(){if(viewport) terminal.style.height=`${Math.max(180,viewport.height-180)}px`;}
viewport?.addEventListener('resize',fit);fit();
terminal.textContent='Terminal channel ready';
