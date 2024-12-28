# thesis-genius web-site (thesis-genius.com) repository

Codebase repository hosting ThesisGenius.com

```text
thesis-genius
├── LICENSE
├── Makefile
├── README.md
├── client
│   └── placeholder
├── docs
│   ├── backend
│   │   └── environment.md
│   ├── ci
│   │   └── gh-actions.md
│   └── data
│       ├── database-dev.md
│       └── scripts
│           └── mysql.sql
├── instance
├── requirements.txt
├── server
│   ├── __init__.py
│   ├── api
│   │   └── v1
│   │       ├── __init__.py
│   │       └── routes
│   │           ├── __init__.py
│   │           ├── forum.py
│   │           ├── thesis.py
│   │           └── user.py
│   ├── app.py
│   ├── config.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── forum.py
│   │   ├── thesis.py
│   │   └── user.py
│   ├── static
│   ├── storage
│   ├── templates
│   └── utils
│       ├── __init__.py
│       └── auth.py
└── tests
    ├── __init__.py
    ├── scripts
    │   └── api.sh
    ├── test_forum_api.py
    ├── test_thesis_api.py
    └── test_user_api.py
```

* Front-End: React (JavaScript)
* Back-End: Python Flask
* Database: MySQL or MongoDB
* Design: Figma (for wireframes)
* Version Control: GitHub
* Testing Frameworks: Jest (Front-End), Pytest (Back-End)
* Deployment: Cloud-based hosting (e.g., AWS, Heroku)