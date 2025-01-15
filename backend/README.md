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

## **Testing**

### Backend

```bash
cd backend
pytest
```