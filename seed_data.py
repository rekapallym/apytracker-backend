"""
Seed script to populate the database with initial data.
Run this with: python seed_data.py
"""
import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def seed_products():
    """Add sample APY products to the database"""
    products = [
        {
            "bank": "Chase",
            "name": "Premier Savings",
            "apy": 4.5,
            "product_type": "HYSA",
            "min_deposit": 0,
            "term": None,
            "state": "CA",
            "details_url": "https://www.chase.com/personal/savings/savings-account/interest-rates",
            "features": ["No monthly fee", "Mobile banking", "FDIC insured"]
        },
        {
            "bank": "Bank of America",
            "name": "Advantage Savings",
            "apy": 4.2,
            "product_type": "HYSA",
            "min_deposit": 100,
            "term": None,
            "state": "NY",
            "details_url": "https://www.bankofamerica.com/deposits/savings/savings-accounts/",
            "features": ["Preferred Rewards", "Overdraft protection", "FDIC insured"]
        },
        {
            "bank": "Capital One",
            "name": "12-Month CD",
            "apy": 5.0,
            "product_type": "CD",
            "min_deposit": 1000,
            "term": 12,
            "state": "TX",
            "details_url": "https://www.capitalone.com/bank/cds/online-cds/",
            "features": ["Fixed rate", "No monthly fees", "FDIC insured"]
        },
        {
            "bank": "Ally",
            "name": "Online Savings",
            "apy": 4.75,
            "product_type": "HYSA",
            "min_deposit": 0,
            "term": None,
            "state": None,  # Available nationwide
            "details_url": "https://www.ally.com/bank/online-savings-account/",
            "features": ["No minimum deposit", "No monthly fees", "24/7 customer service"]
        },
        {
            "bank": "Marcus",
            "name": "High-Yield Savings",
            "apy": 4.6,
            "product_type": "HYSA",
            "min_deposit": 0,
            "term": None,
            "state": None,  # Available nationwide
            "details_url": "https://www.marcus.com/us/en/savings/high-yield-savings",
            "features": ["No fees", "Same-day transfers", "FDIC insured"]
        },
        {
            "bank": "Synchrony",
            "name": "High-Yield Savings",
            "apy": 4.75,
            "product_type": "HYSA",
            "min_deposit": 0,
            "term": None,
            "state": None,  # Available nationwide
            "details_url": "https://www.synchronybank.com/banking/high-yield-savings/",
            "features": ["No minimum balance", "ATM card available", "Mobile banking"]
        },
        {
            "bank": "Discover",
            "name": "36-Month CD",
            "apy": 4.5,
            "product_type": "CD",
            "min_deposit": 2500,
            "term": 36,
            "state": None,  # Available nationwide
            "details_url": "https://www.discover.com/online-banking/cd/",
            "features": ["Fixed rate", "Guaranteed returns", "FDIC insured"]
        }
    ]
    
    for product in products:
        try:
            db.add_product(product)
            print(f"Added product: {product['bank']} - {product['name']}")
        except Exception as e:
            print(f"Error adding product {product['name']}: {e}")

def seed_educational_content():
    """Add sample educational content to the database"""
    content = [
        {
            "title": "What is APY?",
            "content": """Annual Percentage Yield (APY) is the real rate of return earned on a savings deposit or investment taking into account the effect of compounding interest.
            
Unlike simple interest, APY takes into account the frequency at which interest is applied to the principal—be it annually, monthly, or daily—giving you a more accurate picture of what you'll earn over time.""",
            "topic": "basics",
            "summary": "Understanding Annual Percentage Yield and how it works"
        },
        {
            "title": "Simple vs Compound Interest",
            "content": """Simple interest is calculated only on the initial principal, while compound interest is calculated on the initial principal and on the accumulated interest over previous periods.

For example, if you invest $1,000 at 5% simple interest for 3 years, you'll earn $50 per year, for a total of $150 interest. 

With compound interest, you might earn $50 the first year, $52.50 the second year (5% of $1,050), and $55.13 the third year (5% of $1,102.50), for a total of $157.63.""",
            "topic": "basics",
            "summary": "The difference between simple and compound interest calculations"
        },
        {
            "title": "CD vs HYSA: Which is Right for You?",
            "content": """Certificates of Deposit (CDs) and High-Yield Savings Accounts (HYSAs) serve different purposes:

CDs:
- Typically offer higher APY
- Lock your money for a fixed term (3 months to 5+ years)
- May have penalties for early withdrawal
- Best for money you won't need access to

HYSAs:
- Slightly lower APY than CDs
- Complete liquidity - access your money anytime
- No term commitments
- Best for emergency funds or saving for near-term goals

Your choice depends on your timeline and liquidity needs.""",
            "topic": "comparisons",
            "summary": "Comparing Certificate of Deposits and High-Yield Savings Accounts"
        }
    ]
    
    for item in content:
        try:
            db.add_educational_content(item)
            print(f"Added educational content: {item['title']}")
        except Exception as e:
            print(f"Error adding content {item['title']}: {e}")

if __name__ == "__main__":
    print("Seeding database with initial data...")
    seed_products()
    seed_educational_content()
    print("Database seeding complete!")