"""
Generate a mock bank statement PDF for portfolio showcase.
This creates a realistic-looking bank statement with fictional transactions.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime, timedelta
import random

# Output file
OUTPUT_FILE = "bank_statement_december_2024.pdf"

# Mock bank details
BANK_NAME = "Global Commerce Bank"
BANK_ADDRESS = "123 Financial District, Zurich, Switzerland"
ACCOUNT_NUMBER = "CH93 0076 2011 6238 5295 7"
ACCOUNT_HOLDER = "TechFlow Industries GmbH"
ACCOUNT_HOLDER_ADDRESS = "456 Innovation Park, Basel, Switzerland"
CURRENCY = "CHF"

# Generate mock transactions
def generate_transactions():
    """Generate a list of mock transactions for December 2024."""

    # Transaction templates with descriptions and typical amounts
    incoming_templates = [
        ("Payment received - INV-2024-{}", 5000, 50000),
        ("Customer payment - Order #{}", 1000, 15000),
        ("Intercompany transfer from TechFlow UK", 10000, 100000),
        ("Intercompany transfer from TechFlow DE", 15000, 80000),
        ("Refund - Vendor credit note", 500, 3000),
        ("Interest income", 50, 500),
        ("FX Gain adjustment", 100, 2000),
    ]

    outgoing_templates = [
        ("Supplier payment - {} Ltd", -2000, -30000),
        ("Payroll transfer - December", -50000, -150000),
        ("Bank charges - Monthly fee", -25, -100),
        ("SWIFT transfer fee", -15, -50),
        ("Intercompany payment to TechFlow US", -20000, -80000),
        ("Rent payment - Q4", -5000, -15000),
        ("Insurance premium", -1000, -5000),
        ("Utility payment", -500, -2000),
        ("Tax payment - VAT", -10000, -50000),
        ("Professional services - Audit fee", -3000, -15000),
    ]

    transactions = []
    start_date = datetime(2024, 12, 1)

    # Opening balance
    opening_balance = 245678.50
    running_balance = opening_balance

    # Generate ~40 transactions spread across December
    for day in range(1, 32):
        if day > 31:
            break

        current_date = start_date + timedelta(days=day-1)

        # Skip weekends for most transactions
        if current_date.weekday() >= 5 and random.random() > 0.2:
            continue

        # 1-3 transactions per day
        num_transactions = random.randint(0, 3)

        for _ in range(num_transactions):
            # 60% incoming, 40% outgoing
            if random.random() < 0.4:
                template, min_amt, max_amt = random.choice(incoming_templates)
                amount = round(random.uniform(min_amt, max_amt), 2)
                if "{}" in template:
                    description = template.format(random.randint(1000, 9999))
                else:
                    description = template
            else:
                template, min_amt, max_amt = random.choice(outgoing_templates)
                amount = round(random.uniform(min_amt, max_amt), 2)
                if "{}" in template:
                    companies = ["Nordic Supply", "Alpine Tech", "Central Euro", "Pacific Trade", "Atlantic Corp"]
                    description = template.format(random.choice(companies))
                else:
                    description = template

            running_balance += amount

            transactions.append({
                "date": current_date.strftime("%d.%m.%Y"),
                "description": description,
                "amount": amount,
                "balance": round(running_balance, 2)
            })

    return transactions, opening_balance

def create_pdf():
    """Create the bank statement PDF."""

    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT
    )

    elements = []

    # Bank header
    elements.append(Paragraph(BANK_NAME, title_style))
    elements.append(Paragraph(BANK_ADDRESS, ParagraphStyle('addr', alignment=TA_CENTER, fontSize=9)))
    elements.append(Spacer(1, 10*mm))

    # Statement title
    elements.append(Paragraph("<b>Account Statement - December 2024</b>",
                             ParagraphStyle('stitle', fontSize=14, alignment=TA_CENTER)))
    elements.append(Spacer(1, 8*mm))

    # Account details
    account_info = [
        ["Account Holder:", ACCOUNT_HOLDER],
        ["Address:", ACCOUNT_HOLDER_ADDRESS],
        ["Account Number:", ACCOUNT_NUMBER],
        ["Currency:", CURRENCY],
        ["Statement Period:", "01.12.2024 - 31.12.2024"],
    ]

    account_table = Table(account_info, colWidths=[45*mm, 120*mm])
    account_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(account_table)
    elements.append(Spacer(1, 8*mm))

    # Generate transactions
    transactions, opening_balance = generate_transactions()

    # Opening balance row
    elements.append(Paragraph(f"<b>Opening Balance: {CURRENCY} {opening_balance:,.2f}</b>", header_style))
    elements.append(Spacer(1, 3*mm))

    # Transaction table
    table_data = [["Date", "Description", "Amount", "Balance"]]

    for txn in transactions:
        amount_str = f"{txn['amount']:+,.2f}"
        balance_str = f"{txn['balance']:,.2f}"
        table_data.append([
            txn['date'],
            txn['description'][:45],  # Truncate long descriptions
            amount_str,
            balance_str
        ])

    # Add closing balance row
    if transactions:
        closing_balance = transactions[-1]['balance']
    else:
        closing_balance = opening_balance

    table_data.append(["", "", "", ""])
    table_data.append(["", "Closing Balance", "", f"{closing_balance:,.2f}"])

    trans_table = Table(table_data, colWidths=[22*mm, 85*mm, 30*mm, 35*mm])
    trans_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        # Body
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (2, 1), (3, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),

        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -3), [colors.white, colors.HexColor('#f8f9fa')]),

        # Grid
        ('GRID', (0, 0), (-1, -3), 0.5, colors.HexColor('#dee2e6')),

        # Closing balance row
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),

        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    elements.append(trans_table)
    elements.append(Spacer(1, 10*mm))

    # Footer
    footer_text = """
    <i>This statement is generated automatically. Please review all transactions and report any
    discrepancies within 30 days. For questions, contact customer service at +41 44 123 4567.</i>
    """
    elements.append(Paragraph(footer_text, ParagraphStyle('footer', fontSize=8, alignment=TA_CENTER)))

    # Build PDF
    doc.build(elements)
    print(f"PDF generated: {OUTPUT_FILE}")
    print(f"Total transactions: {len(transactions)}")
    print(f"Opening balance: {CURRENCY} {opening_balance:,.2f}")
    print(f"Closing balance: {CURRENCY} {closing_balance:,.2f}")

if __name__ == "__main__":
    create_pdf()
