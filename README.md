# Shortly — URL Shortener

A full-stack URL shortener built with **FastAPI**, **PostgreSQL**, and a lightweight **HTML, CSS, and JavaScript** frontend. Shortly converts long URLs into compact, shareable links and provides an authenticated dashboard for managing them.

## Live Demo

- **Frontend:** [Open Shortly](https://playful-dragon-9acff8.netlify.app/)
- **Backend API:** [Open API](https://url-shortener-api-g45f.onrender.com/)
- **API documentation:** [Swagger UI](https://url-shortener-api-g45f.onrender.com/docs)

## Overview

Shortly makes it easy to create and manage short links. Users can register, log in, create short URLs, view links associated with their account, edit or delete them, and share them with others. Anyone with a short link can open it and be redirected to the original destination.

The frontend is hosted separately from the backend. The FastAPI application exposes REST endpoints, while PostgreSQL stores user and URL data.

## Features

- User registration and login with email and password
- JWT-based authentication for protected endpoints
- Secure password hashing
- Unique short-code generation
- Public redirection from short links to original URLs
- Authenticated dashboard for managing a user's own links
- Create, list, update, and delete URL records
- Click-count tracking
- PostgreSQL persistence
- Database schema migrations with Alembic
- Interactive API documentation with Swagger UI

## Tech Stack

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI |
| ORM | SQLAlchemy 2.x |
| Validation and settings | Pydantic, Pydantic Settings |
| Authentication | JWT (PyJWT), OAuth2 password form |
| Password hashing | pwdlib with Argon2 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Database hosting | Neon |
| Backend hosting | Render |
| Frontend hosting | Netlify |

## Architecture

```text
                   User's Browser
                         |
                         v
             +------------------------+
             |       Frontend         |
             |      HTML / CSS / JS   |
             |        Netlify         |
             +------------------------+
                         |
                    REST / HTTP
             JWT on protected requests
                         |
                         v
             +------------------------+
             |       FastAPI          |
             |        Render          |
             |                        |
             | Authentication         |
             | URL management         |
             | Short-link redirects   |
             +------------------------+
                         |
                     SQLAlchemy
                         |
                         v
             +------------------------+
             |      PostgreSQL        |
             |         Neon           |
             +------------------------+
```

### How it works

1. A user opens the frontend hosted on Netlify.
2. The frontend sends API requests to the FastAPI backend hosted on Render.
3. A user registers or logs in. The login endpoint returns a JWT access token.
4. The frontend includes the token in the `Authorization: Bearer <token>` header when calling protected endpoints.
5. FastAPI validates the token and identifies the authenticated user.
6. SQLAlchemy reads or updates the relevant records in PostgreSQL.
7. When a visitor opens a short link, the public redirect endpoint looks up its short code, increments its click count, and redirects the visitor to the original URL.

## Project Structure

The backend is organized into modules for configuration, database access, models, schemas, routers, services, authentication dependencies, and utility functions.

```textURL-Shortener/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── database/
│   │   └── connections.py
│   ├── models/
│   │   ├── url.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── url.py
│   │   └── user.py
│   ├── routers/
│   │   ├── urls.py
│   │   ├── redirect.py
│   │   └── auth.py
│   ├── services/
│   │   ├── url_service.py
│   │   └── user_service.py
│   ├── dependencies/
│   │   └── auth.py
│   ├── utils/
│   │   └── short_code.py
│   └── frontend/
│       └── index.html
├── migrations/
├── .env.example
├── alembic.ini
├── pyproject.toml
└── uv.lock
```

> Adjust this tree if your GitHub repository uses a different layout or contains additional files.

## Run Locally

### Prerequisites

- Python 3.11 or later
- PostgreSQL, or a Neon PostgreSQL database
- Git
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd URL-Shortener
```

### 2. Install dependencies

If the repository includes `pyproject.toml` and `uv.lock`, run:

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require
DATABASE_URL_DIRECT=postgresql+psycopg://USER:PASSWORD@DIRECT_HOST/DATABASE?sslmode=require

BASE_URL=http://localhost:8000

JWT_SECRET_KEY=replace_with_a_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string used by the application |
| `DATABASE_URL_DIRECT` | Direct database connection string used for migrations, where required |
| `BASE_URL` | Base address used to construct short links |
| `JWT_SECRET_KEY` | Secret used to sign and verify JWTs |
| `JWT_ALGORITHM` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime in minutes |

**Important:** Never commit your real `.env` file. Keep it in `.gitignore` and commit only an `.env.example` containing placeholder values. Never put database credentials or the JWT secret in frontend code.

### 4. Run database migrations

```bash
uv run alembic upgrade head
```

### 5. Start the backend

```bash
uv run uvicorn app.main:app --reload
```

The local backend will be available at:

- API: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 6. Run the frontend

Open `frontend/index.html` in your browser, or serve the frontend folder with a local development server such as the VS Code Live Server extension.

For local development, make sure the frontend's API base URL points to `http://localhost:8000`. The deployed frontend should point to the Render backend.

## API Reference

The deployed API's interactive documentation is available at:

**[https://url-shortener-api-g45f.onrender.com/docs](https://url-shortener-api-g45f.onrender.com/docs)**

The following is a high-level endpoint overview. Check Swagger UI for the exact request and response schemas exposed by the deployed version.

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `POST` | `/auth/register` | Create a user account | Not required |
| `POST` | `/auth/login` | Log in and receive an access token | Not required |

Registration accepts JSON similar to:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

The login endpoint accepts form data (`application/x-www-form-urlencoded`). The email is sent in the `username` field:

```text
username=user@example.com
password=your-password
```

### URL management

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `POST` | `/urls/` | Create a short URL | Required |
| `GET` | `/urls/` | List the current user's URLs | Required |
| `PATCH` | `/urls/{url_id}` | Update a URL | Required |
| `DELETE` | `/urls/{url_id}` | Delete a URL | Required |

### Redirection

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `GET` | `/{short_code}` | Redirect to the original URL and record a click | Not required |

### Authorization header

For protected endpoints, include the access token returned by `/auth/login`:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

URL-management operations are scoped to the authenticated user. Short-link redirection is public so recipients can use shared links without signing in.

## Deployment

The deployed application uses three services:

| Component | Platform |
|---|---|
| Frontend | [Netlify](https://www.netlify.com/) |
| Backend | [Render](https://render.com/) |
| PostgreSQL database | [Neon](https://neon.tech/) |

For deployment:

1. Set the frontend API base URL to the Render backend URL.
2. Configure the required environment variables in Render.
3. Set the production `BASE_URL` to `https://url-shortener-api-g45f.onrender.com`.
4. Configure the Neon database connection strings.
5. Apply Alembic migrations to the intended database.
6. Ensure the backend CORS allowlist includes the deployed Netlify origin: `https://playful-dragon-9acff8.netlify.app`.

CORS controls which browser origins may access API responses. It does not replace authentication; protected endpoints must still validate JWTs.

## Security Considerations

- Passwords are hashed before being stored.
- Protected endpoints require a valid JWT access token.
- URL-management operations check ownership so users manage only their own links.
- Redirect endpoints are public by design.
- Keep `.env`, database credentials, and JWT signing secrets out of source control.
- Use HTTPS for deployed frontend and backend traffic.
- For a production system, review browser token storage and consider secure `HttpOnly` and `SameSite` cookies, along with appropriate XSS protections.

## Future Enhancements

Possible improvements for future versions:

- QR-code generation
- Custom short aliases
- Link expiration dates
- Detailed analytics and click history
- Rate limiting and abuse prevention
- Malicious-link detection
- Email verification and password reset
- Refresh-token rotation and session management
- Automated tests and CI/CD pipeline

## Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Open a pull request describing the changes.

## Author

**Rishi Bisht**

- GitHub: [GitHub profile](https://github.com/)

---

*Built with FastAPI, PostgreSQL, and JavaScript.*
