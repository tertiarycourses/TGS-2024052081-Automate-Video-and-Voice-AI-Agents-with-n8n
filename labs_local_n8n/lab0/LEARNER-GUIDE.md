# Lab 0 - Learner Guide: Set Up n8n on Your Local Computer

> **Time:** 45-60 minutes
> **Goal:** A working local stack - Docker, n8n, Postgres and Ollama - that every later lab depends on.
> **Deliverable:** A screenshot of n8n running at `http://localhost:5678` with a passing Ollama credential test.

## Why this lab exists

Every workflow you build in this course runs on your own machine. Nothing is sent to a hosted n8n, and the language models run locally through Ollama. That means no API bill for the core labs, no data leaving your laptop, and full visibility into every execution.

The cost of that is a setup step. This lab is that step. Get it right once and the remaining labs are about building agents, not fighting the environment.

## The architecture you are about to build

```
Your computer (the host)
|
|-- Ollama            :11434    <- chat + embedding models, runs directly on the host
|
|-- Docker Desktop
      |
      |-- n8n container      :5678  <- the automation platform, you open this in the browser
      |     |
      |     +-- talks to Postgres over Docker's internal network
      |     +-- talks to Ollama via host.docker.internal:11434
      |
      |-- postgres container         <- stores workflows, credentials, execution history
            (no published port - only n8n can reach it)
```

Three things are worth noticing now, because they explain most of the errors later in this lab:

1. **n8n runs inside a container. Ollama does not.** Ollama runs directly on your computer. So n8n has to reach *out* of Docker to find it.
2. **Postgres has no published port.** It is reachable from the n8n container and nowhere else. That is deliberate.
3. **Your work lives in Docker volumes**, not in this folder. Deleting the volumes deletes your workflows.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Docker Desktop | Runs n8n and Postgres as a repeatable local stack. |
| Image vs container | The image is the downloaded template; the container is the running copy of it. |
| `docker compose pull` | Downloads the images ahead of time, so startup is not a silent wait. |
| `docker compose up -d` | Starts the containers in the background and returns your terminal. |
| Named volume | Where n8n keeps your workflows so a restart does not erase them. |
| `host.docker.internal` | How a container says "the computer I am running on". |

## Step 1 - Install the prerequisites

| Tool | macOS | Windows (PowerShell) |
|---|---|---|
| Docker Desktop | `brew install --cask docker` | `winget install Docker.DockerDesktop` |
| Ollama | `brew install ollama` | `winget install Ollama.Ollama` |

On Windows, **close and reopen PowerShell after installing.** A newly installed program is not on your PATH until you do. If a command comes back "not recognized", that is almost always the reason.

Then confirm:

```bash
docker --version
docker compose version
```

Both must print a version. If `docker` is not found, Docker Desktop is not installed or not on your PATH. If `docker compose` is not found but `docker` is, you have a very old Docker - update it, because the old `docker-compose` (with a hyphen) is not what this course uses.

**Docker Desktop must be launched, not merely installed.** Open the app and wait until the whale icon stops animating. The `docker` command talks to a background service that only exists while Docker Desktop is running - this is the single most common reason the next step fails.

## Step 2 - Pull the images

```bash
cd lab0
docker compose pull
```

This downloads two images described in `docker-compose.yml`:

- `n8nio/n8n` - the automation platform
- `postgres:17` - the database

Expect a few hundred megabytes on a first run, and a progress bar per layer. On a slow connection this is the longest part of the lab.

**You could skip this command** - `docker compose up` pulls anything missing anyway. It is worth running separately because it separates *downloading* from *starting*. If the download fails (flaky wifi, proxy, disk full), you see it here as a clean error, instead of a stack that appears to hang on startup for reasons you cannot see.

## Step 3 - Start the stack

```bash
docker compose up -d
```

The `-d` means **detached**: the containers run in the background and you get your prompt back. Without it, the logs stream into your terminal and closing that terminal stops the stack.

Check both containers came up:

```bash
docker compose ps
```

You are looking for `lab0-n8n-1` and `lab0-postgres-1`, both **running**. If n8n is in a restart loop, read its logs:

```bash
docker compose logs -f n8n
```

Press `Ctrl+C` to stop following the logs. This does **not** stop the container - it only stops printing.

## Step 4 - Pull the models

Ollama runs on the host, so this is a normal terminal command, nothing to do with Docker:

```bash
ollama pull gemma4
ollama pull nomic-embed-text
ollama list
```

Two models, two different jobs:

- **`gemma4`** is the *chat* model. It writes, reasons and decides which tool to call. This is the "brain" in every agent lab.
- **`nomic-embed-text`** is the *embedding* model. It turns text into vectors so the RAG labs can search by meaning rather than by keyword. It cannot chat, and the chat model cannot embed - you need both.

`ollama list` must show both before you continue. The lab workflows reference the exact tags **`gemma4:latest`** and **`nomic-embed-text:latest`**. If what `ollama list` prints does not match, use the name it prints and set that name in the Ollama nodes.

## Step 5 - Create your n8n owner account

Open **http://localhost:5678**.

On first run n8n asks you to create an owner account. This account is local to your machine. The email and password are stored in your own Postgres container and are not sent anywhere - but **write them down**, because there is no "forgot password" email on a local instance.

## Step 6 - Connect n8n to Ollama

In n8n go to **Credentials -> Add credential -> Ollama**, and set the base URL to:

```text
http://host.docker.internal:11434
```

Then press **Test**. It must say the connection succeeded.

### Why not `localhost`?

This is the one idea in this lab that is worth genuinely understanding, because it comes back in every Ollama-backed lab.

`localhost` always means *"the machine I am currently running on"*. n8n is running **inside a container**, which is its own little machine. So when the n8n container says `localhost:11434`, it is looking for Ollama *inside the container* - where nothing is listening. The request fails.

`host.docker.internal` is a name Docker Desktop provides that means *"the computer hosting me"* - your actual laptop, where Ollama really is listening on port 11434. It works identically on macOS and Windows.

> **Rule of thumb:** inside n8n, anything running on your host machine is reached at `host.docker.internal`, never `localhost`. Anything in *your browser* still uses `localhost`, because your browser is not in a container.

## Checkpoint

- [ ] `docker compose ps` shows **n8n** and **postgres** both running.
- [ ] n8n opens at `http://localhost:5678` and you are logged in as owner.
- [ ] `ollama list` shows `gemma4` and `nomic-embed-text`.
- [ ] The n8n Ollama credential test succeeds.
- [ ] You can explain, in your own words, why the Ollama credential must not use `localhost:11434`.

## Everyday commands

You will use these all week.

| Task | Command |
|---|---|
| Start the stack | `docker compose up -d` |
| Stop it, keeping all data | `docker compose stop` |
| Start again after a reboot | `docker compose up -d` |
| Follow the n8n logs | `docker compose logs -f n8n` |
| Update n8n to the newest image | `docker compose pull` then `docker compose up -d` |
| Remove the containers, **keep** workflows | `docker compose down` |
| Remove the containers **and erase everything** | `docker compose down -v` |

Note the difference between the last two. `docker compose down` removes the containers but leaves the named volumes, so your workflows survive and `up -d` brings them all back. `docker compose down -v` also deletes the volumes - `n8n_data` and `postgres_data` - which is every workflow, credential and execution you have built. There is no undo. Use `-v` only when you deliberately want a clean slate.

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop is installed but not running. | Launch it, wait for the whale to settle, retry. |
| `port is already allocated` on 5678 | An older n8n container is still running. | `docker ps`, then `docker stop <id>`. Or edit `docker-compose.yml` to publish `5679:5678`. |
| n8n container restarts in a loop | Postgres was not ready yet, or the volume is corrupt. | `docker compose logs n8n`. If it is a database error, `docker compose down -v` and start over - you lose local workflows. |
| Ollama credential test fails | The URL uses `localhost` from inside the container. | Use `http://host.docker.internal:11434`. |
| Ollama credential test fails *and* the URL is right | Ollama is not running on the host. | Run `ollama list` in a terminal. If that fails, start Ollama. |
| `ollama pull gemma4` - model not found | That tag does not exist for your Ollama version. | Pull a tag that does exist, then set that exact name in the Ollama nodes. |
| n8n logs you straight back out | HTTPS cookie enforcement over plain HTTP. | Already handled by `N8N_SECURE_COOKIE=false` in the compose file. Make sure you are on `http://`, not `https://`. |
| Everything disappeared after a restart | The stack was taken down with `-v`. | The volumes were erased. Re-import the workflow JSON from each lab folder. |

## Reflection questions

1. What is the difference between an image and a container, in your own words?
2. Why does n8n reach Ollama at `host.docker.internal` but your browser reaches n8n at `localhost`?
3. Where do your workflows actually live? What command would destroy them?
4. Why does this course use two different models rather than one?

## Lab deliverable

Submit:

- A screenshot of `docker compose ps` showing both containers running.
- A screenshot of the n8n Ollama credential test passing.
- A one-paragraph note describing the local architecture and why `localhost` fails from inside the container.
