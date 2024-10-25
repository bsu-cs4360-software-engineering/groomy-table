# groomy-table

## Functional Requirements
- User can create an account
- User can login / authenticate
- User can CRUD Appointments
- User can CRUD Notes
- User can CRUD Services
- User can CRUD Invoices
- User can see a map of the local area (integrated with a mapping library)
- The map shows a path from the current location to the next appointment
- User can "take payments" (mock payment handling; no actual payment processor involved)

## Nonfunctional Requirements
- GUI based
- Unit testing is the primary source of documentation
- Web-based

## Standards / Conventions
- Languages: Python/HTML/JavaScript
- Frameworks: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- Database: SQLite
- Directory Structure:
    - `static`: CSS, JS, Images
    - `models`: Classes
    - `templates`: HTML
    - `routes`: Routing Blueprints
    - `tests`: Unit Tests
- Naming Conventions
    - Variables: snake_case
    - Methods/Functions: snake_case
    - Classes: PascalCase

### Security

User passwords are hashed using **Werkzeug** security functions.

## Design

### Variables
- `primary: #56b8e6;` (for active elements/main accent color)
- `highlight: #1d81af;` (secondary accent for headers and hover effects)
- `black: #101010;` (standard text/other dark elements)
- `background: #fcfcfc;` (off white background for entire site)
- `clear-border: 1px solid rgba(255, 255, 255, 0.3);` (border for footer/nav/form elements)
- `border-radius: 20px;` (standard border radius for circular borders on main elements)
- `grey-background: rgba(145, 141, 141, 0.1);` (background color for footer/nav/form elements)

### General Style
- `font-family: Arial, sans-serif;`
- `line-height: 1.5;`
- Global Settings:
    - `margin: 0;`
    - `padding: 0;`
    - `box-sizing: border-box;`