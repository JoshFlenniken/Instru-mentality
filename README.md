## Instru-Mentality Inventory App (Flask + MySQL)

All code is based on the CS 340 starter code, with the exception of the code in `DDL.sql`, `DML.sql`, and `plsql.sql`.

This project is a simple inventory and order management system for an independent musical instrument store. It showcases:

- **Flask** for the web UI and routing
- **MySQL** for relational data storage
- **Jinja templates** for server-side rendering

Main pages:

- `Home`: welcome / reset actions
- `Customers`, `Employees`, `Orders`, `Products`, `Order Details`: CRUD-style views over the backing tables and stored procedures.

---

## Architecture Overview

- **`app.py`**: Main Flask application, route handlers, and app entrypoint for local development.
- **`config.py`**: Central configuration, reading from environment variables (with safe dev defaults) for:
  - Flask environment (`FLASK_ENV`, `FLASK_DEBUG`, `PORT`)
  - Database connection (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`)
- **`database/db_connector.py`**: Thin wrapper around `mysqlclient` (`MySQLdb`), now using the values from `Config` instead of hardcoded credentials.
- **`templates/*.j2`**: Jinja templates for each page; `main.j2` is the base layout.
- **`static/style.css`**: Global styling.
- **`wsgi.py`**: WSGI entrypoint (`app` callable) for production servers like Gunicorn.
- **`DDL.sql`, `DML.sql`, `database/plsql.sql`**: Schema, seed data, and stored procedures.

High-level data flow:

1. Browser sends a request to Flask route in `app.py`.
2. Route uses `database.db_connector.connectDB()` and `query()` to talk to MySQL.
3. Query results are passed into a Jinja template in `templates/`.
4. Template renders HTML with data and links to static CSS via `url_for('static', ...)`.

---

## Local Development Setup

You can develop quickly on your Mac without running MySQL locally by pointing the app at a hosted MySQL instance (recommended), or you can run MySQL locally (via Homebrew or Docker).

### 1. Create and activate a virtualenv

```bash
cd MySQL_Flask_Site
python -m venv .venv
source .venv/bin/activate  # on macOS/Linux
```

Then install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure environment variables (.env)

Create a `.env` file in the project root (same folder as `config.py`) with at least:

```bash
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000

DB_HOST=your-mysql-host
DB_USER=your-mysql-username
DB_PASSWORD=your-mysql-password
DB_NAME=your-mysql-database
```

For development, you have two main options:

- **Shared hosted MySQL (recommended for simplicity)**  
  - Use a managed MySQL provider (e.g. PlanetScale) or a MySQL add-on from your chosen PaaS.
  - Configure the host, username, password, and DB name in your `.env` to point to that remote instance.
- **Local MySQL (optional)**  
  - Install MySQL via Homebrew or run it via Docker (see Docker section below).
  - Point `DB_HOST` to `127.0.0.1` and use your local MySQL credentials.

### 3. Run the app locally

With your virtualenv activated and `.env` configured:

```bash
python app.py
```

By default, the app will:

- Bind on `0.0.0.0`
- Use `PORT` from your environment (default 5000)
- Use `FLASK_DEBUG` to control debug mode (on for development)

Visit `http://localhost:5000` in your browser.

To initialize schema/data on a fresh database, run the SQL files in this order using your MySQL client:

1. `DDL.sql` – creates tables.
2. `DML.sql` – inserts sample data.
3. `database/plsql.sql` – creates stored procedures used by the app.

---

## Production Deployment (Low-Cost Portfolio-Friendly)

The recommended production setup is:

- **App hosting**: a modern PaaS with a free or low-cost plan (e.g. Render or Railway), deployed via this repo and the included `Dockerfile`.
- **Database**: a managed MySQL provider with a free/cheap tier (e.g. PlanetScale or a MySQL add-on from your PaaS).

### 1. Prepare a managed MySQL database

1. Sign up for a provider (e.g. PlanetScale).
2. Create a new database (e.g. `instrument_inventory`).
3. Create a username/password with access to that database.
4. Note the connection details:
   - Host
   - Username
   - Password
   - Database name
5. Run `DDL.sql`, `DML.sql`, and `database/plsql.sql` against that database to create tables, seed data, and stored procedures.

### 2. Deploy the Flask app using Docker

Most PaaS platforms can:

- Build your container from the included `Dockerfile`.
- Inject environment variables via their dashboard.

Typical steps (example with a generic PaaS workflow):

1. Push this repository to a Git hosting service (GitHub, GitLab, etc.).
2. Create a new web service on your PaaS and connect it to the repo.
3. Configure the service to build using the `Dockerfile` in the project root.
4. Set environment variables in the PaaS dashboard:
   - `FLASK_ENV=production`
   - `FLASK_DEBUG=0`
   - `DB_HOST=...` (from your managed MySQL)
   - `DB_USER=...`
   - `DB_PASSWORD=...`
   - `DB_NAME=...`
   - The PaaS will typically inject `PORT` automatically; the Docker image already respects that.
5. Deploy. The platform will build the image, run `gunicorn wsgi:app --bind 0.0.0.0:$PORT`, and expose an HTTPS URL you can share with employers.

This yields a **professional-looking deployment** with:

- A dedicated web URL.
- Managed TLS (HTTPS).
- Managed MySQL (backups, durability handled by provider).

---

## Optional: Docker-Based Local Development

If you prefer a fully containerized local setup, you can add a `docker-compose.yml` like:

```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: "1"
      PORT: 5000
      DB_HOST: db
      DB_USER: app_user
      DB_PASSWORD: app_password
      DB_NAME: instru_mentality
    depends_on:
      - db

  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: instru_mentality
      MYSQL_USER: app_user
      MYSQL_PASSWORD: app_password
    ports:
      - "3306:3306"
```

Then you can run:

```bash
docker compose up --build
```

Once the database is up, apply `DDL.sql`, `DML.sql`, and `database/plsql.sql` to the `instru_mentality` database inside the `db` service using your preferred MySQL client or `docker exec`.

This is optional and mainly useful if you want to highlight Docker skills in your portfolio.

---

## What Could Be Improved Next

If you want to extend this project further for portfolio purposes, some natural next steps:

- Add automated tests for the DB layer and routes.
- Introduce a migration tool (e.g. Alembic) instead of raw SQL files.
- Add authentication/authorization for staff vs. front-of-house roles.
- Add more detailed error handling and structured logging for production.
