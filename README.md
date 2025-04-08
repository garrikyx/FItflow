# FitFlow
A fitness platform designed to motivate you, enhancing your fitness journey.

### Prerequisites
1. Docker ([Windows](https://docs.docker.com/desktop/install/windows-install/) | [MacOS](https://docs.docker.com/desktop/install/mac-install/))

### Set-up for frontend

Assuming that you have cloned this repository and navigated to the root of the project, navigate to this folder (`/frontend`)

```bash
cd frontend
```

### Provide secrets

We require several secrets across each of our services.
Make a copy of `.env.example`, rename it to `.env` and provide the information as stated using any text editor (`vi .env.example`).

1. `cp .env.example .env`
2. Add fields with the respective information (subdomain, email_address, API_key).

**Note: `.env` is automatically ignored by git**

```yaml
AUTH_TOKEN_SECRET=your_secret
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
GCP_PROJECT_ID=your_project_id
STRIPE_API_KEY=your_stripe_api_key
```

### Installing Dependencies

```sh
npm install
```


### Run Application in localhost

```sh
npm run dev
```

### Set-up for backend