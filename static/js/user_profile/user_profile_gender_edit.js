const edit_gender_button = document.getElementById("edit-button-gender");
    edit_gender_button.addEventListener('click',(e)=>{
        e.preventDefault()
        document.getElementById("user-form-gender").removeAttribute('style')
        document.getElementById("gender-element").setAttribute('style','display:none;')
        document.getElementById("cancel-edit-gender").removeAttribute('style')
    });
    const cancel_button_gender = document.getElementById("cancel-edit-gender")
    cancel_button_gender.addEventListener('click',(e)=>{
        document.getElementById("user-form-gender").setAttribute('style','display:none;')
        document.getElementById("gender-element").removeAttribute('style')
        e.preventDefault()
        e.target.setAttribute("style","display:none;")
    });