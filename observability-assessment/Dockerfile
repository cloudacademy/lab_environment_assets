FROM python:3.10-alpine


# Build arguments 
ARG application_dir undefined 
ARG use_flask_debug false

# Set the environment variables
ENV FLASK_APP ${application_dir}.app
ENV FLASK_DEBUG ${use_flask_debug}
ENV FLASK_RUN_PORT 9000
ENV FLASK_RUN_HOST 0.0.0.0
ENV SIGNOZ_HOST undefined

# All application code resides inside subdirectories of the /code directory.
WORKDIR /code

# Copy the wheel file from the dist folder and install it using pip.
COPY . ./${application_dir}

# Install and cache the dependencies.
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --no-cache-dir -r ${application_dir}/requirements.txt

# Run the application using the development server.
CMD flask run

