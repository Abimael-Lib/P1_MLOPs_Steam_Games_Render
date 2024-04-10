# Usa una imagen base con Python
FROM python:3.9-slim

# Instala Rust y Cargo
RUN apt-get update && \
    apt-get install -y curl && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    source $HOME/.cargo/env && \
    rustup default stable

# Configura el directorio de trabajo
WORKDIR /app

# Copia el código al contenedor
COPY . .

# Instala los requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta la aplicación
CMD ["python", "app.py"]
