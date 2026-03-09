# # app/ai_service.py

# import os
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# SYSTEM_PROMPT = """
# You are an expense categorization assistant.
# Given an expense description, return only ONE category from:
# Food, Transport, Shopping, Bills, Entertainment, Health, Other
# Return only the category name.
# """


# def categorize_expense(description: str) -> str:
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": description}
#         ],
#         temperature=0
#     )

#     return response.choices[0].message.content.strip()


# def generate_insight(stats: dict) -> str:

#     prompt = f"""
# You are a personal finance assistant.

# User spending stats:

# Total spend: ₹{int(stats['total'])}
# Top category: {stats['top_category']} (₹{int(stats['category_amount'])})
# Most frequent merchant: {stats['top_merchant']}
# Average daily spend: ₹{int(stats['avg_daily'])}

# Write 3 short insights about the user's spending.
# Use bullet points.
# Keep it friendly and concise.
# """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a helpful financial assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.4
#     )

#     return response.choices[0].message.content.strip()



# FOR TEMP TEST
# app/ai_service.py

SYSTEM_PROMPT = """
You are an expense categorization assistant.
Categories:
Food, Transport, Shopping, Bills, Entertainment, Health, Other
"""

def categorize_expense(description: str) -> str:
    text = description.lower()

    # Simple keyword-based categorization
    if any(word in text for word in ["uber", "ola", "taxi", "bus", "train", "metro", "petrol"]):
        return "Transport"

    if any(word in text for word in ["zomato", "swiggy", "restaurant", "food", "pizza", "burger", "cafe"]):
        return "Food"

    if any(word in text for word in ["amazon", "flipkart", "shopping", "mall", "clothes"]):
        return "Shopping"

    if any(word in text for word in ["electricity", "rent", "bill", "wifi", "internet"]):
        return "Bills"

    if any(word in text for word in ["movie", "netflix", "concert", "game"]):
        return "Entertainment"

    if any(word in text for word in ["hospital", "medicine", "doctor", "pharmacy"]):
        return "Health"

    return "Other"