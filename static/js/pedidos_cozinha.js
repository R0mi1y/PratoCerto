let interval = setInterval(function () {
    fetch("http://localhost:8000/cozinhas/atualizar_pedido", {
        mode: "no-cors"
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
    });
}, 3000);
