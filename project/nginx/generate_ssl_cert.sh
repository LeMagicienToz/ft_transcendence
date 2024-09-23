#!/bin/sh

SSL_DIR="/etc/nginx/ssl"
CERT_FILE="$SSL_DIR/server.crt" # les noms de fichiers doivent etre identiques a ceux de la condtion dans le makefile
KEY_FILE="$SSL_DIR/server.key"

# Vérifie si les fichiers de certificats existent
if [[ -f "$CERT_FILE" && -f "$KEY_FILE" ]]; then
    echo "Certificat et clé déjà présents, pas besoin de générer."
else
    echo "Certificats non trouvés, génération de nouveaux certificats..."
    mkdir -p $SSL_DIR
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$KEY_FILE" \
        -out "$CERT_FILE" \
        -subj "/C=FR/ST=PACA/L=NICE/O=42/OU=Unit/CN=transcendence.fr"

    echo "Certificats générés avec succès."
fi
