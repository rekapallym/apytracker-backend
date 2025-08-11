#!/bin/bash

echo "Starting direct deployment to Cloud Run..."

# Deploy directly from source code
gcloud run deploy apytracker-backend \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --memory=512Mi \
  --min-instances=0 \
  --max-instances=10 \
  --service-account=svc-apytracker@apytracker-backend.iam.gserviceaccount.com

echo "Deployment completed!"