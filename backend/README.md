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
    python -m venv venv
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
   FLASK_ENV=development
   FLASK_APP_PORT=8557
   DATABASE_URL=mysql://username:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ``` 

## **Testing**

### Backend

```bash
cd backend
pytest
```