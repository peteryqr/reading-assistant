# Reading Assistant

A Django-based web application for reading and taking notes on PDF documents.

## Features

- User authentication (register/login)
- PDF document upload and management
- PDF text extraction and display
- Note-taking functionality (coming soon)
- Highlight text and associate notes with specific text selections (coming soon)

## Setup

1. Clone the repository:
```bash
git clone git@github.com:peteryqr/reading-assistant.git
cd reading-assistant
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000 in your web browser

## License

This project is licensed under the MIT License - see the LICENSE file for details. 