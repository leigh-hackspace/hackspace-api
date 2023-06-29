# Hackspace API

An external-facing, FastAPI-based front-end for accessing some Leigh Hackspace data.

## Settings

| Env Var                  | Default Value           | Description                                                       |
| ------------------------ | ----------------------- | ----------------------------------------------------------------- |
| `BASE_URL`               | `http://localhost:8000` | URL that the API is accessible at, used to create self references |
| `PROMETHEUS_INSTANCE`    | `http://localhost:9090` | URL to the Prometheus instance to use for metrics and sensors     |
| `HOMEASSISTANT_INSTANCE` | `http://localhost:8123` | URL to the Home Assistant instance to use                         |
| `HOMEASSISTANT_TOKEN`    | nil                     | Long lived token used to access Home Assistant                    |

## Endpoints

### `/space.json`

Outputs a standard [SpaceAPI](https://spaceapi.io) endpoint.

### `/events.ics`

Dumps an iCal format list of events upcoming in the next 30 days.