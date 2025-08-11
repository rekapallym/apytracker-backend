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

### Option 1: Manual Deployment

1. Build and push Docker image:
   ```sh
   # Build the Docker image
   docker build -t gcr.io/YOUR_PROJECT_ID/apytracker-backend .
   
   # Push to Google Container Registry
   docker push gcr.io/YOUR_PROJECT_ID/apytracker-backend
   ```

2. Deploy to Cloud Run:
   ```sh
   gcloud run deploy apytracker-backend \
     --image gcr.io/YOUR_PROJECT_ID/apytracker-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --memory 512Mi \
     --min-instances 0 \
     --max-instances 10
   ```

### Option 2: Continuous Deployment with GitHub and Cloud Build (Recommended)

1. Initialize a Git repository and push to GitHub:
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/apytracker-backend.git
   git push -u origin main
   ```

2. Set up Cloud Build trigger (detailed steps):
   
   a. Go to the Google Cloud Console: https://console.cloud.google.com/
   
   b. Navigate to Cloud Build > Triggers
   
   c. Click "Connect Repository" (if first time) or "Create Trigger" (if you already have repositories connected)
   
   d. Select GitHub as the source and authenticate if prompted
   
   e. Select your repository from the list
   
   f. Configure the trigger with these settings:
      - Name: "apytracker-backend-deploy"
      - Description: "Deploy APYTracker backend to Cloud Run"
      - Event: "Push to a branch"
      - Source: Your repository and branch (typically "main" or "master")
      - Configuration: "Cloud Build configuration file (yaml or json)"
      - Location: "Repository"
      - Cloud Build configuration file location: "/cloudbuild.yaml"
   
   g. Click "Create"

3. Ensure proper permissions (important!):
   
   a. Go to IAM & Admin > IAM in the Google Cloud Console
   
   b. Find the Cloud Build service account (it will look like: `[PROJECT-NUMBER]@cloudbuild.gserviceaccount.com`)
   
   c. Click the edit (pencil) icon and add these roles:
      - Cloud Run Admin
      - Service Account User
      - Cloud Build Service Account
   
   d. Save the changes

4. Trigger your first deployment:
   
   a. In the Cloud Build Triggers page, find your new trigger
   
   b. Click the "Run Trigger" button to start a manual build
   
   c. Monitor the build progress in the Cloud Build history page

5. Future deployments:
   
   After setup, whenever you push changes to your GitHub repository, Cloud Build will automatically detect the change and deploy the updated application to Cloud Run.

### Managing Credentials

For production deployment, use the Google Cloud Secret Manager:

```sh
# Create a secret with your service account key
gcloud secrets create apytracker-service-account \
  --data-file="path/to/your/gcp-key.json"

# Update your Cloud Run service to use this secret
gcloud run services update apytracker-backend \
  --update-secrets=GOOGLE_APPLICATION_CREDENTIALS=/secret/gcp-key.json:apytracker-service-account:latest
```

### Cost-Optimization

The deployment is configured for cost-optimization with:
- Scale to zero when not in use (min-instances=0)
- Limited memory allocation (512Mi)
- Maximum instance cap (max-instances=10)

This setup should cost only a few dollars per month for low to moderate traffic.
