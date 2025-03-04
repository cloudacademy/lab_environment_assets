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


# Install the open telemetry modules here to keep all Otel configuration from here down.
RUN python3 -m pip install \
    opentelemetry-distro \
    opentelemetry-exporter-otlp && \
    opentelemetry-bootstrap -a install

############################################ Task #################################################
#######
####### Auto-instrument the Python applications (be-service & db-service) by editing the
####### default command below to execute the `flask` binary from the `opentelemetry-instrument` 
####### binary installed as part of the above pip install command.
####### 
####### This Dockerfile is is used for both services requiring an environment variable (SERVICE_NAME) to 
####### differentiate the service names sent to Signoz.
####### 
####### 
####### REQUIREMENTS 
####### 
####### 1.) The OTel service name must be set to the $SERVICE_NAME environment variable.
#######     The values are already set in the compose.yaml file per service.
####### 
####### 2.) The OTel exporter OTLP/HTTP endpoint must be set to the following URL: http://$SIGNOZ_HOST:4318
#######     The SIGNOZ_HOST env var is configured to use the SIGNOZ_HOST var from the shell that execs compose.
#######     The command provided to run the service sets the SIGNOZ_HOST variable and must be included.
####### 
####### 3.) Enable the auto-logging feature.
#######
####### 4.) Configure the metric, trace, and log exporters using: otlp_proto_http
#######
####### Documentation is available at: 
####### https://opentelemetry.io/docs/languages/python/getting-started/#add-manual-instrumentation-to-automatic-instrumentation
#######
###################################################################################################

CMD flask run

