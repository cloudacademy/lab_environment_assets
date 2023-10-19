#!/bin/bash

apk update
apk add python3
# Check if all required arguments are provided
if [ $# -lt 4 ]; then
    echo "Usage: $0 <name> <password> <git_tea_url> <repo1> [<repo2> ...]"
    exit 1
fi

# Extract arguments
name="$1"
password="$2"
host="$3"
shift 3
repos=("$@")

# Function to create a student
create_student() {
    su git -c "gitea admin user create --username \"$name\" --password \"$password\" --email \"$name@cloudacademy.com\" --admin=true --must-change-password=false"

}

# Function to auth token.
auth_token() {
    response=$(curl -s -H "Content-Type: application/json" -d '{"name":"student_key", "scopes": ["repo", "admin:repo_hook", "admin:org", "admin:public_key", "admin:org_hook", "notification", "user", "delete_repo", "package", "admin:gpg_key", "admin:application", "sudo"]}' -u "$name:$password" "$host/api/v1/users/$name/tokens")
    # extract token
    echo "$response" | python3 -c "import json, sys; data = json.load(sys.stdin); print(data['sha1'])"
}

# Function to create a repository
create_repo() {
    local token="$1"
    local repo_name="$2"

    # Replace spaces in repo_name with underscores
    repo_name="${repo_name// /_}"

    curl "$host/api/v1/user/repos" \
        -H "accept: application/json" \
        -H "Authorization: token $token" \
        -H "Content-Type: application/json" \
        -d '{ "auto_init": false, "default_branch": "main", "description": "project repo", "name": "'"$repo_name"'", "private": true, "template": false, "trust_model": "default"}' -i
}

# Create the student
create_student

# Get the auth token
token=$(auth_token)

# Loop through the list of repositories and create them
for repo in "${repos[@]}"; do
    create_repo "$token" "$repo"
done

echo "All repositories created successfully."