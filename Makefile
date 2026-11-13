COMPOSE := docker compose -f infra/docker-compose.yml

.PHONY: up down reset ps logs shell lint test

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

## Open a shell inside broker-1, where the Kafka command-line tools live.
shell:
	@$(COMPOSE) exec broker-1 bash || true

lint:
	uv run ruff check .

test:
	uv run pytest
