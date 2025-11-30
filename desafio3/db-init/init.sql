CREATE TABLE IF NOT EXISTS mensagens (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL
);

INSERT INTO mensagens (texto)
VALUES ('Mensagem vinda do banco Postgres via Docker Compose!');