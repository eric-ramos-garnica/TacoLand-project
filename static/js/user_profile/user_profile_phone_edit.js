const edit_phone_button = document.getElementById('edit-button-phone');
edit_phone_button.addEventListener('click',(e)=>{
    document.getElementById('user-phone-edit').setAttribute('style','display: none;');
    document.getElementById('user-form-phone').removeAttribute('style');
    document.getElementById('cancel-edit').removeAttribute('style');
});

const cancel_button = document.getElementById('cancel-edit');
cancel_button.addEventListener('click',(e)=>{
    document.getElementById('user-form-phone').setAttribute('style','display: none;')
    document.getElementById('user-phone-edit').removeAttribute('style')
    e.preventDefault()
    e.target.setAttribute('style','display: none;')
});