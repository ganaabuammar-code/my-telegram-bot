import asyncio
import random
from datetime import datetime, time, timedelta
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ==================== CONFIGURATION ====================
TOKEN = "yahan_bot_token_lagao"
TARGET_CHANNEL_ID = -100yahan_channel_id_lagao
# =======================================================


# Standard Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Sana AI Signal Bot Active Hai!")


# Automated Daily Signal Loop (Starts Daily at 10:00 AM)
async def channel_signal_sender(bot):
    messages = [
        "💖 USD / BRL OTC 💖\n\n🥺 1 MINUTES 💗",
        "🌸 USD / MXN OTC 🌸\n\n💞 1 MINUTES 😘",
        "✨ USD / NGN OTC ✨\n\n🤍 1 MINUTES 🫶",
        "💫 USD / ZAR OTC 💫\n\n💕 1 MINUTES 😍",
        "🌸 USD / INR OTC 🌸\n\n💞 1 MINUTES 😘",
        "🌸 USD / PKR OTC 🌸\n\n💞 1 MINUTES 😘",
        "🌸 NZD / CHF OTC 🌸\n\n💞 1 MINUTES 😘",
        "🌸 USD / ARS OTC 🌸\n\n💞 1 MINUTES 😘",
        "🌸 USD / COP OTC 🌸\n\n💞 1 MINUTES 😘",
        "🌸 CAD / CHF OTC 🌸\n\n💞 1 MINUTES 😘",
        "🌸 USD / BDT OTC 🌸\n\n💞 1 MINUTES 😘",
    ]

    while True:
        now = datetime.now()
        start_time = datetime.combine(now.date(), time(10, 0, 0))

        # Agar abhi time subah 10 AM se pehle ka hai, to 10 AM tak wait karega
        if now < start_time:
            wait_seconds = (start_time - now).total_seconds()
            await asyncio.sleep(wait_seconds)
        # Agar aaj 10 AM beet chuka hai aur signals poore ho chuke hain, to agle din tak wait karega
        elif now >= start_time and 'day_completed' in locals() and day_completed == now.day:
            await asyncio.sleep(60)
            continue

        signal_count = 0

        # Daily 100 Signals Loop
        while signal_count < 100:
            now = datetime.now()

            # Real Clock Calculation (4 Minutes = 240 Seconds Interval):
            # Target trade time har 4 min par rounds hone chahiye (e.g. 10:04, 10:08, etc.)
            seconds_since_epoch = int(now.timestamp())
            remainder = seconds_since_epoch % 240

            # Signal trade time se 30 seconds pehle trigger karne ke liye target is 210s
            if remainder < 210:
                sleep_time = 210 - remainder
            else:
                sleep_time = (240 - remainder) + 210

            await asyncio.sleep(sleep_time)

            # Signal details calculation
            signal_count += 1
            
            # Trade time is exact 30 seconds after the signal trigger time
            trade_datetime = datetime.now() + timedelta(seconds=30)
            trade_time_str = trade_datetime.strftime("%H:%M")

            msg = random.choice(messages)
            direction = random.choice(["🔼 UP / CALL", "🔽 DOWN / PUT"])
            
            # Formatted full signal message
            full_msg = (
                f"{msg}\n\n"
                f"{direction}\n\n"
                f"⏰ TIME = {trade_time_str}\n"
                f"📊 SIGNAL = {signal_count} / 100"
            )

            await bot.send_message(chat_id=TARGET_CHANNEL_ID, text=full_msg)

            # Safe delay to prevent duplicate sends within the same second
            await asyncio.sleep(5)

        # 100 Signals Complete Hone Par Simple Daily Report Message
        summary_msg = (
            "❤️ SANA AI SIGNALS ❤️\n\n"
            "      TODAY TOTAL SIGNALS = 100\n\n"
            "      ALL SIGNALS COMPLETED SUCCESSFULLY! ✨"
        )

        await bot.send_message(chat_id=TARGET_CHANNEL_ID, text=summary_msg)

        # Mark current day as completed
        day_completed = datetime.now().day
        await asyncio.sleep(10)


# Bot Startup Callback
async def post_init(application: Application):
    asyncio.create_task(channel_signal_sender(application.bot))


# Main Application Setup
def main():
    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
