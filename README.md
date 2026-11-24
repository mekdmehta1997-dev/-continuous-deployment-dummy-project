# Dummy Loan API — CI/CD Practice

A toy FastAPI service for learning GitHub Actions, Docker, and Kubernetes. The risk logic is illustrative only; it is not a real credit model.

## 1. Run locally (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
ruff check .
python -m pytest -v
uvicorn app:app --reload --port 8000
```

Open http://localhost:8000/docs. Test health with `Invoke-RestMethod http://localhost:8000/health`.

## 2. Build and run Docker

```powershell
docker build -t dummy-loan-api:local .
docker run --rm -p 8000:8000 dummy-loan-api:local
```

In another terminal: `Invoke-RestMethod http://localhost:8000/health`.

## 3. Prepare local Kubernetes

Check the cluster context before applying anything:

```powershell
kubectl config current-context
kubectl get nodes
```

Apply the placeholder Deployment and Service:

```powershell
kubectl apply -f k8s/
kubectl get deployments,pods,services
```

The initial BusyBox containers are placeholders. The deployment workflow replaces them with the real API image.

## 4. Configure Docker Hub

Create a Docker Hub repository named `dummy-loan-api` and create a Docker Hub access token.

In GitHub repository Settings > Secrets and variables > Actions, add:
- `DOCKERHUB_USERNAME`: your Docker Hub username
- `DOCKERHUB_TOKEN`: your Docker Hub access token

Never commit credentials.

## 5. Configure a self-hosted runner for local Kubernetes

A GitHub-hosted runner cannot access a Kubernetes cluster running only on your PC. This example deploys using a Windows self-hosted GitHub Actions runner on the same PC as your Kind/Minikube cluster.

In GitHub repository Settings > Actions > Runners:
1. Select New self-hosted runner.
2. Select Windows x64.
3. Follow GitHub's displayed download and configuration commands on your PC.
4. Keep the runner online when deployment runs.
5. Ensure the runner account can use `kubectl` and access the intended cluster.

Only use this runner with repositories and workflows you trust. Do not run untrusted pull-request code on it.

## 6. Push to GitHub

```powershell
git add .
git commit -m "Add dummy API CI-CD project"
git push -u origin main
```

On pushes to `main`, the workflow runs Ruff and pytest, builds and pushes an image tagged `latest` and with the commit SHA, then updates Kubernetes through the self-hosted runner.

## 7. Verify and test the service

```powershell
kubectl get pods -l app=dummy-loan-api
kubectl rollout status deployment/dummy-loan-api
kubectl port-forward service/dummy-loan-api 8000:8000
```

In another terminal, test `http://localhost:8000/health` and `http://localhost:8000/docs`.

## 8. Roll back

```powershell
kubectl rollout history deployment/dummy-loan-api
kubectl rollout undo deployment/dummy-loan-api
kubectl rollout status deployment/dummy-loan-api
```

## Notes

- The initial BusyBox Deployment is only a placeholder so `kubectl set image` has a Deployment to update.
- The deployment job expects the Kubernetes cluster to be available to the Windows self-hosted runner.
- For production, use protected environments, hardened ephemeral runners, image scanning, least-privilege credentials, and managed Kubernetes.
