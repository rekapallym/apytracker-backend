#!/bin/bash

echo "APYTracker - Deployment Setup Script"
echo "==================================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK (gcloud) is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Make sure we're logged in
echo "🔐 Checking Google Cloud authentication..."
ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null)

if [ -z "$ACCOUNT" ]; then
    echo "You need to log in to Google Cloud first."
    gcloud auth login
else
    echo "✅ Authenticated as: $ACCOUNT"
fi

# Get the project ID
echo "📁 Listing your GCP projects:"
gcloud projects list

echo ""
read -p "Enter your GCP project ID: " PROJECT_ID

# Set the project
gcloud config set project $PROJECT_ID

# Check if service account key exists
KEY_FILE="gcp-key.json"
if [ -f "$KEY_FILE" ]; then
    echo "⚠️ Warning: A service account key file already exists: $KEY_FILE"
    read -p "Do you want to create a new service account key? (y/n): " CREATE_NEW_KEY
    if [[ "$CREATE_NEW_KEY" != "y" ]]; then
        echo "Skipping service account key creation."
    else
        CREATE_KEY=true
    fi
else
    CREATE_KEY=true
fi

# Create a service account if needed
if [[ "$CREATE_KEY" == true ]]; then
    echo "🔑 Creating a new service account for deployment..."
    
    # Generate a random ID to avoid conflicts
    RANDOM_ID=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-z0-9' | fold -w 6 | head -n 1)
    SA_NAME="apytracker-sa-$RANDOM_ID"
    
    # Create service account
    gcloud iam service-accounts create $SA_NAME \
        --display-name="APYTracker Service Account"
    
    # Grant Firestore access
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
        --role="roles/datastore.user"
    
    # Create and download key
    gcloud iam service-accounts keys create $KEY_FILE \
        --iam-account="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
    
    echo "✅ Service account key created: $KEY_FILE"
    echo "⚠️ IMPORTANT: This file contains sensitive credentials."
    echo "   It has been added to .gitignore, but make sure it's never committed to git."
fi

# Create .env file for local development
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file for local development..."
    echo "GOOGLE_APPLICATION_CREDENTIALS=./$KEY_FILE" > .env
    echo "✅ Created .env file"
fi

echo ""
echo "🎉 Setup complete! You can now:"
echo "1. Commit your code to GitHub (credentials are in .gitignore)"
echo "2. Deploy to GCP Cloud Run with:"
echo "   gcloud run deploy apytracker-backend --source ."
echo ""
echo "For more detailed deployment instructions, see the README.md"