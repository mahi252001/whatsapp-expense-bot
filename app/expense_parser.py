# app/expense_parser.py

def parse_expense(message: str):
    parts = message.strip().split()

    if len(parts) < 2:
        return None

    try:
        amount = float(parts[-1])
    except ValueError:
        return None

    description = " ".join(parts[:-1]).strip()

    if not description:
        return None

    return {
        "description": description,
        "amount": amount
    }