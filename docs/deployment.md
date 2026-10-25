# IBM Cloud Code Engine deployment

This repository builds a single web image with the React production bundle and Django backend. You must supply your own IBM Cloud account/project and credentials. Never check secrets into the repository.

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
