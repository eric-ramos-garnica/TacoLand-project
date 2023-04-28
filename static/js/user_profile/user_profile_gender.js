const addGenderBtn = document.getElementById("add-gender-button");
    addGenderBtn.addEventListener("click", function(e) {
        e.preventDefault()
        document.getElementById("gender").removeAttribute('disabled');
        e.target.setAttribute("style","display:none;")
        document.getElementById("user-gender-button-submit").removeAttribute('style');
        document.getElementById("cancel-edit-gender").removeAttribute('style')  
    });

    const cancel_button_genders = document.getElementById("cancel-edit-gender")
    cancel_button_genders.addEventListener('click',(e)=>{
        e.preventDefault()
        document.getElementById('gender').setAttribute('disabled', "disabled");
        e.target.setAttribute('style','display:none');
        document.getElementById("add-gender-button").removeAttribute('style');
        document.getElementById("user-gender-button-submit").setAttribute('style','display:none;')

    });
