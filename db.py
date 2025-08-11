from google.cloud import firestore
import os

# Initialize Firestore client
# Make sure GOOGLE_APPLICATION_CREDENTIALS is set to your service account key
client = firestore.Client()

# Collections in Firestore
PRODUCTS_COLLECTION = "products"
ALERTS_COLLECTION = "alerts"
EDUCATIONAL_COLLECTION = "educational"

# --- Products ---
def get_all_products(bank=None, min_apy=None, state=None, product_type=None, term=None, min_deposit=None):
    """
    Get all products, with optional filtering by various criteria.
    
    Parameters:
    - bank: Filter by bank name
    - min_apy: Filter by minimum APY percentage
    - state: Filter by state availability
    - product_type: Filter by product type (HYSA, CD)
    - term: Filter by term length in months (for CDs)
    - min_deposit: Filter by minimum deposit amount
    
    Note: When filtering by multiple fields, you'll need a composite index in Firestore.
    """
    query = client.collection(PRODUCTS_COLLECTION)
    
    # Apply filters using the modern .filter() method
    if bank:
        query = query.filter("bank", "==", bank)
    if min_apy is not None:
        query = query.filter("apy", ">=", float(min_apy))
    if state:
        query = query.filter("state", "==", state)
    if product_type:
        query = query.filter("product_type", "==", product_type)
    if term is not None:
        query = query.filter("term", "==", term)
    if min_deposit is not None:
        query = query.filter("min_deposit", "<=", float(min_deposit))
        
    try:
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        # Check if this is an index error
        if "The query requires an index" in str(e):
            index_url = str(e).split("You can create it here: ")[1] if "You can create it here:" in str(e) else ""
            raise ValueError(f"This query requires a Firestore composite index. Please create it at: {index_url}")
        else:
            raise e

# --- Add Product ---
def add_product(product: dict):
    client.collection(PRODUCTS_COLLECTION).add(product)

# --- Alerts ---
def save_alert(alert: dict):
    """Save a user alert for APY notifications"""
    client.collection(ALERTS_COLLECTION).add(alert)


# --- Educational Content ---
def get_educational_content(topic=None):
    """Get educational content, optionally filtered by topic"""
    query = client.collection(EDUCATIONAL_COLLECTION)
    if topic:
        query = query.filter("topic", "==", topic)
    try:
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        raise ValueError(f"Error fetching educational content: {str(e)}")


def add_educational_content(content: dict):
    """Add new educational content to the database"""
    return client.collection(EDUCATIONAL_COLLECTION).add(content)


# --- APY Calculator ---
def calculate_apy_earnings(principal, apy, term_years, compounding="daily"):
    """Calculate earnings based on APY, principal, term, and compounding frequency
    
    Args:
        principal (float): Initial deposit amount
        apy (float): Annual Percentage Yield as a percentage (e.g., 4.5 for 4.5%)
        term_years (float): Investment term in years (e.g., 0.5 for 6 months)
        compounding (str): Compounding frequency (daily, monthly, quarterly, annually)
        
    Returns:
        dict: Dictionary with calculation results
    """
    # Convert APY to decimal
    apy_decimal = apy / 100
    
    # Define compounding periods per year
    periods_map = {
        "daily": 365,
        "monthly": 12,
        "quarterly": 4,
        "annually": 1
    }
    periods = periods_map.get(compounding.lower(), 365)  # Default to daily
    
    # Calculate simple interest (no compounding)
    simple_interest = principal * apy_decimal * term_years
    simple_total = principal + simple_interest
    
    # Calculate compound interest
    compound_total = principal * (1 + (apy_decimal / periods)) ** (periods * term_years)
    compound_interest = compound_total - principal
    
    return {
        "principal": principal,
        "apy": apy,
        "term_years": term_years,
        "compounding": compounding,
        "simple_interest": round(simple_interest, 2),
        "simple_total": round(simple_total, 2),
        "compound_interest": round(compound_interest, 2),
        "compound_total": round(compound_total, 2),
        "difference": round(compound_interest - simple_interest, 2)
    }
