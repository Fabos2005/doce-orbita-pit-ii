'use strict';
document.querySelectorAll('form[data-confirm]').forEach(form=>{
 const button=form.querySelector('button');const original=button.textContent;let pending=false;let notice,cancel;
 const reset=()=>{pending=false;notice.remove();cancel.remove();button.textContent=original;button.focus();};
 form.addEventListener('submit',event=>{if(pending)return;event.preventDefault();pending=true;notice=document.createElement('p');notice.setAttribute('role','status');notice.textContent=form.dataset.confirm;cancel=document.createElement('button');cancel.type='button';cancel.textContent='Manter pedido';cancel.className='secondary';cancel.addEventListener('click',reset);button.textContent='Confirmar cancelamento';form.prepend(notice);form.append(cancel);cancel.focus();});
 form.addEventListener('keydown',event=>{if(pending&&event.key==='Escape'){event.preventDefault();reset();}});
});
