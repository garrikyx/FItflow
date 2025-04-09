# FitFlow
A fitness platform designed to motivate you, enhancing your fitness journey.

### Prerequisites
1. Docker ([Windows](https://docs.docker.com/desktop/install/windows-install/) | [MacOS](https://docs.docker.com/desktop/install/mac-install/))
2. Node.js - [Download & Install Node.js](https://nodejs.org/en/download/) and the npm package manager.


### Set-up for backend using Docker Compose

navigate to this folder (`/backend`)

```bash
cd backend
```

### Provide secrets

We require several secrets across each of our services.
Make a copy of `.env.example`, rename it to `.env` and provide the information as stated using any text editor (`vi .env.example`).

1. `cp .env.example .env`
2. Add fields with the respective information (subdomain, email_address, API_key).

**Note: `.env` is automatically ignored by git**

```yaml
OPENWEATHER_API_KEY=your_api_key
GROQ_API_KEY=your_api_key
```

Deploying using Docker Compose relies on the `docker-compose.yml` file for the container specifications and runtime configurations. Environment variables in the `.env` created earlier will be loaded automatically (as long as the commands are run in the same folder as the `.env` file).

1. Run the following command to rebuild the Docker images:

   ```bash
   # windows
   docker compose build

   # macOS
   docker compose build
   ```

   or if you want to rebuild the images without using the cache.

   ```bash
   # windows
   docker-compose build --no-cache

   # macOS
   docker compose build --no-cache
   ```

   or if the containers are already running.

   ```bash
   # windows
   docker-compose up --build

   # macOS
   docker compose up --build
   ```

2. Run the following command to run the containers:

   ```bash
   # windows
   docker-compose up

   # macOS
   docker compose up
   ```


### Set-up for frontend

Assuming that you have cloned this repository and navigated to the root of the project, navigate to this folder (`/frontend`)

```bash
cd frontend
```


### Installing Dependencies

```sh
npm install
```


### Run Application in localhost

```sh
npm run dev
```