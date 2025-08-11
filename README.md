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
# apytracker-backend
