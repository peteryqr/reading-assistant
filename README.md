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
git clone <repository-url>
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

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000 in your web browser

## Usage

1. Register a new account or log in
2. Upload PDF documents through the web interface
3. View your documents and their contents
4. Take notes while reading (feature coming soon)
5. Highlight text and associate notes with selections (feature coming soon)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 