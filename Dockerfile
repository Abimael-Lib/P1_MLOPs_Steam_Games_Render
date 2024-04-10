# Usar la imagen de Rust como base
FROM rust:latest

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copiar los archivos de dependencias
COPY Cargo.toml Cargo.lock ./

# Build de las dependencias sin el código fuente
RUN cargo build --release

# Copiar todo el código fuente
COPY . .

# Compilar tu aplicación
RUN cargo build --release

# Comando para ejecutar tu aplicación
CMD ["./target/release/tu_aplicacion"]