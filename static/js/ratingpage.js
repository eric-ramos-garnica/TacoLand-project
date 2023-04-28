rating_button = document.getElementById("rate-review-button")
    rating_button.addEventListener('click',(e)=>{
        form_rating = document.getElementById("rating-review-form")
        form_rating.removeAttribute("style")
        e.target.setAttribute("style","display:none;")
    });