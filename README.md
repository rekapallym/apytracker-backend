# APYTracker Backend (FastAPI)

This is the backend API for APYTracker, built with FastAPI and Google Firestore.

## Features
- Products API (list/filter APY products)
- Alerts API (save user alert preferences)
- Educational Content API (for APY guides and explanations)
- APY Calculator API (compare simple vs compound interest)
- AI Chat API (OpenAI integration)

## Quickstart

1. Create a Python virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up your Google Cloud credentials for Firestore:
   - Download your service account key from GCP and set the environment variable:
     ```sh
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
     ```
4. Run the server:
   ```sh
   uvicorn main:app --reload
   ```

## Endpoints
- `GET /products` — List/filter APY products
- `POST /products` — Add a new APY product
- `POST /alerts` — Save user alert preferences
- `GET /educational` — Get educational content (optional topic filter)
- `POST /educational` — Add educational content
- `POST /calculator` — Calculate earnings with and without compound interest
- `POST /chat` — AI chat assistant

All API endpoints are documented at http://localhost:8000/docs or http://localhost:8001/docs

---

Edit `main.py` and `db.py` to customize your logic.

## Example Requests

### Add a new product
```json
POST /products

{
  "bank": "Chase",
  "name": "Premier Savings",
  "apy": 4.5,
  "product_type": "HYSA",
  "min_deposit": 0,
  "term": null,
  "state": "CA"
}
```

### Create an alert
```json
POST /alerts

{
  "email": "user@example.com",
  "criteria": {
    "min_apy": 5.0,
    "state": "WA",
    "product_type": "CD"
  }
}
```

### Use the APY calculator
```json
POST /calculator

{
  "principal": 10000,
  "apy": 4.5,
  "term_years": 1,
  "compounding": "daily"
}
```
## Deployment to Google Cloud Platform

### Direct Source Deployment (Recommended)

1. Make sure your service account has the necessary permissions:
   ```sh
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member='serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL' \
     --role='roles/run.admin'

   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member='serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL' \
     --role='roles/iam.serviceAccountUser'
   ```

2. Deploy directly from source code:
   ```sh
   bash deploy_direct.sh
   ```

   This will:
   - Upload your source code to Cloud Run
   - Build the container automatically
   - Deploy and make it publicly accessible
   - Configure scaling parameters

3. Access your API:
   - Find the deployed URL in the terminal output or in the GCP Console
   - API documentation is available at YOUR_URL/docs

### Managing Your Deployment

#### Viewing Logs
1. In GCP Console:
   - Go to Cloud Run > apytracker-backend > Logs

2. Via command line:
   ```sh
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=apytracker-backend" --limit 50
   ```

#### Updating Your Deployment
Make changes to your code, then run:
```sh
bash deploy_direct.sh
```

#### Monitoring Performance
In GCP Console:
- Go to Cloud Run > apytracker-backend > Metrics
- Monitor request count, latency, and resource usage

### Cost-Optimization

The deployment is configured for cost-optimization with:
- Scale to zero when not in use (min-instances=0)
- Limited memory allocation (512Mi)
- Maximum instance cap (max-instances=10)

This setup should cost only a few dollars per month for low to moderate traffic.

### Common Issues and Solutions

1. **Permission denied when deploying**
   - Problem: Service account lacks necessary permissions
   - Solution: Grant Cloud Run Admin and Service Account User roles

2. **Unable to access Firestore from Cloud Run**
   - Problem: Cloud Run service lacks Firestore permissions
   - Solution: Grant the Firestore User role to the service account

3. **Environment variables not available in Cloud Run**
   - Problem: Environment variables need to be set in Cloud Run configuration
   - Solution: Add environment variables in the deployment command with --set-env-vars

### Viewing Your Deployed Application

After successful deployment:

1. Go to Cloud Run in the Google Cloud Console
2. Click on your service name ("apytracker-backend")
3. You'll find the URL to your deployed application on the service details page
4. Your API will be accessible at this URL (e.g., https://apytracker-backend-abc123.run.app/)
5. Verify it's working by accessing the root endpoint or the documentation at `/docs`