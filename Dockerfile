# Use the official Rust image from Docker Hub
FROM rust:latest

# Create a new directory to work in
WORKDIR /usr/src/app

# Copy the local Cargo.toml and Cargo.lock into the container
COPY Cargo.toml .
COPY Cargo.lock .

# Copy the entire local code into the container
COPY . .

# Build the application
RUN cargo build

# Set the startup command to run your binary
CMD ["./target/debug/my_app"]