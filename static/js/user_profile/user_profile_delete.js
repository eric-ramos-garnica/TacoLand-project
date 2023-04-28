const button_delete = document.getElementById("delete-button")
        button_delete.addEventListener('click',(e)=>{
            e.target.setAttribute('style','display:none;');
            document.getElementById("par-delete").removeAttribute('style');
            document.getElementById("button-yes-delete").removeAttribute('style');
            document.getElementById("cancel-button-delete").removeAttribute('style');
        });
const button_cancel_delete = document.getElementById("cancel-button-delete");
    button_cancel_delete.addEventListener('click',(e)=>{
        e.preventDefault();
        document.getElementById("par-delete").setAttribute('style','display:none;');
        document.getElementById("button-yes-delete").setAttribute('style','display:none;');
        document.getElementById("cancel-button-delete").setAttribute('style','display:none;');
        document.getElementById("delete-button").removeAttribute('style');

    });