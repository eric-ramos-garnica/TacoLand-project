const cancel_button_name = document.getElementById("cancel-edit-name")
cancel_button_name.addEventListener('click',(e)=>{
    document.getElementById("first-last-name").removeAttribute('style');
    document.getElementById("edit-form-name").setAttribute('style','display: none;');
    e.preventDefault();
    e.target.setAttribute('style','display: none;');
    edit_button_name.removeAttribute("style");
});

