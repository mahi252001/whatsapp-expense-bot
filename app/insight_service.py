from sqlalchemy import text


def get_spending_stats(db, user_number):

    total_query = text("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_number = :user
    """)

    total = db.execute(total_query, {"user": user_number}).scalar() or 0


    category_query = text("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_number = :user
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """)

    category_row = db.execute(category_query, {"user": user_number}).fetchone()

    top_category = category_row[0] if category_row else "None"
    category_amount = category_row[1] if category_row else 0


    merchant_query = text("""
        SELECT description, COUNT(*) as cnt
        FROM expenses
        WHERE user_number = :user
        GROUP BY description
        ORDER BY cnt DESC
        LIMIT 1
    """)

    merchant_row = db.execute(merchant_query, {"user": user_number}).fetchone()

    top_merchant = merchant_row[0] if merchant_row else "None"


    avg_query = text("""
        SELECT SUM(amount) / COUNT(DISTINCT DATE(created_at))
        FROM expenses
        WHERE user_number = :user
    """)

    avg_daily = db.execute(avg_query, {"user": user_number}).scalar() or 0


    return {
        "total": total,
        "top_category": top_category,
        "category_amount": category_amount,
        "top_merchant": top_merchant,
        "avg_daily": avg_daily
    }


def generate_insight(stats):

    insight = f"""
💡 Spending Insight

• You spend most on {stats['top_category']} (₹{int(stats['category_amount'])})
• Your most frequent merchant is {stats['top_merchant']}
• Your average daily spend is ₹{int(stats['avg_daily'])}
"""

    return insight.strip()