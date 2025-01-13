
curl -X POST http://127.0.0.1:8557/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"name": "John Doe", "email": "test@example.com", "password": "password123"}'


TOKEN=$(curl -s -X POST http://127.0.0.1:8557/api/auth/signin \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}' | jq -r .token)

curl -X POST http://127.0.0.1:8557/api/auth/signout \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"email": "test@example.com", "password": "password123"}'

TOKEN=$(curl -s -X POST http://127.0.0.1:8557/api/auth/signin \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}' | jq -r .token)

curl -X PUT http://127.0.0.1:8557/api/user/deactivate \
    -H "Authorization: Bearer ${TOKEN}"

TOKEN=$(curl -s -X POST http://127.0.0.1:8557/api/auth/signin \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}' | jq -r .token)

curl -X GET http://127.0.0.1:8557/api/user/profile \
    -H "Authorization: Bearer ${TOKEN}"


curl -X PUT http://127.0.0.1:8557/api/user/profile \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"name": "Jane Doe", "email": "jane@example.com"}'




curl -X GET http://127.0.0.1:8557/api/forum/posts

curl -X POST http://127.0.0.1:8557/api/forum/posts \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"title": "New Post", "content": "Post content here"}'

curl -X GET http://127.0.0.1:8557/api/forum/posts/1


curl -X POST http://127.0.0.1:8557/api/forum/posts/1/comments \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"content": "This is a comment"}'


curl -X GET http://127.0.0.1:8557/api/thesis/theses \
    -H "Authorization: Bearer ${TOKEN}"

curl -X POST http://127.0.0.1:8557/api/thesis/thesis \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"title": "New Thesis", "abstract": "This is the abstract", "status": "Pending"}'


curl -X PUT http://127.0.0.1:8557/api/thesis/thesis/1 \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d '{"title": "Updated Thesis Title", "abstract": "Updated Abstract", "status": "Approved"}'
