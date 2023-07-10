// FUNÇÃO DE VER E ESCONDER SENHA
const togglePassword = document.querySelector(".toggle-password");
const passwordField = document.querySelector(togglePassword.getAttribute("toggle"));

togglePassword.addEventListener("click", function () {
  const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
  passwordField.setAttribute("type", type);
  togglePassword.classList.toggle("fa-eye-slash");
});

// FUNÇÃO DE CARREGAMENTO DA PAGINA
document.getElementById("loginButton").addEventListener("click", function (event) {
  event.preventDefault();
  var usernameInput = document.getElementById("username-field");
  var passwordInput = document.getElementById("password-field");

  if (usernameInput.value && passwordInput.value) {
    var loadingOverlay = document.getElementById("loadingOverlay");
    loadingOverlay.style.display = "block";

    setTimeout(function () {
      document.getElementById("loginForm").submit();
    }, 3500);
  }
});

