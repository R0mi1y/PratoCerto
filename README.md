---

# Prato Certo

Prato Certo é uma aplicação web desenvolvida em Django, destinada a auxiliar restaurantes no gerenciamento de suas operações. A aplicação oferece funcionalidades abrangentes, incluindo gerenciamento de garçons, eventos, reservas, pratos, pedidos, pagamentos, caixas, clientes e cozinhas.

## Funcionalidades

- **Gerenciamento de Garçons:** Controle e supervisão dos garçons.
- **Eventos e Reservas:** Criação e gerenciamento de eventos e reservas.
- **Pratos e Pedidos:** Cadastro e gerenciamento de pratos e pedidos.
- **Pagamentos:** Processamento e registro de pagamentos.
- **Gerenciamento de Caixa:** Controle das operações de caixa.
- **Gerenciamento de Clientes:** Cadastro e gerenciamento de clientes.
- **Cozinha:** Coordenação das atividades da cozinha.

## Tecnologias Usadas

- **Django:** Framework web utilizado para o desenvolvimento da aplicação.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/R0mi1y/PratoCerto.git
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd PratoCerto
    ```
3. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    ```
4. Ative o ambiente virtual:
    - No Windows:
        ```bash
        venv\Scripts\activate
        ```
    - No macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
6. Realize as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```
7. Inicie o servidor:
    ```bash
    python manage.py runserver
    ```

## Uso

1. Acesse o site através do navegador:
    ```
    http://127.0.0.1:8000/
    ```
2. Cadastre e gerencie garçons, eventos, reservas, pratos, pedidos, pagamentos, caixas, clientes e cozinhas conforme necessário.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch:
    ```bash
    git checkout -b feature/nome-da-feature
    ```
3. Faça as alterações necessárias.
4. Commit suas mudanças:
    ```bash
    git commit -m 'Adicionei uma nova feature'
    ```
5. Faça o push para a branch:
    ```bash
    git push origin feature/nome-da-feature
    ```
6. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Ediel Romily Silva Caetano - [edielromily7@gmail.com](mailto:edielromily7@gmail.com)

---

Sinta-se à vontade para ajustar qualquer parte conforme necessário!
