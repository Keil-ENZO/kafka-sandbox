COMPOSE := docker compose -f infra/docker-compose.yml

.PHONY: up down reset ps logs lint test

## Start the cluster and wait until every broker is healthy.
up:
	$(COMPOSE) up -d --wait --wait-timeout 120

## Stop the cluster. Data is kept.
down:
	$(COMPOSE) down

## Stop the cluster and delete its data. The next `make up` starts from an empty cluster.
reset:
	$(COMPOSE) down -v

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f --tail 100

lint:
	uv run ruff check .

test:
	uv run pytest
