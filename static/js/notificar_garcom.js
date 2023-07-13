atualizar_notificacoes();
var interval = setInterval(atualizar_notificacoes, 3000);

function atualizar_notificacoes() {
    fetch('http://localhost:8000/garcons/get_pedidosPrato/pronto_para_entrega')
      .then(response => response.json())
      .then(response => {
        // Limpar a seção de pedidos pendentes
        $('#pedidoPratos').empty();
  
        // Iterar sobre cada pedido pronto no array
        response.pedidoPrato_prontos.forEach(pedidoPratoPronto => {
          // Criar um elemento HTML para exibir as informações do pedido
          var pedidoHTML = '<div class="pedido">';
          pedidoHTML += '<p>ID do Pedido: ' + pedidoPratoPronto.pedidoPrato.id + '</p>';
          pedidoHTML += '<p>Cliente: ' + pedidoPratoPronto.pedidoPrato.nome_cliente + '</p>';
          pedidoHTML += '<p>Status: ' + pedidoPratoPronto.pedidoPrato.status + '</p>';
          pedidoHTML += '<p>Prato: ' + pedidoPratoPronto.prato.nome + '</p>';
  
          if (pedidoPratoPronto.pedido.mesa && pedidoPratoPronto.pedido.mesa.numero) {
            pedidoHTML += '<p>Mesa: ' + pedidoPratoPronto.pedido.mesa.numero + '</p>';
          } else if (pedidoPratoPronto.pedido.endereco) {
            var endereco = pedidoPratoPronto.pedido.endereco[0];
            pedidoHTML += '<p>Endereço: ' + 'Nome: ' + endereco.nome + ', Rua: ' + endereco.rua + ', Bairro: ' + endereco.bairro + ', Complemento: ' + (endereco.complemento || "Não há complemento") + ', Número: ' + endereco.numero + '</p>';
          }
  
          pedidoHTML += '<a href="/garcons/servir_pedido/' + pedidoPratoPronto.pedidoPrato.id + '">Servir</a>';
          pedidoHTML += '</div>';
          pedidoHTML += '<hr>';
  
          // Adicionar o elemento HTML do pedido à seção de pedidos pendentes
          $('#pedidoPratos').append(pedidoHTML);
        });
      })
      .catch(error => {
        console.log('Erro na requisição fetch:', error);
      });
  }
  