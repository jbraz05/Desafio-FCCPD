# ➊ Primeiro Desafio: Containers em Rede

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

---

## ◈ Rede Docker
Foi criada um rede customizada chamada `minha-rede`. Nela, os containers se comunicam via DNS interno do Docker.

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