# APYTracker API Examples

This document provides examples of how to use the APYTracker API endpoints, including examples that don't require Firestore composite indexes.

## Setting Up Firestore Indexes

When filtering products by multiple criteria (e.g., bank + state + product_type), Firestore requires a composite index. If you encounter an error like this:

```
The query requires an index. You can create it here: [URL]
```

Follow these steps:

1. Click the URL in the error message to open the Firebase console
2. The index creation screen will be pre-filled with the required fields
3. Click "Create index" to create the composite index
4. Wait for the index to finish building (this may take a few minutes)

## Product API Examples

### Simple Queries (No Composite Index Required)

These queries work without setting up any special indexes:

#### Get All Products
```
GET /products
```

#### Filter by a Single Field
```
GET /products?bank=Chase
```

```
GET /products?min_apy=4.5
```

```
GET /products?state=CA
```

```
GET /products?product_type=HYSA
```

```
GET /products?term=12
```

```
GET /products?min_deposit=1000
```

#### Sorting Results
```
GET /products?sort_by=apy&sort_order=desc
```

```
GET /products?sort_by=min_deposit&sort_order=asc
```

### Advanced Queries (Composite Index Required)

These queries require composite indexes to be set up first:

#### Filter by Two Fields
```
GET /products?bank=Chase&product_type=HYSA
```

#### Filter by Three Fields
```
GET /products?bank=Chase&state=CA&product_type=HYSA
```

#### Filter by Multiple Fields with Sorting
```
GET /products?min_apy=4.5&product_type=HYSA&sort_by=apy&sort_order=desc
```

```
GET /products?product_type=CD&term=12&sort_by=apy&sort_order=desc
```

#### Filter by All Fields
```
GET /products?bank=Chase&min_apy=4.5&state=CA&product_type=HYSA&min_deposit=0&term=12
```

## Adding a New Product

```
POST /products
Content-Type: application/json

{
  "bank": "Discover",
  "name": "Online Savings",
  "apy": 4.3,
  "product_type": "HYSA",
  "min_deposit": 0,
  "term": null,
  "state": "NY",
  "details_url": "https://www.discover.com/online-banking/savings-account/",
  "features": ["No monthly fees", "No minimum balance", "FDIC insured"]
}
```

## Alerts API Example

```
POST /alerts
Content-Type: application/json

{
  "email": "user@example.com",
  "criteria": {
    "min_apy": 5.0,
    "state": "WA",
    "product_type": "CD"
  }
}
```

## Educational Content API Examples

```
GET /educational
```

```
GET /educational?topic=basics
```

## APY Calculator API Example

```
POST /calculator
Content-Type: application/json

{
  "principal": 10000,
  "apy": 4.5,
  "term_years": 1,
  "compounding": "daily"
}
```

Example response:
```json
{
  "principal": 10000,
  "apy": 4.5,
  "term_years": 1,
  "compounding": "daily",
  "simple_interest": 450.0,
  "simple_total": 10450.0,
  "compound_interest": 460.1,
  "compound_total": 10460.1,
  "difference": 10.1
}
```

## AI Chat API Example

```
POST /chat
Content-Type: application/json

{
  "question": "Which savings account type is best for emergency funds?"
}
```

## Testing with curl

Here are some curl commands you can use to test the API:

```bash
# Get all products
curl http://localhost:8000/products

# Filter products by bank
curl http://localhost:8000/products?bank=Chase

# Filter products by minimum APY and sort by APY descending
curl http://localhost:8000/products?min_apy=4.5&sort_by=apy&sort_order=desc

# Filter by product type and term
curl http://localhost:8000/products?product_type=CD&term=12

# Add a new product
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"bank":"Discover","name":"Online Savings","apy":4.3,"product_type":"HYSA","min_deposit":0,"term":null,"state":"NY","details_url":"https://www.discover.com/online-banking/savings-account/","features":["No monthly fees","No minimum balance","FDIC insured"]}'

# Get all products with filtering and sorting
curl "http://localhost:8000/products?min_apy=4.5&product_type=HYSA&sort_by=apy&sort_order=desc"

# Calculate APY earnings
curl -X POST http://localhost:8000/calculator \
  -H "Content-Type: application/json" \
  -d '{"principal":10000,"apy":4.5,"term_years":1,"compounding":"daily"}'
```