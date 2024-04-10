# Usar la imagen de Rust como base
FROM rust:latest

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copiar el archivo de dependencias
COPY Cargo.toml ./

# Descargar las dependencias sin el código fuente
RUN cargo fetch

# Copiar todo el código fuente
COPY . .

# Compilar tu aplicación
RUN cargo build --release

# Comando para ejecutar tu aplicación
CMD ["./target/release/tu_aplicacion"]
