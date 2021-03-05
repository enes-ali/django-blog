let form = document.querySelector("#register-form");
let error_container = document.querySelector("#error-container");


form.addEventListener("submit", (event) => {
    let password_1 = event.target.password.value;
    let password_2 = event.target.password_check.value;

    if(password_1 !== password_2){
        let error = document.createElement("div");
        error.className = "error";
        error.innerText = "Passwords are not same";
        error_container.innerHTML = "";
        error_container.appendChild(error);
        event.preventDefault();
    }
});