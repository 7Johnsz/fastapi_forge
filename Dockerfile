FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    locales \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen pt_BR.UTF-8

ENV LANG=pt_BR.UTF-8 \
    LANGUAGE=pt_BR:pt \
    LC_ALL=pt_BR.UTF-8

WORKDIR /app

RUN pip install --no-cache-dir uv && \
    pip install --no-cache-dir --upgrade pip

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000