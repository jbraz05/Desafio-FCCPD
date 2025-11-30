Antes de executar qualquer um dos desafios, certifique-se de que está na pasta correspondente. Caso não esteja, use o comando `cd desafioN` no terminal, sendo N o número do desafio a ser testado.

<details>
<summary><h2>⓵ Primeiro Desafio: Containers em Rede</h2></summary>

## ◈ Objetivo
Criar dois containers Docker que se comunicam através de uma rede customizada.

---

## ◈ Componentes do Projeto

### Webserver (Flask)
- Executa um servidor HTTP na porta **8080**
- Responde com uma string simples para cada requisição

### Client
- Envia requisições HTTP periódicas ao servidor usando `curl`
- Intervalo de 5 segundos entre cada camada

### Rede Docker
- Foi criada um rede customizada chamada `minha-rede`. 
- Nela, os containers se comunicam via DNS interno do Docker.

---

## ◈ Como Executar

### 1. Criar a rede:
```bash
docker network create minha-rede
```

### 2. Buildar e rodar servidor:
```bash
docker build -t meu-webserver ./webserver
docker run -d --name webserver --network minha-rede -p 8080:8080 meu-webserver
```

### 3. Buildar e rodar o cliente:
```bash
docker build -t meu-client ./client
docker run -d --name client --network minha-rede meu-client
```

### 4. Ver o cliente consultando o servidor:
```bash
docker logs client
```

</details>

<details>
<summary><h2>⓶ Segundo Desafio: Volumes e Persistência</h2></summary>

## ◈ Objetivo
Demonstrar persistência de dados utilizando volumes Docker e um pequeno banco SQLite.

---

## ◈ Componentes do Projeto

### Banco de Dados (SQLite)
- Banco armazenado no caminho `/data/banco.db`, dentro de um volume Docker.
- Arquivo criado e populado pelo script `init_db.py`.
- Permite demonstrar persistência real mesmo após remoção do container.

### Script de Inicialização (`init_db.py`)
- Cria o banco e a tabela `usuarios`.
- Insere registros iniciais para demonstrar a persistência:
  - João
  - Maria
- Executado **uma única vez** para popular o volume.

### Aplicação Leitora (`main.py`)
- Abre o banco SQLite já criado no volume.
- Lê os usuários cadastrados.
- Imprime o resultado no terminal do container.
- Serve como prova de que os dados persistiram.

### Volume Docker (`meuvolume`)
- Armazena o arquivo `banco.db` fora do container.
- Permite recriar o container quantas vezes forem necessárias sem perder dados.

---

## ◈ Como Executar

### 1. Criar o volume:
```bash
docker volume create meuvolume
```

### 2. Inicializar o banco de dados:
```bash
docker run --rm \
  -v meuvolume:/data \
  -v ${PWD}\app:/app \
  python:3.10-slim python /app/init_db.py
```
*Observação: Se estiver executando no PowerShell, troque cada \ por um `*

### 3. Construir a imagem do projeto:
```bash
docker build -t desafio2-sqlite .
```

### 4. Executar o container que lê os dados:
```bash
docker run --rm -v meuvolume:/data desafio2-sqlite
```

### 5. Testando a persistência:
```bash
docker rm -f qualquercoisa 2>/dev/null
docker run --rm -v meuvolume:/data desafio2-sqlite
```
*Observação: Se estiver executando no PowerShell, troque pelo comando abaixo:*
```bash
docker rm -f qualquercoisa 2>$null
docker run --rm -v meuvolume:/data desafio2-sqlite
```

</details>

<details>
<summary><h2>⓷ Terceiro Desafio: Docker Compose Orquestrando Serviços</h2></summary>

## ◈ Objetivo
Orquestrar múltiplos serviços Docker usando Docker Compose, demonstrando comunicação interna, variáveis de ambiente e dependências.

---

## ◈ Componentes do Projeto

### Web (Flask)
- Expõe API na porta 8000.
- Conecta ao Redis para contador de visitas.
- Conecta ao PostgreSQL para ler mensagens.

### Banco de Dados (ProstgreSQL)
- Armazena tabela `mensagens`.
- Possui script de inicialização automático em `db-init/init.sql`.

### Cache (Redis)
- Mantém o contador de acessos.
- Comunicação rápida via rede interna.

### Rede e Dependências
- Todos os serviços estão na rede interna `minha-rede.`
- `depends_on` garante que db e cache iniciem antes do web.
- Variáveis de ambiente configuram conexões de forma clara e isolada.

---

## ◈ Como Executar

### 1. Subir tudo:
```bash
docker compose up --build
```

### 2. Ver comunicação funcionando:
*Acesse o link:*
```bash
http://localhost:8000
```
*O retorno inclui:*
- *Mensagem do Postgres*
- *Contador do Redis*
- *Confirmação da comunicação entre os serviços*

</details>

<details>
<summary><h2>⓸ Quarto Desafio: Microsserviços Independentes</h2></summary>

## ◈ Objetivo
Criar dois microsserviços independentes que se comunicam via HTTP, cada um com seu próprio Dockerfile, demonstrando uma arquitetura simples de microsserviços.

---

## ◈ Componentes do Projeto

### Microsserviço A (service_a)
- Exposto na porta interna 5000.
- Endpoint principal: `GET /users`
  - Retorna uma lista de usuários em JSON, com campos `id`, `nome` e `ativo_desde`.
- Endpoint de saúde: `GET /health`
  - Retorna um JSON simples com status do serviço.

### Microsserviço B (service_b)
- Exposto na porta interna 5000 e mapeado para `localhost:5001`.
- Endpoint principal: `GET /relatorio`
  - Consome `GET /users` do microsserviço A.
  - Monta frases no formato: `"Usuário X ativo desde Y."`.
  - Retorna um JSON com:
    - `quantidade_usuarios`
    - `frases` (lista de strings)
    - `origem` (texto explicativo).
- Endpoint de saúde: `GET /health`
  - Mostra status do serviço B e a URL configurada para o serviço A.

### Docker e Comunicação
- Cada microsserviço possui seu próprio `Dockerfile`.
- A comunicação entre eles é feita via HTTP, usando o nome do serviço (`service_a`) como host.
- O arquivo `docker-compose.yml` orquestra a subida dos dois serviços na mesma rede interna `micros_net`.

---

## ◈ Como Executar

### 1. Subir os serviços com Docker Compose:
```bash
docker compose up --build
```
*Isso irá:*
- *Construir as imagens de service_a e service_b.*
- *Criar a rede interna micros_net.*
- *Subir os dois containers já conectados.*

### 2. Testar o Microsserviço A:
```bash
curl http://localhost:5000/users
```

### 3. Testar o Microsserviço B (consumindo A):
```bash
curl http://localhost:5001/relatorio
```
*Isso comprova que:*
- *O microsserviço B está chamando o A via HTTP.*
- *A comunicação entre microsserviços está funcionando na rede interna.*

---

## ◈ Arquitetura e Endpoints

- Rede interna: `micros_net`.
- Serviços:
  - `service_a`: serve JSON com usuários.
  - `service_b`: consome `service_a` e monta um relatório.
- Principais endpoints:
  - `service_a`: `GET /users`, `GET /health`.
  - `service_b`: `GET /relatorio`, `GET /health`.

</details>

<details>
<summary><h2>⓹ Quinto Desafio: Microsserviços com API Gateway</h2></summary>

## ◈ Objetivo
Criar uma arquitetura com três serviços independentes:
- Microsserviço de usuários
- Microsserviço de pedidos
- API Gateway centralizando o acesso

Cada serviço deve rodar em seu próprio container e se comunicar via HTTP.

---

## ◈ Componentes do Projeto

### Microsserviço de Usuários (`users_service`)
- Porta interna 6000.
- Endpoint principal: `GET /users`
  - Retorna uma lista de usuários em JSON.
- Endpoint de saúde: `GET /health`.

### Microsserviço de Pedidos (`orders_service`)
- Porta interna 7000.
- Endpoint principal: `GET /orders`
  - Retorna pedidos vinculados aos usuários.
- Endpoint de saúde: `GET /health`.

### API Gateway (`gateway`)
- Porta exposta: 8000.
- Endpoints:
  - `GET /users` → chama o users_service
  - `GET /orders` → chama o orders_service
- Centraliza o acesso a ambos os serviços.
- Configurado via variáveis de ambiente:
  - `USERS_URL`
  - `ORDERS_URL`

---

## ◈ Como Executar

### 1. Subir tudo:
```bash
docker compose up --build
```

### 2. Testar o microsserviço de usuários:
```bash
curl http://localhost:6000/users
```

### 3. Testar o microsserviço de pedidos:
```bash
curl http://localhost:7000/orders
```

### 4. Testar o Gateway:
```bash
curl http://localhost:8000/users
curl http://localhost:8000/orders
```

</details>