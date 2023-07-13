var butao_notificacao = document.getElementById("notification_icon");
var popUp;
var idPopUp = 0;

butao_notificacao.addEventListener("click", function() {
  fetch("http://localhost:8000/clientes/notificacoes")
    .then(response => response.json())
    .then(data => {
        var msmPopUp = `<div class="popup-overlay" id="popup-overlay${idPopUp}"></div>
        <div class="popup-content"><div class="titulo-popUp"><h4>Notificações<h4></div><div class="inner-popup">`;
        if(data['status_pedido'].length > 0) {
            for (statusPedido in data.status_pedido){
                msmPopUp += `<h2>${data.status_pedido[statusPedido].prato}</h2>`;
                msmPopUp += `<p>${data.status_pedido[statusPedido].status}</p>`;
            }
            msmPopUp += "<hr></div></div>"
        } else {
            msmPopUp += `<h3>Não há notificações</h3></div></div>`;
        }
        document.body.insertAdjacentHTML('beforeend', msmPopUp);
        
        // Adicionar o evento de clique para fechar o pop-up
        var overlay = document.getElementById(`popup-overlay${idPopUp}`);
        overlay.addEventListener('click', closePopup);
        idPopUp = idPopUp + 1;
    })
    .catch(error => {
      // Tratar erros
      console.error(error);
    });
});

function closePopup() {
  var overlay = document.querySelector('.popup-overlay');
  var content = document.querySelector('.popup-content');

  // Remover o pop-up do DOM
  overlay.parentNode.removeChild(overlay);
  content.parentNode.removeChild(content);
}
