# Networking: who talks to the brokers, and on which port

A broker tells every client where to reach it. That address is the *advertised listener*, and it must be valid from where the client stands. A container and the host do not see the same network, so each broker has two client listeners.

| Listener | Port | Advertised as | Used by |
|---|---|---|---|
| `INTERNAL` | 9092 | `broker-N:9092` | other brokers, and any container on the Compose network |
| `EXTERNAL` | 19092, 29092, 39092 | `localhost:<port>` | tools running on the host |
| `CONTROLLER` | 9093 | not advertised | the KRaft quorum only, never clients |

A client connects to one broker, the *bootstrap server*, gets the advertised address of all three, then talks to each one directly. That is why every broker needs its own host port.

- From a container: `--bootstrap-server broker-1:9092`
- From the host: `--bootstrap-server localhost:19092`

Mixing them up is the classic mistake: the first connection works, then the client is told to reach `broker-1:9092`, a name the host cannot resolve.

Host ports are published on `127.0.0.1` only. Nothing is reachable from another machine.
