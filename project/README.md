# ft_transcendence

This project uses Docker to manage both development and production environments. Below are the instructions to set up and run the application in both environments.

## Requirements

- Docker
- Docker Compose

## Getting Started

### Development Environment

1. **Build the Development Environment:**

    ```bash
    make dev-build
    ```

2. **Start the Development Environment:**

    ```bash
    make dev-up
    ```

   This will build and start the Docker containers for development.

3. **Stop the Development Environment:**

    ```bash
    make dev-down
    ```

4. **Apply Migrations in Development:**

    ```bash
    make dev-migrate
    ```

5. **Get a Shell in the Development Web Container:**

    ```bash
    make dev-shell
    ```

   This will open a shell session in the `web` container.

### Production Environment

1. **Build the Production Environment:**

    ```bash
    make prod-build
    ```

2. **Start the Production Environment:**

    ```bash
    make prod-up
    ```

   This will build and start the Docker containers for production in detached mode.

3. **Stop the Production Environment:**

    ```bash
    make prod-down
    ```

4. **Apply Migrations in Production:**

    ```bash
    make prod-migrate
    ```

5. **Get a Shell in the Production Web Container:**

    ```bash
    make prod-shell
    ```

   This will open a shell session in the `web_prod` container.

### Makefile Commands
The Makefile provides a set of commands for managing Docker containers for both development and production. Use make help to see all available commands.
```bash
make help
```