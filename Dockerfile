ARG PYTHON_ENV_ARG=3.9

# Builder stage
FROM python:${PYTHON_ENV_ARG}-alpine AS builder
COPY requirements.txt .

# Install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# Final image stage
FROM python:${PYTHON_ENV_ARG}-alpine
WORKDIR /code

# Copy the dependencies installation from the builder stage image
COPY --from=builder /root/.local/bin /root/.local
COPY --from=builder /root/.local/lib /root/.local

# Copy source code
COPY ./src .

# Update environment variables
ENV PATH=/root/.local:$PATH
ARG PYTHON_ENV_ARG
ENV PYTHONPATH=/root/.local/python${PYTHON_ENV_ARG}/site-packages

ENTRYPOINT [ "python", "./siras.py" ]
