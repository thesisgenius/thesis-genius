# thesis-genius web-site (thesis-genius.com) repository

* Front-End: React (JavaScript)
* Back-End: Python Flask
* Database: MySQL or MongoDB
* Design: Figma (for wireframes)
* Version Control: GitHub
* Testing Frameworks: Jest (Front-End), Pytest (Back-End)
* Deployment: Cloud-based hosting (e.g., AWS, Heroku)

```text
thesis-genius
├── LICENSE
├── README.md
├── client
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   └── index.html
│   └── src
│       ├── App.js
│       └── index.js
├── docs
│   └── wireframes
├── instance
├── server
│   ├── app.py
│   ├── config.py
│   ├── instance
│   ├── models
│   │   └── thesis.py
│   ├── routes
│   │   └── api.py
│   ├── static
│   ├── storage
│   └── templates
└── tests
    ├── backend
    └── frontend
```

### Prerequisites

* Software
  * python: ≥ v3.12
  * pip: ≥ 24.0
  * NodeJS.js: ≥ v18


### Getting Started

Install all required Python, Flask, and React:

1. Install Python: [Downloading Python](https://wiki.python.org/moin/BeginnersGuide/Download)
2. Install Pip: [Installing Pip](https://pip.pypa.io/en/stable/installation/#installation)
3. Install Node.js: [Installing Node.js](https://nodejs.org/)
4. Create Python Virtual Environment `venv`:
    ```shell
    python3 -m venv venv # Creates virtual environment
    ```
5. Activate or use Python virtual environment `venv`:
    ```shell
    source venv/bin/activate
    ```
6. Install Python dependent modules:
    ```shell
    pip install -r requirements.txt
    ```

---

### Getting Started: Frontend Server

The frontend server runs the build process for your React application and serves 
the static files in production mode.

Follow these steps to set it up:

1. **Install Node.js**:
    * Ensure you have Node.js installed on your system (v18 or later is recommended). Check the version with:
   ```shell
   node -v
   ```
    * If not installed, download it from [Node.js Official Website](https://nodejs.org/).
2. **Navigate to the Frontend Directory**:
    * From the project root, navigate to the frontend directory:
   ```shell
   cd frontend
   ```
3. **Install Dependencies**:
    * Run the following command to install all required dependencies:
   ```shell
   npm install
   ```
4. **Start the Development Server**:
    * Start the React development server:
   ```shell
   npm start
   ```
5. **Access the Application**:
    * The application should now be running. Access it in your browser at: `http://localhost:3000`

6. **Edit and Save Code**:
    * Any changes you make to the React codebase will automatically reload in the browser.

7. **Stop the Server**:
    * Press `Ctrl + C` in the terminal to stop the server.

---

### Getting Started: Flask Backend (Development Mode)

The development server allows for testing and debugging the Flask backend.

1. **Install Python**:
   * Ensure Python 3.9 or later is installed. Check the version with:
   ```shell
   python3 --version
   ```
2. **Set Up the Virtual Environment**:
    * Navigate to the repository root and create a virtual environment:
   ```shell
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. **Install Dependencies**:
    * Install the required Python packages:
   ```shell
   pip install -r requirements.txt
   ```
4. **Set Environment Variables**:
    * Create a .env file in the backend/ directory and configure it:
   ```shell
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///app.db
   FLASK_APP=app
   FLASK_ENV=development
   ```
5. **Initialize the Database**:
    * Run database migrations to set up the schema:
   ```shell
   flask db upgrade
   ```
6. **Run the Flask Development Server**:
    * Start the development server:
   ```shell
   flask run
   ```

7. **Access the Application**:
    * Access the Flask API at: `http://127.0.0.1:5000`

8. **Stop the Server**:
    * Press Ctrl + C in the terminal to stop the server.


---

### MySQL (Unfinished)

TODO

* `schema.sql` for table definitions.
* Uses `SQLAlchemy` for ORM integration.


---

## Helpful Troubleshooting Notes

#### Clearing Python cache

```shell
find . -name "__pycache__" -type d -exec rm -r {} +
```