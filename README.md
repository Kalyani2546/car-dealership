# Cars Dealership

A full-stack dealership directory and review application built with Django, React, and SQLite. Customers can browse U.S. dealerships, filter by state, register and sign in, read and submit reviews, and inspect lightweight sentiment analysis. The repository also includes Docker, GitHub Actions, sample data, and IBM Cloud Code Engine deployment guidance.

## Features

- Dealer directory, dealership details, and Kansas/state filtering
- Account registration, login, logout, and authenticated review submission
- Dealer reviews and sentiment analysis for review text
- Responsive React interface plus standalone Django About Us and Contact Us pages
- SQLite sample database, Docker image, and CI checks

## Run locally

### Backend

```powershell
cd server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_dealerships
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`. The Django runserver output should be saved as `django_server.txt` if evidence is required.

### Frontend

In a second terminal:

```powershell
cd frontend\client
npm install
npm run dev
```

Open the Vite URL (normally `http://localhost:5173`). Vite proxies API requests to Django. Use the registration form to create a local account; no sample password or production user is included.

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/csrf/` | Set the CSRF cookie before session-authenticated POST requests |
| POST | `/api/register/` | Create a user (`username`, `first_name`, `last_name`, `email`, `password`) |
| POST | `/api/login/` | Log in (`username`, `password`) |
| POST | `/api/logout/` | Log out the current session |
| GET | `/api/me/` | Current session user and authentication status |
| GET | `/api/dealers/` | List dealerships; optional `?state=KS` |
| GET | `/api/dealers/<id>/` | Dealership details |
| GET | `/api/dealers/<id>/reviews/` | Reviews for one dealership |
| POST | `/api/reviews/` | Add a review (`dealer_id`, `rating` 1–5, `review`) while signed in |
| GET | `/api/cars/` | All available makes and models |
| POST | `/api/analyze-review/` | Analyze review text (`review`) |

Session-changing requests require a CSRF token. Fetch `/api/csrf/`, read the `csrftoken` cookie, and send it as the `X-CSRFToken` header with the same cookie. The React client handles this automatically. See `docs/api-examples.md` for PowerShell/cURL examples and evidence limitations.

## Static assignment pages

- `server/frontend/static/About.html`
- `server/frontend/static/Contact.html`

They are served at `/about/` and `/contact/`, and use the shared `site.css` stylesheet. The React registration form is at `server/frontend/src/components/Register/Register.jsx`.

## Docker

From the repository root:

```powershell
docker build -t cars-dealership .
docker run --rm -p 8000:8000 -e DJANGO_SECRET_KEY="replace-with-a-long-random-value" cars-dealership
```

The container uses SQLite for this learning project. For persistent production data, configure a managed database and persistent storage before deployment.

## GitHub Actions

The workflow at `.github/workflows/ci.yml` runs Django checks and tests, then installs frontend dependencies and builds the React app.

## Deploy to Render (assignment demo)

See `docs/deployment.md` and the root `render.yaml` Blueprint. Connect the GitHub repository to Render, create the Blueprint service, and use the assigned public URL. The demo uses ephemeral SQLite storage, so do not use it for real customer data.

## Deploy to IBM Cloud Code Engine

See `docs/deployment.md` for Code Engine guidance. Deployment requires an activated IBM Cloud account, CLI login, a Code Engine project, and a configured secret. Do not commit credentials.

## Evidence checklist

Screenshots, live URLs, GitHub URLs, successful workflow logs, and terminal/cURL transcripts must come from your own running environment and account. The project does not fabricate screenshots, deployment URLs, workflow results, or login/logout evidence. Follow `docs/api-examples.md` and save genuine command outputs under the filenames requested by the assignment.
