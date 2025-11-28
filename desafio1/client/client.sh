#!/bin/bash
while true; do
    echo "➡ Enviando requisição..."
    curl -s http://webserver:8080
    echo ""
    sleep 5
done