<details>
<summary><h2>➊ Primeiro Desafio: Containers em Rede</h2></summary>

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

---

## ◈ Critérios atendidos

| **Critério**                        | **Como foi atendido**                    |
| ----------------------------------- | ---------------------------------------- |
| Configuração correta da rede docker | Criada rede `minha-rede` ✔               |
| Comunicação funcional               | Client envia curl → webserver responde ✔ |
| README claro                        | Passo a passo completo incluído ✔        |
| Organização do projeto              | Pastas separadas + Scripts executáveis ✔ |
</details>

<details>
<summary><h2>➋ Segundo Desafio: Volumes e Persistência</h2></summary>

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

---

## ◈ Critérios atendidos

| **Critério**                        | **Como foi atendido**                                                         |
| ----------------------------------- | ----------------------------------------------------------------------------- |
| Uso correto de volumes              | Banco SQLite armazenado em volume Docker (`meuvolume`) ✔                      |
| Comunicação funcional               | Dados permaneceram após remover e recriar containers ✔                        |
| README claro                        | Passo a passo completo de criação, preenchimento e leitura do volume ✔        |
| Organização do projeto              | Scripts separados em `/app`, Dockerfile simples e bem organizado ✔            |
</details>

<details>
<summary><h2>➌ Terceiro Desafio: Docker Compose Orquestrando Serviços</h2></summary>

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

---

## ◈ Critérios atendidos

| **Critério**                           | **Como foi atendido**                                         |
| -------------------------------------- | ------------------------------------------------------------- |
| Compose funcional e bem estruturado    | docker-compose.yml com 3 serviços, volumes, rede e configs ✔  |
| Comunicação entre serviços funcionando | Web acessa Redis e PostgreSQL via DNS interno ✔               |
| README com explicação da arquitetura   | Documentação completa e organizada no estilo dos desafios ✔   |
| Clareza e boas práticas                | Códigos separados, init SQL, rede interna e env vars limpas ✔ |
</details>