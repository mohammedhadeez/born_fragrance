const key='born-fragrance-presentation-v1';
const main=document.querySelector('main');
const status=document.querySelector('#status');
try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(saved){main.innerHTML=saved.html;document.documentElement.style.setProperty('--accent',saved.accent);document.querySelector('#accent').value=saved.accent}}catch(e){status.textContent='Local save unavailable. Use Download edited HTML.'}
function renumber(){document.querySelectorAll('.folio').forEach((el,i)=>el.textContent=String(i+1).padStart(2,'0'))}
function persist(){try{localStorage.setItem(key,JSON.stringify({html:main.innerHTML,accent:document.querySelector('#accent').value}));status.textContent='Edits saved in this browser. Download HTML to keep or share a copy.'}catch(e){status.textContent='Browser storage is full or unavailable. Download HTML to keep edits.'}}
main.addEventListener('input',persist);
main.addEventListener('click',e=>{const button=e.target.closest('[data-move]');if(button){const page=button.closest('.page');const direction=Number(button.dataset.move);if(direction<0&&page.previousElementSibling)main.insertBefore(page,page.previousElementSibling);if(direction>0&&page.nextElementSibling)main.insertBefore(page.nextElementSibling,page);renumber();persist()}const swatch=e.target.closest('.swatch');if(swatch){const picker=document.createElement('input');picker.type='color';picker.value='#d9d4ca';picker.addEventListener('input',()=>{swatch.style.background=picker.value;persist()});picker.click()}});
let targetImage;
const upload=document.querySelector('#upload');
main.addEventListener('dblclick',e=>{if(e.target.matches('figure img')&&!document.body.classList.contains('readonly')){targetImage=e.target;upload.click()}});
main.addEventListener('keydown',e=>{if(e.target.matches('figure img')&&e.key==='Enter'){targetImage=e.target;upload.click()}});
upload.addEventListener('change',()=>{const file=upload.files[0];if(!file||!targetImage)return;const reader=new FileReader();reader.onload=()=>{targetImage.src=reader.result;persist()};reader.readAsDataURL(file);upload.value=''});
document.querySelector('#accent').addEventListener('input',e=>{document.documentElement.style.setProperty('--accent',e.target.value);persist()});
document.querySelector('#edit').onclick=e=>{const readonly=document.body.classList.toggle('readonly');main.querySelectorAll('[contenteditable]').forEach(el=>el.contentEditable=String(!readonly));e.target.textContent=readonly?'Editing off':'Editing on'};
document.querySelector('#print').onclick=()=>window.print();
document.querySelector('#save').onclick=()=>{const copy=document.documentElement.cloneNode(true);copy.querySelectorAll('[contenteditable]').forEach(el=>el.setAttribute('contenteditable','true'));copy.querySelector('body').classList.remove('readonly');copy.querySelector('#edit').textContent='Editing on';const blob=new Blob(['<!doctype html>\n'+copy.outerHTML],{type:'text/html'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='born-fragrance-presentation-edited.html';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};
document.querySelector('#reset').onclick=()=>{if(confirm('Clear browser-saved edits and reload this file? Download your edits first if you want to keep them.')){try{localStorage.removeItem(key)}catch(e){}location.reload()}};
renumber();
