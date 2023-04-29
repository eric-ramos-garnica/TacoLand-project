// if the user is login the navbar tab <"USER"> will show, if user is not login it will not show
var login = document.getElementById("display-user-nav").innerHTML
//the 'login ' has space after the n, if you do not put a space there it will not work, you can check the web-developer tool and type login then it will show result
if(login == 'login '){
    user_tab_in_navbar=document.getElementById("user-tab")
    user_tab_in_navbar.removeAttribute("style")

    logout_tab_in_navbar =document.getElementById("logout-tab")
    logout_tab_in_navbar.removeAttribute("style")

    login_tab_in_navbar =document.getElementById("login-tab")
    login_tab_in_navbar.setAttribute("style","display:none;")

    signup_tab_in_navbar =document.getElementById("sign-up-tab")
    signup_tab_in_navbar.setAttribute("style","display:none;")
}