### Getting Started: Flask Backend (Development Mode)

### Python Setup

Install all required Python, Flask, and React:

1. Install Python: [Downloading Python](https://wiki.python.org/moin/BeginnersGuide/Download)
2. Install Pip: [Installing Pip](https://pip.pypa.io/en/stable/installation/#installation)
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