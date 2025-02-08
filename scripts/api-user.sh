#!/bin/bash

# Register a user
curl -X POST http://127.0.0.1:8557/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"first_name": "John", "last_name": "Doe", "email": "test@example.com", "username": "testuser", "password": "password123", "institution": "NU","role": "Student"}'

# Log in the user and get the token
TOKEN=$(curl -s -X POST http://127.0.0.1:8557/api/auth/signin \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}' | jq -r .token)

# Sign out the user (blacklist the token)
curl -X POST http://127.0.0.1:8557/api/auth/signout \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}"

# Log in again to get a new token
TOKEN=$(curl -s -X POST http://127.0.0.1:8557/api/auth/signin \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}' | jq -r .token)

# Deactivate the user
curl -X PUT http://127.0.0.1:8557/api/user/deactivate \
    -H "Authorization: Bearer ${TOKEN}"

# Register an admin user
curl -X POST http://127.0.0.1:8557/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Admin", "last_name": "User", "email": "admin@example.com", "username": "adminuser", "password": "adminpassword123", "role": "Admin"}'

# Log in the admin user and get the token
ADMIN_TOKEN=$(curl -s -X POST http://127.0.0.1:8557/api/auth/signin \
    -H "Content-Type: application/json" \
    -d '{"email": "admin@example.com", "password": "adminpassword123"}' | jq -r .token)

# Reactivate the deactivated user using the admin token
curl -X PUT http://127.0.0.1:8557/api/user/activate/4 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}"

# Log in the reactivated user
TOKEN=$(curl -s -X POST http://127.0.0.1:8557/api/auth/signin \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}' | jq -r .token)

# Get user profile
curl -X GET http://127.0.0.1:8557/api/user/profile \
    -H "Authorization: Bearer ${TOKEN}"

# Update user profile
curl -X PUT http://127.0.0.1:8557/api/user/profile \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"first_name": "Jane", "last_name": "Doe", "email": "test@example.com", "username": "janedoe"}'

# Fetch all forum posts
curl -X GET http://127.0.0.1:8557/api/forum/posts

# Create a new forum post
curl -X POST http://127.0.0.1:8557/api/forum/posts \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"title": "New Post", "content": "Post content here"}'

# Fetch a specific forum post by ID
curl -X GET http://127.0.0.1:8557/api/forum/posts/3

# Add a comment to a forum post
curl -X POST http://127.0.0.1:8557/api/forum/posts/3/comments \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"content": "This is a comment"}'

# Fetch all theses for the user
curl -X GET http://127.0.0.1:8557/api/thesis/theses \
    -H "Authorization: Bearer ${TOKEN}"

# Create a new thesis
THESIS_ID=$(curl -X POST http://127.0.0.1:8557/api/thesis/new \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"title": "New Thesis", "status": "Pending"}' | jq -r '.id')

# Update an existing thesis
curl -X PUT http://127.0.0.1:8557/api/thesis/"$THESIS_ID" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"title": "Updated Thesis Title", "status": "Approved"}'

curl -X GET http://127.0.0.1:8557/api/thesis/4 \
    -H "Authorization: Bearer ${TOKEN}"


curl -X POST http://127.0.0.1:8557/api/thesis/new \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{
          "title": "New Thesis",
          "status": "Pending",
          "abstract": "This is a test abstract.",
          "body_pages": [
              {"page_number": 1, "body": "This is the first page."},
              {"page_number": 2, "body": "This is the second page."}
          ]
        }'