# 🚀 FastAPI Forge - Boilerplate 

A **robust**, **scalable**, and **modular** FastAPI boilerplate — designed for production-ready REST APIs.

> 🧰 Your starter kit for building modern, async APIs with FastAPI.

---

## ✨ Features

- ⚡ **High Performance** with **FastAPI** (async support).
- 🔒 **Rate Limiting** via **Redis** + **SlowAPI**.
- 🔧 **Structured Logging** using **Loguru**.
- 🛠️ **Error Notifications** via configurable **Discord Webhooks**.
- 🧱 **Modular Architecture** for easy scalability.
- 🐳 **Docker-Ready** with Dockerfile + Docker Compose.
- 🧪 **Testing Suite** with `pytest`.
- 🧬 **Environment Management** using `.env` files.
- 🚀 **Production-Ready Stack** with **Gunicorn** + **Uvicorn**.

---

## 📁 Project Structure

```
.
├── app/
│   ├── config/           # Middleware, events, app setup
│   ├── main.py           # App factory and FastAPI instance
│   └── v1/
│       ├── controllers/  # Route definitions
│       ├── models/       # Pydantic schemas
│       ├── service/      # Business logic (auth, webhooks)
│       ├── utils/        # Helper functions (UUIDs, etc.)
│       └── test/         # Unit/integration tests
├── entrypoint.py         # Entrypoint to run the app
├── main.py               # CLI entry for local dev
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Orchestrates services
├── pyproject.toml        # Project metadata & dependencies
├── uv.lock               # Dependency lockfile (uv)
├── .env, .env.dev        # Env variable configs
└── README.md             # This file
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- **Python** 3.13+
- [`uv`](https://github.com/astral-sh/uv) for dependency management
- **Docker** (optional but recommended)
- **Redis** (required for rate limiting)

---

### 🛠️ Installation

1. **Clone the project**

2. **Install dependencies**:

```bash
uv sync
```

3. **Run the API**:

- Locally:

```bash
uv run entrypoint.py dev
```

- With Docker:

```bash
docker-compose up --build
```

4. **Access the API**:

- API: [http://localhost:3008](http://localhost:3008)  
- Docs: [http://localhost:3008/scalar](http://localhost:3008/scalar)

---

## 🧪 Running Tests

```bash
uv run pytest app/v1/test -v
```

---

## 🧱 Architecture Overview

| Layer         | Description                                        |
|---------------|----------------------------------------------------|
| Controllers   | Route handlers and routers                         |
| Models        | Pydantic-based request/response schemas            |
| Service       | Core business logic, authentication, webhooks      |
| Utils         | Reusable helpers (UUIDs, file handling, etc.)      |
| Config        | Middleware, events, CORS, rate limiting setup      |

---

## 🛡️ Middleware

- **CORS**: Cross-origin request support.
- **GZip**: Compression for large responses.
- **Rate Limiting**: Per-IP throttling with Redis + SlowAPI.
- **Exception Handling**: Friendly error responses with webhook support.

---

## 📈 Logging & Monitoring

- ✅ **Loguru**: Beautiful, structured, and filterable logs.
- 📡 **Webhooks**: Discord-ready alerts for critical events.

---

## 📦 Deployment

### 🐳 Docker

```bash
docker-compose up --build
```

---

### 🌐 Environment Variables

Sample `.env` configuration:

```env
APP_ENV=dev
REDIS_URL=redis://localhost:6379
WEBHOOK_URL=https://discord.com/api/webhooks/...
```

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

Have questions or feedback?  
Open an issue or reach out via [contato@devjohn.com.br](mailto:contato@devjohn.com.b).