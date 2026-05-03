import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

BOT_TOKEN = "8667805331:AAEHyudTxsmRpUdeGzBbqDXFEoTYKr60A28"
ADMIN_ID = 6846032351

PLATFORM, PRODUCT_LINK, QUANTITY, ADDRESS, PHONE, CONFIRM = range(6)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🟠 Uzum Market", "🔵 Ozon"]]
    await update.message.reply_text(
        "👋 Salom! Buyurtma botiga xush kelibsiz!\n\nQaysi platformadan buyurtma bermoqchisiz?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return PLATFORM

async def choose_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['platform'] = update.message.text
    await update.message.reply_text(
        "🔗 Mahsulot havolasini (link) yuboring:",
        reply_markup=ReplyKeyboardRemove()
    )
    return PRODUCT_LINK

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['link'] = update.message.text
    await update.message.reply_text("📦 Nechta kerak?")
    return QUANTITY

async def get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['quantity'] = update.message.text
    await update.message.reply_text("🏠 Yetkazib berish manzilingizni yozing:")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("📱 Telefon raqamingizni yozing:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    data = context.user_data
    keyboard = [["✅ Tasdiqlash", "❌ Bekor qilish"]]
    await update.message.reply_text(
        f"📋 Buyurtma:\n\n"
        f"🛒 Platforma: {data['platform']}\n"
        f"🔗 Havola: {data['link']}\n"
        f"📦 Miqdor: {data['quantity']}\n"
        f"🏠 Manzil: {data['address']}\n"
        f"📱 Telefon: {data['phone']}\n\n"
        f"Tasdiqlaysizmi?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "✅ Tasdiqlash":
        data = context.user_data
        user = update.message.from_user
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 YANGI BUYURTMA!\n\n"
                 f"👤 Mijoz: {user.full_name}\n"
                 f"🛒 Platforma: {data['platform']}\n"
                 f"🔗 Havola: {data['link']}\n"
                 f"📦 Miqdor: {data['quantity']}\n"
                 f"🏠 Manzil: {data['address']}\n"
                 f"📱 Telefon: {data['phone']}"
        )
        await update.message.reply_text(
            "✅ Buyurtmangiz qabul qilindi! Tez orada bog'lanamiz. 🙏",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            "❌ Bekor qilindi. /start bosing.",
            reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi. /start bosing.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_platform)],
            PRODUCT_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_quantity)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv)
    print("✅ Bot ishlamoqda...")
    app.run_polling()

if __name__ == "__main__":
    main()
