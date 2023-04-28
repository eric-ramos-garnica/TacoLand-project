const add_image_button = document.getElementById('add-image-button')
      
        // add photo
        add_image_button. addEventListener('click',(e)=>{
            
            e.preventDefault();
            document.getElementById('user-image').removeAttribute('style');
            e.target.setAttribute("style","display:none;")
            document.getElementById("user-image-button-submit").removeAttribute('style');
            document.getElementById("cancel-edit-img").removeAttribute('style')
        });
        cancel_button = document.getElementById("cancel-edit-img");
        cancel_button.addEventListener('click',(e)=>{
            document.getElementById("user-image").setAttribute('style','display:none;')
            document.getElementById("add-image-button").removeAttribute('style')
            document.getElementById('user-image-button-submit').setAttribute('style','display:none;');
            e.preventDefault()
            e.target.setAttribute('style', 'display:none;')
        });

        const edit_button_image = document.getElementById("add-image-button")
        edit_button_image.addEventListener('click',(e)=>{
            e.preventDefault()
            document.getElementById("user-image").removeAttribute('style');
            document.getElementById("user-image-button-submit").removeAttribute('style');
            document.getElementById("add-image-button").setAttribute('style', 'display:none;');
            document.getElementById("cancel-edit-img").removeAttribute('style')
        });


        const cancel_button_img = document.getElementById('cancel-edit-img');
        cancel_button_img.addEventListener('click',(e)=>{
            
            e.preventDefault()
            document.getElementById('user-image').setAttribute('style','display:none;');
            e.target.setAttribute('style','display:none;');
            document.getElementById('user-image-button-submit').setAttribute('style','display:none;');
            document.getElementById("add-image-button").removeAttribute('style');

        });