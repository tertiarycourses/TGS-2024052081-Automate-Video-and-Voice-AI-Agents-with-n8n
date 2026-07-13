# Lab 0 - Set Up n8n on Your Local Computer

> Do this before Topic 1. Every other lab in the course assumes this stack is running.

This folder starts **n8n** and **Postgres** as two Docker containers. n8n stores your workflows and credentials in Postgres, so nothing is lost when you restart your machine.

## Before you start

| Tool | macOS | Windows (PowerShell) |
|---|---|---|
| Docker Desktop | `brew install --cask docker` | `winget install Docker.DockerDesktop` |
| Ollama | `brew install ollama` | `winget install Ollama.Ollama` |

Confirm both Docker commands work before going further:

```bash
docker --version
docker compose version
```

**Docker Desktop must actually be running** - not just installed. Launch it and wait for the whale icon to stop animating. On Windows, Docker Desktop needs **WSL 2**; if it refuses to start, run `wsl --install` in PowerShell **as Administrator**, reboot, then start Docker again.

## Start the stack

From the repository folder:

```bash
cd lab0
docker compose pull
docker compose up -d
```

What the two commands do:

- **`docker compose pull`** downloads the `n8nio/n8n` and `postgres:17` images. This is the slow step - a few hundred MB on first run. Running it separately means the download finishes before anything tries to start, so you get a clear progress bar instead of a silent wait.
- **`docker compose up -d`** starts both containers in the background (`-d` = detached). Your terminal returns immediately and the stack keeps running.

Confirm both containers are up:

```bash
docker compose ps
```

You want to see `lab0-n8n-1` and `lab0-postgres-1` both in state **running**.

## Pull the models

The labs use a chat model and an embedding model, both running locally through Ollama:

```bash
ollama pull gemma4
ollama pull nomic-embed-text
ollama list
```

`ollama list` must show both. The workflow files reference the exact tags **`gemma4:latest`** and **`nomic-embed-text:latest`** - if your tags differ, either pull the matching tag or update the model name in the node.

## Create your n8n account

Open **http://localhost:5678** and create the owner account. This is a local account on your own machine - the email and password are not sent anywhere, but write them down, because there is no password reset.

## Connect n8n to Ollama

In n8n, create an **Ollama** credential with this base URL:

```text
http://host.docker.internal:11434
```

**Do not use `http://localhost:11434`.** n8n runs inside a container, and inside that container `localhost` means *the container itself*, not your computer - so Ollama would not be found. `host.docker.internal` is how a container refers to its host machine. It works the same on macOS and Windows.

Click **Test** on the credential. It must succeed before you continue.

## Verify

- [ ] `docker compose ps` shows n8n and postgres both **running**.
- [ ] n8n opens at `http://localhost:5678` and you are logged in.
- [ ] `ollama list` shows `gemma4` and `nomic-embed-text`.
- [ ] The n8n Ollama credential test succeeds.

## Everyday commands

| Task | Command |
|---|---|
| Start the stack | `docker compose up -d` |
| Stop the stack (keeps all data) | `docker compose stop` |
| Restart after a reboot | `docker compose up -d` |
| Watch the n8n logs | `docker compose logs -f n8n` |
| Update n8n to the latest image | `docker compose pull` then `docker compose up -d` |
| Remove containers, **keep** workflows | `docker compose down` |
| Remove containers **and erase all workflows** | `docker compose down -v` |

The `-v` flag deletes the named volumes (`n8n_data`, `postgres_data`). That is where every workflow and credential you build in this course lives. Use it only when you intend to start over.

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop is not running. | Launch Docker Desktop, wait for it to settle, retry. |
| `port is already allocated` (5678) | An older n8n container is still up. | `docker ps` to find it, `docker stop <id>`. Or change the left-hand port in `docker-compose.yml` to `5679:5678`. |
| n8n cannot connect to Ollama | The credential uses `localhost` from inside Docker. | Use `http://host.docker.internal:11434`. |
| `ollama pull` fails - model not found | The tag does not exist for your Ollama version. | Run `ollama list`, pull a tag that exists, and set that exact name in the Ollama nodes. |
| n8n loads but immediately logs you out | Cookie issue over plain HTTP. | Already handled: the compose file sets `N8N_SECURE_COOKIE=false`. Confirm you are on `http://localhost:5678`, not `https://`. |
| Workflows vanished after a restart | The stack was brought down with `-v`. | Volumes were erased. Re-import the workflow JSON from the lab folders. |

## What is in the compose file

| Service | Image | Why it is here |
|---|---|---|
| `n8n` | `n8nio/n8n` | The automation platform. Published on port **5678**. |
| `postgres` | `postgres:17` | Durable storage for workflows, credentials and execution history. |

Both services use `restart: unless-stopped`, so the stack comes back automatically after a reboot once Docker Desktop starts.

The Postgres password in this file (`n8n_password`) is a throwaway for local classroom use. It is never exposed outside your machine - Postgres has no published port. Do not reuse this file as-is for anything internet-facing.
