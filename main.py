from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import db

# Load environment variables from .env file if it exists
load_dotenv()

app = FastAPI(
    title="APYTracker API",
    description="API for tracking and comparing APY rates from different financial institutions",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Exception Handler ---

@app.exception_handler(ValueError)
async def value_error_handler(_, exc):  # Using _ for unused parameter
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


# --- Pydantic Models ---
class AlertCreate(BaseModel):
    email: str
    criteria: dict = Field(..., description="Alert criteria like min_apy, state, etc.")


class ProductCreate(BaseModel):
    bank: str
    name: str
    apy: float
    product_type: str = Field(..., description="Type of product (e.g., HYSA, CD)")
    min_deposit: Optional[float] = Field(0, description="Minimum deposit amount required")
    term: Optional[int] = Field(None, description="Term length in months (primarily for CDs)")
    state: Optional[str] = Field(None, description="State availability (e.g., CA, NY, or null for nationwide)")
    details_url: Optional[str] = Field(None, description="URL to the product details page")
    features: Optional[List[str]] = Field(None, description="List of product features or benefits")


class EducationalContentCreate(BaseModel):
    title: str
    content: str
    topic: str
    summary: Optional[str] = None


class CalculatorRequest(BaseModel):
    principal: float = Field(..., description="Initial deposit amount")
    apy: float = Field(..., description="Annual Percentage Yield (%)")
    term_years: float = Field(..., description="Investment term in years")
    compounding: str = Field("daily", description="Compounding frequency (daily, monthly, quarterly, annually)")

@app.get("/")
def root():
    return {"message": "APYTracker API is running"}

@app.get("/products")
def get_products(
    bank: str = None, 
    min_apy: float = None, 
    state: str = None, 
    product_type: str = None,
    term: int = None,
    min_deposit: float = None,
    sort_by: str = None,
    sort_order: str = "desc"
):
    """
    List all APY products, with optional filtering and sorting.
    
    Parameters:
    - bank: Filter by bank name (e.g., Chase, Bank of America)
    - min_apy: Filter by minimum APY percentage (e.g., 4.5 for 4.5%)
    - state: Filter by state availability (e.g., CA, NY)
    - product_type: Filter by product type (e.g., HYSA, CD)
    - term: Filter by term length in months (for CDs)
    - min_deposit: Filter by minimum deposit amount
    - sort_by: Field to sort by (e.g., apy, term, min_deposit)
    - sort_order: Sort direction (asc or desc)
    
    Example: /products?bank=Chase&min_apy=4.5&state=CA&product_type=HYSA&sort_by=apy&sort_order=desc
    
    Note: When using multiple filters, a Firestore composite index is required.
    For best results without indexes, use only one filter parameter at a time.
    """
    try:
        products = db.get_all_products(
            bank=bank, 
            min_apy=min_apy, 
            state=state, 
            product_type=product_type,
            term=term,
            min_deposit=min_deposit
        )
        
        # Apply sorting if requested
        if sort_by and products:
            reverse = sort_order.lower() == "desc"
            try:
                products = sorted(products, key=lambda x: x.get(sort_by, 0), reverse=reverse)
            except Exception as e:
                # If sorting fails, return unsorted results
                pass
                
        return products
    except ValueError as e:
        # Check if this is an index error
        if "composite index" in str(e):
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        else:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/products", status_code=201)
def add_product(product: ProductCreate):
    """Add a new APY product (for admin/testing)"""
    # Convert Pydantic model to dict
    product_dict = product.model_dump()
    db.add_product(product_dict)
    return {"message": "Product added"}

@app.post("/alerts", status_code=201)
def create_alert(alert: AlertCreate):
    """Save a user alert (email + criteria)"""
    # Convert Pydantic model to dict
    alert_dict = alert.model_dump()
    db.save_alert(alert_dict)
    return {"message": "Alert saved"}

@app.post("/chat")
def chat(query: dict):
    """Send a user question to the AI assistant (stub for now)"""
    # This is a placeholder; you can later call OpenAI here
    user_question = query.get("question", "")
    return {"answer": f"You asked: {user_question} (AI response coming soon)"}


# --- Educational Content Endpoints ---
@app.get("/educational")
def get_educational_content(topic: Optional[str] = None):
    """Get educational content, optionally filtered by topic"""
    return db.get_educational_content(topic)


@app.post("/educational", status_code=201)
def add_educational_content(content: EducationalContentCreate):
    """Add new educational content (for admin use)"""
    content_dict = content.model_dump()
    db.add_educational_content(content_dict)
    return {"message": "Educational content added"}


# --- APY Calculator Endpoint ---
@app.post("/calculator")
def calculate_apy(calc_request: CalculatorRequest):
    """Calculate earnings with and without compound interest"""
    result = db.calculate_apy_earnings(
        principal=calc_request.principal,
        apy=calc_request.apy,
        term_years=calc_request.term_years,
        compounding=calc_request.compounding
    )
    return result
