
const add_phone_button = document.getElementById('add-phone-button')
add_phone_button.addEventListener('click',(e)=>{
        e.preventDefault();
        document.getElementById('user-phone').removeAttribute('disabled');
        e.target.setAttribute("style","display:none;")
        document.getElementById("user-phone-button-submit").removeAttribute('style');
        document.getElementById("cancel-edit").removeAttribute('style')     
});

const cancel_button_image = document.getElementById('cancel-edit');
cancel_button_image.addEventListener('click',(e)=>{
    e.preventDefault()
        document.getElementById('user-phone').setAttribute('disabled', "disabled");
        document.getElementById('user-phone-button-submit').setAttribute('style','display:none;')
        e.target.setAttribute('style','display:none;')
        document.getElementById('add-phone-button').removeAttribute('style')
    });

