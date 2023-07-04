function atualizar_notificacoes() {
    $.ajax({
        url: "http://localhost:8000/garcons/get_pedidos/Pendente_local",
        type: "GET",
        dataType: "json",
        success: function (response) {
            $('#pedidoPratos').empty();

            $.each(response.pedido_prontos, function (index, pedido_pronto) {
                var pedidoHTML = '<div class="pedido">';
                pedidoHTML += '<a href="/pedidos/ver/' + pedido_pronto.pedido.id + '"><p>ID do Pedido: ' + pedido_pronto.pedido.id + '</p>';
                pedidoHTML += '<p>Valor Total: ' + pedido_pronto.pedido.total + '</p>';
                pedidoHTML += '<p>Status: ' + pedido_pronto.pedido.status + '</p>';
                pedidoHTML += '<p>Método de Pagamento: ' + pedido_pronto.pedido.metodo_pagamento + '</p>';
                pedidoHTML += '<p>Desconto: ' + pedido_pronto.pedido.desconto + '</p>';
                pedidoHTML += '</div>';
                pedidoHTML += '<hr>';

                $('#pedidoPratos').append(pedidoHTML);
            });
        },
        error: function (xhr, status, error) {
            console.log("Erro na requisição AJAX:", error);
        }
    });
}

atualizar_notificacoes()

var interval = setInterval(atualizar_notificacoes, 3000);
