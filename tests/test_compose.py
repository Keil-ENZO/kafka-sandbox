"""Guards on the Compose file: what must stay true whatever gets added to it."""

from pathlib import Path

import yaml

COMPOSE = Path(__file__).resolve().parent.parent / "infra" / "docker-compose.yml"
SERVICES = yaml.safe_load(COMPOSE.read_text())["services"]
BROKERS = {name: svc for name, svc in SERVICES.items() if name.startswith("broker-")}


def test_three_brokers() -> None:
    assert sorted(BROKERS) == ["broker-1", "broker-2", "broker-3"]


def test_every_published_port_binds_to_localhost() -> None:
    for name, svc in SERVICES.items():
        for port in svc.get("ports", []):
            assert str(port).startswith("127.0.0.1:"), f"{name} publishes {port} beyond localhost"


def test_images_are_pinned() -> None:
    for name, svc in SERVICES.items():
        tag = svc["image"].rpartition(":")[2]
        assert tag and tag != "latest" and "/" not in tag, f"{name} uses an unpinned image"


def test_node_ids_are_unique_and_in_the_quorum() -> None:
    ids = [svc["environment"]["KAFKA_NODE_ID"] for svc in BROKERS.values()]
    assert sorted(ids) == [1, 2, 3]
    for name, svc in BROKERS.items():
        env = svc["environment"]
        assert f"{env['KAFKA_NODE_ID']}@{name}:9093" in env["KAFKA_CONTROLLER_QUORUM_VOTERS"]


def test_each_broker_advertises_its_own_host_port() -> None:
    for name, svc in BROKERS.items():
        host_port = str(svc["ports"][0]).split(":")[1]
        assert f"EXTERNAL://localhost:{host_port}" in svc["environment"]["KAFKA_ADVERTISED_LISTENERS"]
        assert f"INTERNAL://{name}:9092" in svc["environment"]["KAFKA_ADVERTISED_LISTENERS"]
