# Variables
# DOCKER_COMPOSE_DEV = docker-compose -f docker-compose-dev.yml
DOCKER_COMPOSE_PROD = docker compose

# Commands
.PHONY: help dev-build dev-up dev-down dev-migrate dev-shell prod-build prod-up prod-down prod-migrate prod-shell

help: ## Show this help
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# dev-build: ## Build the development environment
# 	$(DOCKER_COMPOSE_DEV) build

# dev-up: ## Start the development environment
# 	$(DOCKER_COMPOSE_DEV) up --build

# dev-down: ## Stop the development environment
# 	$(DOCKER_COMPOSE_DEV) down

# dev-migrate: ## Apply migrations in the development environment
# 	$(DOCKER_COMPOSE_DEV) run web python manage.py migrate

# dev-shell: ## Get a shell in the development web container
# 	docker exec -it ft_transcendence_web_1 /bin/bash

prod-build: ## Build the production environment
	$(DOCKER_COMPOSE_PROD) build

prod-up: ## Start the production environment (generate certificates if missing)
	@if [ ! -f nginx/ssl/server.crt ] || [ ! -f nginx/ssl/server.key ]; then \
		echo "Certificates missing, generating..."; \
		$(DOCKER_COMPOSE_PROD) --profile generate-certificates run --rm certificates; \
	else \
		echo "Certificates already exist, skipping generation."; \
	fi
	$(DOCKER_COMPOSE_PROD) down --remove-orphans
	$(DOCKER_COMPOSE_PROD) up --build

prod-down: ## Stop the production environment
	$(DOCKER_COMPOSE_PROD) down

prod-migrate: ## Apply migrations in the production environment
	$(DOCKER_COMPOSE_PROD) run web python manage.py migrate

prod-shell: ## Get a shell in the production web container
	docker exec -it ft_transcendence_web_prod_1 /bin/bash
