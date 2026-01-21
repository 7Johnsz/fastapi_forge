<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="100" alt="FastAPI Logo" />
</p>

<h1 align="center">⚡ FastAPI Forge</h1>

<p align="center">
  <strong>A modern, production-ready FastAPI boilerplate</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0.1-blue?style=for-the-badge" alt="Version" />
  <img src="https://img.shields.io/badge/python-3.13+-green?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License" />
</p>

---

## 📖 About

**FastAPI Forge** is a robust and scalable boilerplate for FastAPI applications. Designed to accelerate modern API development, it provides a well-organized structure with best practices already configured.

---

## 🚀 Tech Stack

| Category | Technology |
|----------|------------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) - Modern, high-performance web framework |
| **ORM** | [SQLModel](https://sqlmodel.tiangolo.com/) - SQL databases in Python with type hints |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) - Database migrations |
| **Database** | [PostgreSQL](https://www.postgresql.org/) - Relational database |
| **Cache** | [Redis](https://redis.io/) - In-memory cache and storage |
| **Auth** | [PyJWT](https://pyjwt.readthedocs.io/) + [Bcrypt](https://github.com/pyca/bcrypt) - JWT authentication |
| **Serialization** | [ORJSON](https://github.com/ijl/orjson) - Ultra-fast JSON serialization |
| **Logging** | [Loguru](https://github.com/Delgan/loguru) - Simplified logging |
| **Settings** | [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) - Configuration management |
| **Docs** | [Scalar](https://scalar.com/) - Modern API documentation |
| **Package Manager** | [UV](https://github.com/astral-sh/uv) - Ultra-fast package manager |
| **Containerization** | [Docker](https://www.docker.com/) - Containerization |
| **Reverse Proxy** | [Traefik](https://traefik.io/) - Reverse proxy and load balancer |

---

## 📁 Project Structure

```
fastapi_forge/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── controllers/    # Routes and controllers
│   │       ├── models/         # SQLModel models
│   │       ├── service/        # Business logic
│   │       ├── utils/          # Utilities
│   │       └── worker/         # Workers and tasks
│   ├── config/
│   │   ├── middleware/         # Middlewares (CORS, Redis, etc.)
│   │   └── handlers/           # Event handlers
│   └── main.py                 # Application entry point
├── alembic/                    # Database migrations
├── docker-compose.yml          # Container orchestration
├── Dockerfile                  # Docker image build
├── entrypoint.py               # Startup script
└── pyproject.toml              # Dependencies (UV)
```

---

## ⚙️ Prerequisites

- **Python** 3.13+
- **UV** (Package manager)
- **Docker** & **Docker Compose** (for production)
- **PostgreSQL** (local or via Docker)
- **Redis** (local or via Docker)

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi_forge.git
cd fastapi_forge
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

```bash
# For development
cp .env.dev.example .env.dev

# For production
cp .env.example .env
```

### 4. Run migrations

```bash
uv run alembic upgrade head
```

---

## 🏃 Running

### Development

```bash
uv run entrypoint.py dev
```

### Production (Docker)

```bash
docker-compose up -d
```

---

## 🐳 Docker

The project includes complete Docker configuration with:

- **API** - Main application container
- **PostgreSQL** - Database
- **Redis** - Cache and sessions
- **Migrations** - Container for automatic migrations
- **Traefik** - Reverse proxy with automatic HTTPS

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

---

## 📚 API Documentation

In development mode, documentation is available at:

- **Scalar UI**: `http://localhost:{PORT}/docs`

---

## 🔐 Authentication

The project uses JWT (JSON Web Tokens) for authentication:

- `POST /signup` - User registration
- `POST /login` - Login and token retrieval
- `POST /logout` - Logout
- `POST /refresh` - Token refresh

---

## 🛠️ Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page |
| `GET` | `/ping` | Health check |
| `GET` | `/memory` | Memory usage |
| `POST` | `/signup` | Registration |
| `POST` | `/login` | Login |
| `POST` | `/logout` | Logout |
| `POST` | `/refresh` | Refresh token |

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.