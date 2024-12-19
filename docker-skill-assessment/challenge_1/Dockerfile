# syntax=docker/dockerfile:1
FROM rust:latest AS build
WORKDIR /build
RUN cargo new greetings
RUN rustup target add x86_64-unknown-linux-musl
RUN cd greetings && cargo build --target=x86_64-unknown-linux-musl && strip /build/greetings/target/x86_64-unknown-linux-musl/debug/greetings
RUN cp /build/greetings/target/x86_64-unknown-linux-musl/debug/greetings hello
###########################################
# TODO: Complete this Dockerfile by adding the final stage.
# 
# 
# Requirements
# - Use the latest Alpine Linux image.
# - Add the hello binary from the build stage to a /runtime directory.
# - Add the /runtime directory to the PATH environment variable.
# - Set /runtime/hello as the default command.

###########################################