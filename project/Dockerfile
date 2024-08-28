# Base stage
FROM python:3.10 AS base

WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js and npm
RUN apt-get update && \
    apt-get upgrade -y && \
    curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh | bash - && \
    apt-get install -y nodejs && \
    apt-get install -y npm

COPY . .

# Install Node.js dependencies in the subfolder
RUN cd ft_transcendence/frontend && npm install && npm run build

# Development stage
FROM base AS development

# Expose the port for the Django server
EXPOSE 8000

# Set environment variables for development
ENV DJANGO_SETTINGS_MODULE=ft_transcendence.settings

# Command to run the Django development server
# Command to run both Node.js development server and Django server
# Entrypoint script to handle migrations and start the server
COPY entrypoint-dev.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]

# Production stage
FROM base AS production

# Collect static files
RUN python manage.py collectstatic --noinput

# Set environment variables for production
ENV DJANGO_SETTINGS_MODULE=ft_transcendence.settings

# Expose the port for the Django server
EXPOSE 8000

# Entrypoint script to handle migrations and start the server
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create a non-root user and set permissions
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Create a directory for the app and change ownership
RUN mkdir -p /usr/src/app && chown -R appuser:appgroup /usr/src/app

# Switch to the non-root user
USER appuser

ENTRYPOINT ["entrypoint.sh"]