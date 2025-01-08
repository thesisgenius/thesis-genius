# Use a lightweight base image
FROM python:3.10-slim AS dev-api

# NAME and VERSION are the name of the software
# and the version to download. Example: NAME=thesisgenius-api VERSION=.
ARG BIN_NAME=thesisgenius-api
ARG VERSION
ARG TARGETARCH
ARG TARGETOS
ARG APPLICATION_PORT=8557

ENV PRODUCT_NAME=$BIN_NAME

# Flask environment variables
ENV FLASK_PORT=${APPLICATION_PORT}
ENV FLASK_ENV=development

# Gunicorn environment variables
ENV GUNICORN_BIND_ADDR="0.0.0.0:${FLASK_PORT}"

LABEL name=${BIN_NAME} \
      maintainer="Team ThesisGenius <support@thesis-genius.com>" \
      vendor="ThesisGenius" \
      version=${VERSION} \
      release=${VERSION} \
      summary="ThesisGenius provides AI integrated API thesis-genius.com." \
      description="ThesisGenius provides AI integrated API thesis-genius.com."

COPY ../LICENSE /usr/share/doc/$PRODUCT_NAME/LICENSE.txt

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY backend/ server/

# Copy the default (dev) .env file for environment variables
COPY ../build-support/docker/.env .

# Expose application port
EXPOSE ${FLASK_PORT}

# Command to run the Flask app with Gunicorn
# gunicorn --workers 3 --bind 0.0.0.0:8557 "backend:create_app()"
CMD ["sh", "-c", "gunicorn --workers 2 --bind 0.0.0.0:${FLASK_PORT} 'server:create_app()'"]