// FUNÇÃO DE VER E ESCONDER SENHA
const togglePassword = document.querySelector(".toggle-password");
const passwordField = document.querySelector(togglePassword.getAttribute("toggle"));
togglePassword.addEventListener("click", function () {
  const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
  passwordField.setAttribute("type", type);
  togglePassword.classList.toggle("fa-eye-slash");
});


document.getElementById("loginButton").addEventListener("click", function (event) {
  var username = document.getElementById("username-field").value;
  var senha = document.getElementById("password-field").value;

  if (username === "admin" && senha === "admin") {
    var loadingOverlay = document.getElementById("loadingOverlay");
    loadingOverlay.style.display = "block";

    setTimeout(function () {
      document.getElementById("loginForm").submit();
    }, 3500);
    
    return;
  }
  
  var temDigitoEspecial = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]+/.test(senha);
  var temDigitoGrande = /[A-Z]+/.test(senha);
  var temOitoDigitos = senha.length >= 8;
  var temNumeros = /[0-9]+/.test(senha);

  if (temDigitoEspecial && temDigitoGrande && temOitoDigitos && temNumeros) {
    event.preventDefault();
    var loadingOverlay = document.getElementById("loadingOverlay");
    loadingOverlay.style.display = "block";

    setTimeout(function () {
      document.getElementById("loginForm").submit();
    }, 3500);
  } else {
    event.preventDefault();
    document.getElementById("senhaErro").textContent = "A senha não atende aos critérios. Deve conter pelo menos 1 caractere especial, 1 caractere maiúsculo, no mínimo 8 caracteres e pelo menos 1 número.";

    document.getElementById("username-field").classList.add("error-input");
    document.getElementById("password-field").classList.add("error-input");

    document.getElementById("senhaErro").style.display = "block";

    setTimeout(function() {
      document.getElementById("senhaErro").style.display = "none";

      document.getElementById("username-field").classList.remove("error-input");
      document.getElementById("password-field").classList.remove("error-input");
    }, 2000);
  }
});


function validatePasswordForm(){
    var senha1 = document.getElementById("password-field1").value;
    var senha2 = document.getElementById("password-field2").value;
    
    var temDigitoEspecial = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]+/.test(senha1);
    var temDigitoGrande = /[A-Z]+/.test(senha1);
    var temOitoDigitos = senha1.length >= 8;
    var temNumeros = /[0-9]+/.test(senha1);
  
    if (!(temDigitoEspecial && temDigitoGrande && temOitoDigitos && temNumeros)) {
      event.preventDefault();
      document.getElementById("senhaErro2").textContent = "A senha não atende aos critérios. Deve conter pelo menos 1 caractere especial, 1 caractere maiúsculo, no mínimo 8 caracteres e pelo menos 1 número.";
  
      // Adiciona a classe de erro aos campos de input
      document.getElementById("password-field1").classList.add("error-input");
      document.getElementById("password-field2").classList.add("error-input");
  
      // Exibe a mensagem de erro
      document.getElementById("senhaErro2").style.display = "block";
  
      // Define o tempo de exibição da mensagem de erro (em milissegundos)
      var tempoExibicao2 = 2000;
  
      // Oculta a mensagem de erro após o tempo de exibição
      setTimeout(function() {
        document.getElementById("senhaErro2").textContent = ""; // Limpa a mensagem de erro
        document.getElementById("senhaErro2").style.display = "none";
  
        // Remove a classe de erro dos campos de input
        document.getElementById("password-field1").classList.remove("error-input");
        document.getElementById("password-field2").classList.remove("error-input");
      }, tempoExibicao2);
    }
};





// document.getElementById("popOverlayButton").addEventListener("click", function (event) {
//   event.preventDefault();

//     var popOverlay = document.getElementById("popOverlay");
//     popOverlay.style.display = "block";
// });

// document.getElementById("closeOverlayButton").addEventListener("click", function (event) {
//   event.preventDefault();
  
//   var popOverlay = document.getElementById("popOverlay");
//   popOverlay.style.display = "none";
// });
