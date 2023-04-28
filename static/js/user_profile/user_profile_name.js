const edit_button_name = document.getElementById("edit-button-name")
        edit_button_name.addEventListener('click',(e)=>{
            e.target.setAttribute('style','display:none;');
            document.getElementById("edit-form-name").removeAttribute('style');
            document.getElementById("first-last-name").setAttribute('style','display:none;');
            document.getElementById("cancel-edit-name").removeAttribute("style");
        });

       const  cancel_button_name = document.getElementById("cancel-edit-name")
        cancel_button_name.addEventListener('click',(e)=>{
            document.getElementById("first-last-name").removeAttribute('style');
            document.getElementById("edit-form-name").setAttribute('style','display: none;');
            e.preventDefault();
            e.target.setAttribute('style','display: none;');
            edit_button_name.removeAttribute("style");
        });

