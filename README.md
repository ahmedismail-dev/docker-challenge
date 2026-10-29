# VisitorBeacon

A small visit counter I built for the CoderCo container challenge. Three containers work together: nginx takes the requests, several Flask containers handle them, and Redis keeps the count.

```
Browser -> nginx (port 5002) -> web (Flask, x3) -> Redis
```

## What it does

| Route | Result |
|-------|--------|
| `/` | Welcome message with the app name |
| `/count` | Adds one visit and shows which container answered |
| `/health` | Checks Redis and returns 200 if it's up, 503 if not |
| `/reset` | Sets the counter back to 0 |

The app name and Redis settings come from environment variables in `docker-compose.yml`, so nothing is hardcoded. Only nginx is exposed to my machine. Flask and Redis talk to each other on Docker's internal network using their service names, and a volume keeps the counter when containers restart.

**Stack:** Docker, Docker Compose, Python 3.8, Flask, Redis, nginx

## Run it

You need Docker Desktop and Git.

```bash
git clone https://github.com/ahmedismail-dev/docker-challenge.git
cd docker-challenge
docker compose up --build --scale web=3
```

Open http://localhost:5002/count and refresh a few times. The number goes up, and the container ID changes as nginx spreads the requests across the three Flask containers. Stop with `Ctrl+C`, then `docker compose down`.

<!-- Add a screenshot: ![VisitorBeacon /count page](docs/count.png) -->

## What went wrong along the way

Most of what I learned came from fixing errors:

- **`ssh: Could not resolve hostname`**: I ran the repo URL as an `ssh` command. A remote URL is only used with `git remote add` or `git clone`.
- **`services.web.build must be a string or object`**: I'd left `build:` empty. It needed `build: .`.
- **`enviroment false schema`**: a typo. Compose rejects keys it doesn't know.
- **`SyntaxError` and `exited with code 1`**: a typo in `count.py` crashed the container. Reading the traceback from the bottom led me to the line.
- **`exited with code 0`**: my `if __name__ == "__main__"` was indented inside a function, so Flask never started. Code 1 is a crash, code 0 means it finished normally.
- **`operation not permitted` on `nginx.conf`**: macOS blocked Docker from reading my Desktop folder. nginx didn't start, so the browser showed `ERR_CONNECTION_REFUSED`. Allowing Docker access fixed it.
- **Port clash**: `web` and `nginx` both published port 5002, and scaled containers can't share a host port. Now only nginx publishes one.

## Next steps

- Add healthchecks to the compose file
- Use gunicorn instead of the Flask dev server
- Install dependencies before copying the code in the Dockerfile, so rebuilds are faster
- Add a GitHub Actions workflow to build the image
- Deploy it on AWS
