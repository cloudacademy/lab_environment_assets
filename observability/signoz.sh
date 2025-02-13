#!/bin/bash

# Function to start the services
start_services() {
    echo "Signoz (starting)"
    docker-compose -f ~/.app/signoz/deploy/docker/docker-compose.yaml up --detach --remove-orphans
    echo "Signoz (running)"

    until curl -L -s -o /dev/null -w "%{http_code}" http://localhost:3301/api/v1/register | grep 200; do
        sleep 1
    done

    curl -Ls -X POST -o /dev/null -H "Content-Type: application/json" -d '{"email":"student@qa.com","name":"Student","orgName":"QA","password":"blueberry-3.14"}' http://localhost:3301/api/v1/register
    echo "Signoz (admin registered)"
}

# Function to stop the services
stop_services() {
    echo "Signoz (stopping)"
    docker-compose -f ~/.app/signoz/deploy/docker/docker-compose.yaml down
    echo "Signoz (stopped)"
}

# Function to download signoz
download_signoz() {
    echo "Signoz (downloading)"
    
    mkdir -p ~/.app 
    pushd ~/.app
    
    # Remove the dir if it's already downloaded.
    rm -rf signoz
    # Clone the repo
    git clone -b main https://github.com/SigNoz/signoz.git 
    
    # Currently a bug in the current version, the otel collector doesn't start.
    # Using the previous version until its fixed.
    pushd signoz
    git checkout v0.72.0 
    
    # Back to the original dir.
    popd
    popd
    echo "Signoz (downloaded)"
}

# Check for command-line arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {start|stop|download}"
    exit 1
fi

case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    download)
        download_signoz
        ;;
    *)
        echo "Invalid option: $1"
        echo "Usage: $0 {start|stop|download}"
        exit 1
        ;;
esac
