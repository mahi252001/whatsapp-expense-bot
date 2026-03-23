from fastapi import APIRouter, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Expense
from app.expense_parser import parse_expense
from app.ai_service import categorize_expense
from app.cache_service import get_cached_category, save_merchant_category

from app.user_service import get_or_create_user
from app.welcome_service import get_welcome_message

router = APIRouter()


@router.post("/whatsapp/webhook")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...)
):
    db: Session = SessionLocal()

    try:
        message = Body.strip().lower()
        user_number = From



        # =========================
        # USER ONBOARDING
        # =========================

        user, is_new_user = get_or_create_user(db, user_number)

        if is_new_user:

            reply_text = get_welcome_message()

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )


        # =========================
        # ✅ SUMMARY COMMAND
        # =========================
        if message == "summary":
            from app.summary_service import get_weekly_summary

            results, total = get_weekly_summary(user_number)

            if total == 0:
                reply_text = "📭 No expenses recorded this week."
            else:
                response_text = "📊 Weekly Summary\n\n"
                response_text += f"Total: ₹{int(total)}\n\n"

                for category, amount in results:
                    response_text += f"{category}: ₹{int(amount)}\n"

                reply_text = response_text

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )

        if message.startswith("month"):
            from app.monthly_summary_service import get_monthly_summary
            from datetime import datetime
            import calendar

            parts = message.split()

            now = datetime.utcnow()
            year = now.year
            month = now.month

            # If user specified a month
            if len(parts) > 1:
                value = parts[1].lower()

                month_map = {
                    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
                    "may": 5, "jun": 6, "jul": 7, "aug": 8,
                    "sep": 9, "oct": 10, "nov": 11, "dec": 12
                }

                try:
                    if value.isdigit():
                        month = int(value)

                    elif value in month_map:
                        month = month_map[value]

                    elif "-" in value:
                        year_str, month_str = value.split("-")
                        year = int(year_str)
                        month = int(month_str)

                except Exception:
                    pass

            results, total = get_monthly_summary(user_number, year, month)

            if total == 0:
                reply_text = "📭 No expenses recorded for this month."
            else:
                month_name = calendar.month_name[month]

                response_text = f"📅 {month_name} {year} Summary\n\n"
                response_text += f"Total: ₹{int(total)}\n\n"

                for category, amount in results:
                    response_text += f"{category}: ₹{int(amount)}\n"

                reply_text = response_text

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )

        if message.startswith("year"):
            from app.yearly_summary_service import get_yearly_summary
            from datetime import datetime

            parts = message.split()

            now = datetime.utcnow()
            year = now.year

            # If user specifies a year
            if len(parts) > 1:
                try:
                    year = int(parts[1])
                except Exception:
                    pass

            results, total = get_yearly_summary(user_number, year)

            if total == 0:
                reply_text = f"📭 No expenses recorded for {year}."
            else:
                response_text = f"📅 {year} Summary\n\n"
                response_text += f"Total: ₹{int(total)}\n\n"

                for category, amount in results:
                    response_text += f"{category}: ₹{int(amount)}\n"

                reply_text = response_text

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )

        if message == "undo":
            from app.undo_service import undo_last_expense

            result = undo_last_expense(user_number)

            if not result:
                reply_text = "📭 No expense to undo."
            else:
                reply_text = (
                    "↩️ Last expense removed\n\n"
                    f"₹{int(result['amount'])} - {result['description']} ({result['category']})"
                )

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )

        if message == "last":
            from app.expense_query_service import get_last_expenses

            expenses = get_last_expenses(user_number)

            if not expenses:
                reply_text = "📭 No expenses found."
            else:
                response = "🧾 Last Expenses\n\n"

                for i, exp in enumerate(expenses, start=1):
                    response += f"{i}. ₹{int(exp.amount)} - {exp.description} ({exp.category})\n"

                reply_text = response

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )

        if message.startswith("delete"):
            from app.delete_service import delete_by_serial

            parts = message.split()

            if len(parts) != 2 or not parts[1].isdigit():
                reply_text = "❌ Usage: delete 2"
            else:
                serial = int(parts[1])

                result = delete_by_serial(user_number, serial)

                if not result:
                    reply_text = "⚠️ Invalid expense number."
                else:
                    description, amount, category = result

                    reply_text = (
                        "🗑️ Expense deleted\n\n"
                        f"₹{int(amount)} - {description} ({category})"
                    )

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )

        if message == "help":

            reply_text = (
                "🤖 Expense Bot Commands\n\n"
                "Add expense:\n"
                "Uber 300\n\n"

                "Commands:\n"
                "summary → weekly summary\n"
                "month → monthly summary\n"
                "month feb → specific month\n"
                "year → yearly summary\n\n"

                "last → show last 5 expenses\n"
                "delete 2 → delete expense\n"
                "undo → undo last expense\n"
                "help → show commands"
            )

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )
        
        if message.startswith("edit"):
            from app.edit_service import edit_expense_amount

            parts = message.split()

            if len(parts) != 3 or not parts[1].isdigit():
                reply_text = "❌ Usage: edit 2 500"
            else:
                serial = int(parts[1])

                try:
                    new_amount = float(parts[2])
                except:
                    new_amount = None

                if new_amount is None:
                    reply_text = "❌ Invalid amount."
                else:
                    result = edit_expense_amount(user_number, serial, new_amount)

                    if not result:
                        reply_text = "⚠️ Invalid expense number."
                    else:
                        description, category, old_amount, new_amount = result

                        reply_text = (
                            "✏️ Expense updated\n\n"
                            f"{description} ({category})\n"
                            f"₹{int(old_amount)} → ₹{int(new_amount)}"
                        )

        if message == "stats":
            from app.stats_service import get_spending_stats

            stats = get_spending_stats(user_number)

            if not stats["category"]:
                reply_text = "📭 No expenses recorded yet."
            else:
                reply_text = (
                    "📊 Spending Stats\n\n"
                    f"Most spent category: {stats['category']}\n"
                    f"Most frequent merchant: {stats['merchant']}\n"
                    f"Avg daily spend: ₹{int(stats['avg_daily'])}"
                )

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )

        if message.strip().lower() == "insight":

            from app.insight_service import get_spending_stats, generate_insight

            stats = get_spending_stats(db, user_number)

            if stats["total"] == 0:
                reply_text = "📭 No expenses yet to generate insights."
            else:
                insight = generate_insight(stats)

                reply_text = f"💡 Spending Insight\n\n{insight}"

            twilio_response = MessagingResponse()
            twilio_response.message(reply_text)

            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )

        # =========================
        # ✅ NORMAL / MULTI-LINE EXPENSE FLOW
        # =========================
        lines = message.split("\n")
        saved_expenses = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parsed = parse_expense(line)

            if not parsed:
                continue  # skip invalid lines

            description = parsed["description"]
            amount = parsed["amount"]

            merchant = description.lower()

            # =========================
            # CACHE CHECK
            # =========================
            category = get_cached_category(db, merchant)

            if not category:
                category = categorize_expense(merchant)
                save_merchant_category(db, merchant, category)

            expense = Expense(
                phone=user_number,
                description=description,
                amount=amount,
                category=category
            )

            db.add(expense)

            saved_expenses.append(
                f"₹{amount} - {description} ({category})"
            )

        if not saved_expenses:
            raise ValueError("Invalid format")

        db.commit()

        reply_text = "✅ Saved:\n\n" + "\n".join(saved_expenses)

    except ValueError:
        reply_text = (
            "❌ Please enter expense like:\n\n"
            "Uber 320\n"
            "Tea 20\n"
            "Swiggy 450\n\n"
            "You can also send multiple lines:\n"
            "Uber 300\n"
            "Bus 40"
        )

    except Exception as e:
        print("Error:", e)
        reply_text = "⚠️ Something went wrong. Try again."

    finally:
        db.close()

    # =========================
    # ✅ DEFAULT RESPONSE
    # =========================
    twilio_response = MessagingResponse()
    twilio_response.message(reply_text)

    return Response(
        content=str(twilio_response),
        media_type="application/xml"
    )