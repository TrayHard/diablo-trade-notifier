# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim AS base
LABEL org.opencontainers.image.authors="Ilia Poliakov <trayhardplay@gmail.com>"
LABEL version="1.0.0"

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/diablo-trade-notifier" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

WORKDIR /home/diablo-trade-notifier/
COPY main.py /home/diablo-trade-notifier/main.py
COPY .env /home/diablo-trade-notifier/.env
COPY requirements.txt /home/diablo-trade-notifier/requirements.txt
COPY session_id.txt /home/diablo-trade-notifier/session_id.txt

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

WORKDIR /home/diablo-trade-notifier/
# Run the application.
CMD ["python3", "-m", "main"]
