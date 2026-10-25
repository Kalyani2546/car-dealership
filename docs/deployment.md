# IBM Cloud Code Engine deployment

This repository builds a single web image with the React production bundle and Django backend. Never check deployment credentials or secrets into the repository.

## Deploy on Render (assignment demo)

The root `render.yaml` is a Render Blueprint for the app. To deploy it:

1. Sign in to Render and connect the GitHub account that can access `Kalyani2546/car-dealership`.
2. In the Render dashboard, choose **New + → Blueprint**, select this repository and the `main` branch, then apply the `render.yaml` configuration.
3. Review the service settings, create the web service, and wait for its first deploy to finish.
4. Open the service's `onrender.com` URL and verify `/` and `/api/dealers/` load successfully. Record that exact public URL in the local `deploymentURL` file for the assignment.

The Blueprint creates a free demo service. Free services may sleep when idle, and the configured SQLite database is stored under `/tmp`, which is ephemeral and can reset on restart/redeploy. This is intended for short assignment evidence capture, not production data. Do not add real customer information.

The container binds to Render's assigned `PORT`; Django is configured with the Render host and HTTPS CSRF origins. Render generates `DJANGO_SECRET_KEY` as a service secret.

## IBM Cloud Code Engine

Alternatively, deploy on IBM Cloud Code Engine. This requires an activated IBM Cloud account/project and CLI login. Follow the remaining steps below.

## Prepare

1. Install and log in to the IBM Cloud CLI, including the Code Engine and Container Registry plugins.
2. Create or select a Code Engine project and a Container Registry namespace.
3. Choose a strong, persistent `DJANGO_SECRET_KEY` and a `DJANGO_ALLOWED_HOSTS` value containing the public application host.
4. Create a durable database/storage plan before accepting real user data. The bundled SQLite database is suitable for local learning/demo use, not multi-instance production; an ephemeral container filesystem may lose data on redeploy.

## Build and deploy

From the repository root, build and push the Docker image to your own registry:

```powershell
docker build -t us.icr.io/<namespace>/cars-dealership:latest .
ibmcloud cr login
docker push us.icr.io/<namespace>/cars-dealership:latest
```

Create a Code Engine application using your selected project/image and configure:

- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` as a Code Engine secret reference
- `DJANGO_ALLOWED_HOSTS` to the assigned application host
- `DJANGO_CSRF_TRUSTED_ORIGINS` to the matching `https://` application origin

Example CLI outline (fill in the actual project, namespace, image, and secret values):

```powershell
ibmcloud ce project select -n <your-project>
ibmcloud ce app create --name cars-dealership --image us.icr.io/<namespace>/cars-dealership:latest --port 8000 --env DJANGO_DEBUG=0 --env DJANGO_ALLOWED_HOSTS=<your-app-host> --env DJANGO_CSRF_TRUSTED_ORIGINS=https://<your-app-host>
```

Set the secret through the Code Engine console or its secret-reference options in the CLI rather than passing a secret value directly on the command line. After deployment, open the assigned URL, verify the landing page and API, and save that actual URL in `deploymentURL`. A managed persistent database, HTTPS-origin CSRF setting, and production secrets are required for a production deployment.
