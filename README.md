# Hackspace API

An external-facing, FastAPI-based front-end for accessing some Leigh Hackspace data.

## Settings

| Env Var               | Default Value           | Description                                                   |
| --------------------- | ----------------------- | ------------------------------------------------------------- |
| `PROMETHEUS_INSTANCE` | `http://10.3.1.30:9090` | URL to the Prometheus instance to use for metrics and sensors |

## Endpoints

### `/space.json`

Outputs a standard [SpaceAPI](https://spaceapi.io) endpoint.