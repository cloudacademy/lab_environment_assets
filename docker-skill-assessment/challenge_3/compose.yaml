# syntax=docker/dockerfile:1
FROM rust:latest AS build
WORKDIR /build
RUN cargo new greetings
RUN rustup target add x86_64-unknown-linux-musl
RUN cd greetings && cargo build --target=x86_64-unknown-linux-musl && strip /build/greetings/target/x86_64-unknown-linux-musl/debug/greetings
RUN cp /build/greetings/target/x86_64-unknown-linux-musl/debug/greetings hello
###########################################
# Complete this Dockerfile by adding the final stage.
# 
# 
# Requirements
# - Ensure the latest Alpine Linux image is used as the base image.
# - Ensure the /build/hello binary from the build stage resides at /runtime/hello in the final stage.
# - Ensure the /runtime directory is added to the PATH environment variable. 
# - Ensure the /runtime/hello binary runs when the container starts.
#
#
