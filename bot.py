
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from cbu_api import get_exchange_rates


BOT_TOKEN = "8700580174:AAFV9wumLkLix-AD7Ad8kkHmJeziQvVs2S0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def get_main_keyboard():
    keyboard = [
        ["💵 Dollar (USD)", "💶 Yevro (EUR)"],
        ["🇷🇺 Rubl (RUB)", "📊 Barcha kurslar"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🇺🇿 <b>O'zbekiston Respublikasi Markaziy Banki</b> valyuta kurslari botiga xush kelibsiz!\n\n"
        "Kerakli valyutani tanlang yoki pastdagi tugmalardan foydalaning."
    )
    await update.message.reply_text(
        welcome_text, 
        parse_mode="HTML", 
        reply_markup=get_main_keyboard()
    )


async def handle_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Bot "Qidirilmoqda..." deb tursin
    waiting_msg = await update.message.reply_text("🔄 Markaziy bankdan ma'lumot olinmoqda...")
    
    # API'dan kurslarni tortamiz
    rates = get_exchange_rates()
    
    if not rates:
        await waiting_msg.edit_text("❌ Markaziy bank serveri bilan bog'lanishda xatolik yuz berdi. Birozdan so'ng urinib ko'ring.")
        return

    response = ""
    
    if "Dollar" in text:
        usd = rates.get("USD")
        response = (
            f"🇺🇸 <b>{usd['name']} (USD)</b>\n"
            f"💰 Kurs: <code>{usd['rate']}</code> so'm\n"
            f"📈 O'zgarish (Kechagiga nisbatan): {usd['diff']} so'm\n"
            f"📅 Sana: {usd['date']}"
        )
    elif "Yevro" in text:
        eur = rates.get("EUR")
        response = (
            f"🇪🇺 <b>{eur['name']} (EUR)</b>\n"
            f"💰 Kurs: <code>{eur['rate']}</code> so'm\n"
            f"📈 O'zgarish: {eur['diff']} so'm\n"
            f"📅 Sana: {eur['date']}"
        )
    elif "Rubl" in text:
        rub = rates.get("RUB")
        response = (
            f"🇷🇺 <b>{rub['name']} (RUB)</b>\n"
            f"💰 Kurs: <code>{rub['rate']}</code> so'm\n"
            f"📈 O'zgarish: {rub['diff']} so'm\n"
            f"📅 Sana: {rub['date']}"
        )
    elif "Barcha kurslar" in text:
        usd = rates.get("USD")
        eur = rates.get("EUR")
        rub = rates.get("RUB")
        
        response = (
            f"📊 <b>Markaziy Bank kurslari ({usd['date']}):</b>\n\n"
            f"🇺🇸 1 USD = <code>{usd['rate']}</code> UZS ({usd['diff']})\n"
            f"🇪🇺 1 EUR = <code>{eur['rate']}</code> UZS ({eur['diff']})\n"
            f"🇷🇺 1 RUB = <code>{rub['rate']}</code> UZS ({rub['diff']})"
        )
    else:
        response = "🤔 Noma'lum buyruq. Iltimos, menyudagi tugmalardan foydalaning."

    await waiting_msg.edit_text(response, parse_mode="HTML")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
  
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_currency))

    print("Valyuta boti ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()