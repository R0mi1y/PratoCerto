atualizar_notificacoes();
var interval = setInterval(atualizar_notificacoes, 3000);

function atualizar_notificacoes(){
        $.ajax({
            url: "http://localhost:8000/garcons/get_pedidosPrato/pronto_para_entrega",
            type: "GET",
            dataType: "json", // Altere o tipo de dados para JSON
            success: function(response) {
                // Limpar a seção de pedidos pendentes
                $('#pedidoPratos').empty();
        
                // Iterar sobre cada pedido pronto no array
                $.each(response.pedidoPrato_prontos, function(index, pedidoPratoPronto) {
                    // Criar um elemento HTML para exibir as informações do pedido
                    var pedidoHTML = '<div class="pedido">';
                    pedidoHTML += '<p>ID do Pedido: ' + pedidoPratoPronto.pedidoPrato.id + '</p>';
                    pedidoHTML += '<p>Cliente: ' + pedidoPratoPronto.pedidoPrato.nome_cliente + '</p>';
                    pedidoHTML += '<p>Status: ' + pedidoPratoPronto.pedidoPrato.status + '</p>';
                    pedidoHTML += '<p>Prato: ' + pedidoPratoPronto.prato.nome + '</p>';
                    pedidoHTML += '<a href="/garcons/servir_pedido/' + pedidoPratoPronto.pedidoPrato.id + '">Servir</a>';
                    pedidoHTML += '</div>';
                    pedidoHTML += '<hr>';
        
                    // Adicionar o elemento HTML do pedido à seção de pedidos pendentes
                    $('#pedidoPratos').append(pedidoHTML);
                });
            },
            error: function(xhr, status, error) {
                console.log("Erro na requisição AJAX:", error);
            }
        });
}