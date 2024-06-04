# Discord Meta Bot

Este é um bot de Discord para controle de metas dos funcionários. Ele permite definir metas, atualizar seu status, deletar metas e gerar relatórios semanais.

## Funcionalidades

- Definir metas para funcionários
- Atualizar o status das metas
- Deletar metas
- Listar metas atuais
- Gerar relatório semanal e resetar metas

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/discord-meta-bot.git
    cd discord-meta-bot
    ```

2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o token do seu bot no arquivo `bot.py`:
    ```python
    TOKEN = 'your_token_here'
    ```

## Uso

1. Execute o bot:
    ```bash
    python bot.py
    ```

2. Use os comandos no Discord:
    - `!setmeta <funcionario> <meta>`: Define uma meta para um funcionário (apenas usuários autorizados).
    - `
