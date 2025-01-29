### Getting Started: Flask Backend (Development Mode)

#### 1. **Clone the Repository**
```bash
git clone https://github.com/thesisgenius/thesis-genius.git
cd thesis-genius
```

#### 2. **Backend Setup**
- Navigate to the `backend/` directory:
  ```bash
  cd backend
  ```
- Install dependencies
  ```bash
  python -m venv .venv
  source venv/bin/activate    # On Windows, use venv\Scripts\activate
  pip install -r requirements.txt
  ```
- Run the backend server:
  ```bash
  python run.py
  ```
- The backend will be available at `http://127.0.0.1:8557`

#### 3. **Environment Variables**
- Backend:
   - Create a `.env` file in the `backend/` directory:
   ```text
    # Python Flask Environment Variables
    FLASK_APP=run.app
    FLASK_ENV=development
    FLASK_PORT=8557
    LOG_LEVEL=DEBUG
    SECRET_KEY=dev
    
    # Development Environment Variables
    DEV_DATABASE_ENGINE=mysql
    DEV_DATABASE_NAME=thesis_app_dev
    DEV_DATABASE_USER=thesis_dev
    DEV_DATABASE_PASSWORD='dev_password'
    DEV_DATABASE_HOST=localhost
    
    # Testing Environment Variables
    TEST_DATABASE_ENGINE=sqlite
    TEST_DATABASE_NAME=:memory:
    
    # Production Environment Variables
    PROD_DATABASE_ENGINE=mysql
    PROD_DATABASE_NAME=prod_db
    PROD_DATABASE_USER=prod_user
    PROD_DATABASE_PASSWORD=prod_password
    PROD_DATABASE_HOST=cloud-mysql-url
   ``` 

---

# Backend API Overview for ThesisGenius

Based on your list of API endpoints, most CRUD operations are covered for major entities like **thesis**, **references**, **footnotes**, **tables**, **figures**, **appendices**, **forum posts**, and **user profiles**. However, there are some gaps and potential enhancements to make the API more comprehensive and flexible:

---

### **Potential CRUD Gaps**

#### **1. User Management**
- **Create User**: No endpoint is listed for an admin to create new users. Registration exists (`/api/auth/register`), but admin-initiated user creation might be needed for management purposes.
  - Suggested: **POST** `/api/user/new`
- **Delete User**: There's no endpoint for deleting a user.
  - Suggested: **DELETE** `/api/user/<int:user_id>`

#### **2. ForumDashboard Posts**
- **Update Post**: No endpoint for updating forum posts.
  - Suggested: **PUT** `/api/forum/posts/<int:post_id>`

#### **3. Comments**
- **List Comments**: No endpoint for listing comments on a post.
  - Suggested: **GET** `/api/forum/posts/<int:post_id>/comments`

- **Delete Comment**: No endpoint for deleting a comment.
  - Suggested: **DELETE** `/api/forum/posts/<int:post_id>/comments/<int:comment_id>`

#### **4. Thesis Sub-Entities**
CRUD operations for sub-entities like references, footnotes, figures, etc., appear to be covered individually. Ensure the following workflows are supported:
- **Bulk Update**: Ability to update multiple references or footnotes in one request.
  - Suggested: **PUT** `/api/thesis/<int:thesis_id>/bulk-update/references`

#### **5. Global Search/Filter Endpoints**
- **Search Theses**: Provide a search or filter endpoint for theses by title, student, or date.
  - Suggested: **GET** `/api/thesis/search`
  - Query Parameters:
    - `title=`
    - `student=`
    - `date=`

---

### **Enhancements for Flexibility**

#### **Pagination**
- Add pagination support to endpoints that return lists (e.g., `/api/forum/posts`, `/api/thesis/theses`, `/api/thesis/<int:thesis_id>/references`).
  - Suggested Query Parameters:
    - `page=1`, `size=10`

#### **Soft Deletes**
- Add "soft delete" support for entities like theses, users, and posts, where records are marked as inactive rather than permanently deleted.

#### **Audit Logging**
- Include endpoints for viewing audit logs or history of changes for critical entities like theses.
  - Suggested: **GET** `/api/thesis/<int:thesis_id>/history`

---

### **Updated CRUD Checklist**

| Entity        | Create              | Read                             | Update                   | Delete                     |
|---------------|---------------------|----------------------------------|--------------------------|----------------------------|
| User          | ✅ (`auth.register`) | ✅ (`/api/user/profile`)          | ✅ (`/api/user/profile`)  | ❌ Missing                  |
| Thesis        | ✅                   | ✅ (`/api/thesis/:id`)            | ✅ (`/api/thesis/:id`)    | ✅ (`/api/thesis/:id`)      |
| Reference     | ✅                   | ✅ (`/api/thesis/:id/references`) | ✅ (`/api/reference/:id`) | ✅ (`/api/reference/:id`)   |
| Footnote      | ✅                   | ✅ (`/api/thesis/:id/footnotes`)  | ✅ (`/api/footnote/:id`)  | ✅ (`/api/footnote/:id`)    |
| Table         | ✅                   | ✅ (`/api/thesis/:id/tables`)     | ✅ (`/api/table/:id`)     | ✅ (`/api/table/:id`)       |
| Figure        | ✅                   | ✅ (`/api/thesis/:id/figures`)    | ✅ (`/api/figure/:id`)    | ✅ (`/api/figure/:id`)      |
| Appendix      | ✅                   | ✅ (`/api/thesis/:id/appendices`) | ✅ (`/api/appendix/:id`)  | ✅ (`/api/appendix/:id`)    |
| ForumDashboard Post    | ✅                   | ✅ (`/api/forum/posts`)           | ❌ Missing                | ✅ (`/api/forum/posts/:id`) |
| ForumDashboard Comment | ✅                   | ❌ Missing                        | ❌ Missing                | ❌ Missing                  |

---

### **Suggestions to Enhance Functionality**
1. Add missing endpoints (`POST`, `DELETE`, `PUT`, `GET`) for users, forum posts, and comments.
2. Support pagination for list endpoints.
3. Add bulk operations for thesis sub-entities like references and footnotes.
4. Consider implementing search/filter endpoints for theses and other entities.

Would you like help drafting these additional endpoints?

## Key Endpoints
### Thesis Management
- **POST** `/api/thesis` - Create a new thesis.
- **GET** `/api/thesis/:id` - Fetch details of a specific thesis.
- **PUT** `/api/thesis/:id` - Update metadata or content of a specific thesis.
- **DELETE** `/api/thesis/:id` - Delete a specific thesis.

### References
- **POST** `/api/thesis/:id/references` - Add a reference to a thesis.
- **GET** `/api/thesis/:id/references` - Fetch all references for a thesis.
- **PUT** `/api/reference/:id` - Update a specific reference.
- **DELETE** `/api/reference/:id` - Delete a specific reference.

### Footnotes
- **POST** `/api/thesis/:id/footnotes` - Add a footnote.
- **GET** `/api/thesis/:id/footnotes` - Fetch all footnotes for a thesis.
- **PUT** `/api/footnote/:id` - Update a specific footnote.
- **DELETE** `/api/footnote/:id` - Delete a specific footnote.

### Tables
- **POST** `/api/thesis/:id/tables` - Add a table.
- **GET** `/api/thesis/:id/tables` - Fetch all tables for a thesis.
- **PUT** `/api/table/:id` - Update a specific table.
- **DELETE** `/api/table/:id` - Delete a specific table.

### Figures
- **POST** `/api/thesis/:id/figures` - Add a figure.
- **GET** `/api/thesis/:id/figures` - Fetch all figures for a thesis.
- **PUT** `/api/figure/:id` - Update a specific figure.
- **DELETE** `/api/figure/:id` - Delete a specific figure.

### Appendices
- **POST** `/api/thesis/:id/appendices` - Add an appendix.
- **GET** `/api/thesis/:id/appendices` - Fetch all appendices for a thesis.
- **PUT** `/api/appendix/:id` - Update a specific appendix.
- **DELETE** `/api/appendix/:id` - Delete a specific appendix.

## Health and Status Endpoints
- **GET** `/api/status/alive` - Basic liveness check.
- **GET** `/api/status/health` - Health check including:
  - CPU and memory usage.
  - Required environment variables.
- **GET** `/api/status/ready` - Readiness check ensuring:
  - Database connectivity.
  - Redis server availability.

## Implementation Details
### Database Integration
- **ORM**: Peewee.
- **Connection Proxy**: `database_proxy` is utilized for managing connections across threads.
- **Database Tables**:
  - `Thesis`, `References`, `Footnotes`, `Tables`, `Figures`, `Appendices`, etc.

### Redis Integration
- **Purpose**: Session management, token blacklisting, and caching.
- **Helper Functions**:
  - `get_redis_client`: Returns a Redis client.
  - `add_token_to_user`, `revoke_user_tokens`: Manage user session tokens.
  - `is_token_blacklisted`, `is_token_expired`: Token validation utilities.

### Error Handling
- **Redis**:
  - Catch and return Redis-specific errors such as `redis.exceptions.RedisError`.
- **Peewee**:
  - Handle database-related exceptions like `PeeweeException`.
- **General Exceptions**:
  - Return HTTP status codes (`500` or `503`) with detailed error messages for unknown issues.

## Testing Suite
- **Framework**: Pytest.
- **Fixtures**:
  - `app`: Initializes Flask app with a test database.
  - `db_service`: Provides access to `DBService`.
  - `mock_redis`: Mocks Redis functionality with `fakeredis`.
  - `client`: Provides a test client for HTTP requests.
- **Unit Test Coverage**:
  - CRUD operations for thesis, references, footnotes, tables, figures, appendices.
  - Health, readiness, and liveness endpoints.
  - Redis and database connection validation.

## Best Practices and Recommendations
1. **Security**:
  - Ensure all protected endpoints require valid JWT tokens.
  - Store sensitive data (e.g., Redis and DB credentials) in environment variables.
2. **Scalability**:
  - Optimize Redis and database connection pooling.
  - Consider caching frequent reads (e.g., references and appendices).
3. **Testing**:
  - Expand integration tests to simulate real-world scenarios.
  - Mock external services (e.g., Redis) to validate failure scenarios.

---
This document serves as a comprehensive export of the backend API details.

---

## **Testing**

### Backend

```bash
cd backend
pytest app/tests/ --disable-warnings
```

