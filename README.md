# Music Band

Web application for presenting a music band, built with Flask. The project demonstrates work with templates, authentication, database, and forms.

## Technologies

- Flask 3.1.2
- SQLAlchemy 2.0.45
- Flask-Login
- Flask-WTF
- SQLite
- Tailwind CSS

## Project Structure

```
flask/
├── app/
│   ├── models/          # Data models (User, Album)
│   ├── services/        # Business logic
│   ├── templates/       # Jinja2 templates
│   ├── __init__.py      # Application factory
│   ├── routes.py        # Routes
│   ├── forms.py         # WTForms forms
├── instance/            # SQLite database
├── run.py              # Entry point
└── requirements.txt    # Dependencies
```

## Installation

1. Clone the repository or download the project files

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///band.db
```

2. Run the application:

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Features

### Public Pages

- Home page with band information
- About page
- Band history
- Album browsing

### Authentication

- User registration
- Login
- Logout

### Album Management (for authenticated users)

- View album list
- Album details
- Add new album
- Edit album
- Delete album

## Design

The project uses a minimalist design with consistent styling based on Tailwind CSS. All pages feature a unified light neutral theme with consistent components, typography, and color palette.

## Development

This project was created as an educational example of working with Flask and modern web technologies.

## License

This project is created for educational purposes.
