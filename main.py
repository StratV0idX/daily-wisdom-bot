import os, requests, json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ------------- Bot --------------------
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

# ------------ FILE SAVE ---------------
def save_quote(quote):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # script location
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, "quotes_log.json")

    with open(file_path, "a") as f:
        f.write(json.dumps({"quote": quote}) + "\n")

# ----------- GET QUOTE ---------------
def get_quote():
    url = "https://api.api-ninjas.com/v2/randomquotes"
    headers = {"X-Api-Key": API_KEY}

    response = requests.get(url, headers=headers)

    # Always good practice 👇
    if response.status_code != 200:
        return "❌ Failed to fetch quote. Try again later."

    data = response.json()
    if not data:
        return "⚠️ No quote found"

    quote_data = data[0]

    return f"🌟 {quote_data['quote']}\n\n— {quote_data['author']}"

# -------- COMMANDS --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to DailyWisdomBot!\n\n" "Use /quote to get an inspiring quote ✨"
    )

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = get_quote()
    save_quote(q)
    await update.message.reply_text(q)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n"
        "/start - Start bot\n"
        "/quote - Get a quote\n"
        "/help - Show this help"
    )

# -------- MAIN --------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quote", quote))
app.add_handler(CommandHandler("help", help_command))

print("Bot is running... 🤖")
app.run_polling()
