# Hackspace API

An external-facing, FastAPI-based front-end for accessing some Leigh Hackspace data.

## Settings

| Env Var                     | Default Value                                                                                           | Description                                                    |
| --------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `BASE_URL`                  | `http://localhost:8000`                                                                                 | URL base where the application will be accessible at           |
| `PROMETHEUS_INSTANCE`       | `http://prometheus:9090`                                                                                | Endpoint URL for the Prometheus instance                       |
| `HOMEASSISTANT_INSTANCE`    | `http://homeassistant:8123`                                                                             | Endpoint URL for the Home Assistant instance                   |
| `HOMEASSISTANT_TOKEN`       |                                                                                                         | Token used to access the Home Assistant API                    |
| `HACKSPACE_NAME`            | `Leigh Hackspace`                                                                                       | Name of the hackspace                                          |
| `HACKSPACE_LOGO_URL`        | `https://raw.githubusercontent.com/leigh-hackspace/logos-graphics-assets/master/logo/rose_logo.svg`     | URL to the logo for the hackspace                              |
| `HACKSPACE_WEBSITE_URL`     | `https://leighhack.org`                                                                                 | URL to the hackspace's website                                 |
| `HACKSPACE_ADDRESS`         | `Leigh Hackspace, Unit 3.14, 3rd Floor, Leigh Spinners Mill, Park Lane, Leigh, WN7 2LB, United Kingdom` | Full address to the hackspace                                  |
| `HACKSPACE_ADDRESS_LAT`     | `53.493012`                                                                                             | Latitude of the hackspace                                      |
| `HACKSPACE_ADDRESS_LON`     | `-2.49301`                                                                                              | Longitude of the hackspace                                     |
| `HACKSPACE_TIMEZONE`        | `Europe/London`                                                                                         | Timezone the hackspace is located in                           |
| `HACKSPACE_OPEN_ENTITY`     | `binary_sensor.hackspace_open_multi`                                                                    | Entity ID of the Home Assistant device to indicate open status |
| `HACKSPACE_PUBLIC_CALENDAR` | `calendar.public_events`                                                                                | The entity ID of the Home Assistant public calendar            |
| `HACKSPACE_MEMBER_CALENDAR` | `calendar.member_events`                                                                                | The entity ID of the Home Assistant member calendar            |
| `SENSORS_PRESSURE_ENABLED`  | `False`                                                                                                 | Enable pressure sensors                                        |

## Endpoints

Hackspace API responds to Swagger docs requests at `/docs`.

### `/health`

Simple health endpoint.

### `/space.json`

Outputs a standard [SpaceAPI](https://spaceapi.io) endpoint.

### `/events`

Dumps a JSON format list of events upcoming in the next 30 days.

### `/events.ics`

Dumps a iCal format list of events upcoming in the next 30 days.