# **Thesis Genius Web Application**

Welcome to the repository for Thesis Genius, a web-based platform designed for 
managing theses and academic discussions. This project includes a Flask backend API 
and a React frontend, built for scalability, ease of use, and developer efficiency.

---

## Table of Contents

1. [Thesis Genius Web Application](#thesis-genius-web-application)
2. [Repository Structure](#repository-structure)
3. [Technologies](#technologies)
   - [Frontend](#frontend)
   - [Backend](#backend)
   - [Testing](#testing)
   - [Deployment](#deployment)
4. [Setup Instructions](#setup-instructions)
   - [Prerequisites](#prerequisites)
   - [Development Environment](#development-environment)
     1. [Clone the Repository](#1-clone-the-repository)
     2. [Backend Setup](#2-backend-setup)
     3. [Frontend Setup](#3-frontend-setup)
     4. [Environment Variables](#4-environment-variables)
5. [Using the Makefile](#using-the-makefile)
   - [Key Commands](#key-commands)
6. [Testing](#testing)
   - [Backend](#backend)
   - [Frontend](#frontend)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)


---

## **Repository Structure**

```text
thesis-genius/
├── backend/               # Backend Flask application
│   ├── app/               # Core Flask app
│   │   ├── __init__.py    # Flask app factory
│   │   ├── routes/        # API route handlers
│   │   ├── models/        # Database models
│   │   ├── services/      # Business logic services
│   │   ├── utils/         # Utility functions (e.g., JWT, auth)
│   │   ├── tests/         # Backend unit tests
│   └── requirements.txt   # Backend dependencies
│
├── frontend/              # Frontend React application
│   ├── public/            # Static files (e.g., index.html, favicon.ico)
│   ├── src/               # React source code
│   │   ├── components/    # Reusable React components (Header, Footer, etc.)
│   │   ├── pages/         # Pages (SignIn, SignUp, ManageThesis, ForumDashboard, etc.)
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API service integration
│   │   └── styles/        # Component-specific stylesheets
│   ├── package.json       # Frontend dependencies
│   ├── vite.config.js     # Vite configuration
│   └── .env               # Environment variables for React app
│
├── Makefile               # Build and management commands
├── docker-compose.yml     # Docker configuration for local development
├── .gitignore             # Ignored files for Git
└── README.md              # Documentation and instructions
```

---

## **Technologies**

### **Frontend**
- **Framework**: React (JavaScript)
- **Styling**: CSS (Component-specific and global)
- **Build Tool**: Vite (for fast development)

### **Backend**
- **Framework**: Python Flask
- **Database**: MySQL (primary) or MongoDB (optional)

### **Testing**
- **Frontend**: Jest
- **Backend**: Pytest

### **Deployment**
- **Hosting**: AWS, Heroku, or other cloud platforms
- **Containerization**: Docker

---

## **Setup Instructions**

### **Prerequisites**
1. [Docker](https://www.docker.com/) installed.
2. Python 3.8+ and Node.js 16+ installed.
3. Access to MySQL or MongoDB for database functionality.

### **Development Environment**

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
  python -m cli.main run
  ```
- The backend will be available at `http://127.0.0.1:8557`

#### 3. **Frontend Setup**
- Navigate to the frontend/ directory:
    ```bash
    cd ../frontend
    ```
- Install dependencies:
    ```bash
    npm install
    ```
- Start the development server:
    ```bash
    npm run dev --host
    ```
- The frontend will be available at `http://localhost:5173`.

#### 4. **Environment Variables**
  - Backend:
    - Create a `.env` file in the `backend/` directory:
   ```text
   FLASK_ENV=development
   FLASK_APP_PORT=8557
   DATABASE_URL=mysql://username:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ``` 

  - Frontend:
     - Create a `.env` file in the frontend/ directory:
   ```text
   VITE_API_BASE_URL=http://127.0.0.1:8557/api
   ```
---

## **Using the Makefile**

The `Makefile` provides convenient commands for building and managing the application.

Key Commands
- Build Backend Docker Image:
    ```bash
    make docker-dev-backend
    ```

- Run Backend Container:
    ```bash
    make docker-dev-backend-run
    ```

- Build Frontend Docker Image:
    ```bash
    make docker-dev-frontend
    ```

- Run Frontend Container:
    ```bash
    make docker-dev-frontend-run
    ```

- Stop All Containers:
    ```bash
    make docker-stop
    ```

- Clean Up Docker Images and Containers:
    ```bash
    make docker-clean
    ```

- Lint Code:
    ```bash
    make lint
    ```
---

## **Testing**

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

---

### **Contributing**

1. Clone the repository.
2. Create a feature branch:
3. git checkout -b feature/your-feature-name
4. Commit your changes:
    ```bash
    git commit -m "Add your feature description"
    ```
5. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
6. Submit a pull request.

---

## **License**

This project is licensed under the MIT License. See `LICENSE` for details.

---

## **Contact**
- **Author**: ThesisGenius
- **Email**: support@thesis-genius.com
- **GitHub**: https://github.com/thesisgenius/thesis-genius.git