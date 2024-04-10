# Usamos una imagen base con Rust preinstalado
FROM rust:latest

# Actualiza el repositorio de paquetes e instala curl
RUN apt-get update && \
    apt-get install -y curl

# Instala Rust y Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$PATH:$HOME/.cargo/bin" && \
    export CARGO_HOME="$HOME/.cargo" && \
    rustup default stable

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia tu código fuente al contenedor
COPY . .

# Compila tu aplicación
RUN cargo build

# Ejecuta tu aplicación
CMD ["./target/debug/your_app_name"]