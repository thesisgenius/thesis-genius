# thesis-genius web-site (thesis-genius.com) repository

Codebase repository hosting ThesisGenius.com

```text
thesis-genius/
├── backend/                # Backend Flask application
│   ├── app/                # Core Flask app
│   │   ├── __init__.py     # Flask app factory
│   │   ├── routes.py       # API routes
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Helper utilities
│   │   └── tests/          # Backend tests
│   ├── instance/           # Config files (optional)
│   ├── requirements.txt    # Python dependencies
│   └── run.py              # Run the Flask application
│
├── frontend/               # Frontend React application
│   ├── public/             # Static files (e.g., index.html, favicon.ico)
│   ├── src/                # React source code
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Route-specific pages (SignIn, Dashboard, etc.)
│   │   ├── services/       # API service layer for interacting with Flask
│   │   ├── App.jsx         # Main React component
│   │   ├── index.jsx       # Entry point for React app
│   │   └── styles/         # Global and component-specific styles
│   ├── package.json        # Frontend dependencies
│   ├── vite.config.js      # Configuration (if using Vite)
│   └── .env                # Environment variables for React
│
├── .gitignore              # Ignored files for Git
├── README.md               # Project overview and setup instructions
└── docker-compose.yml      # Optional: Docker configuration

```

* Front-End: React (JavaScript)
* Back-End: Python Flask
* Database: MySQL or MongoDB
* Design: Figma (for wireframes)
* Version Control: GitHub
* Testing Frameworks: Jest (Front-End), Pytest (Back-End)
* Deployment: Cloud-based hosting (e.g., AWS, Heroku)