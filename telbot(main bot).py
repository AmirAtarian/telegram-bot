import logging
import json
from telegram import *
from telegram.ext import *
txt_1 = "دستورات قابل استفاده:"
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("وارد کردن نمره"  , callback_data= " کلیک کنید'/point' روی گزینه " ),
            InlineKeyboardButton("دریافت برنامه هفتگی", callback_data= "    دستور /plan را وارد کنید :"),
        ],    
        [

            InlineKeyboardButton("راهنما", callback_data = f"{txt_1}/start - /help - /point - /set_time - plan" ),
            InlineKeyboardButton("تنطیم هشدار", callback_data = "از دستور /set_time  استفاده کنید" ),
            InlineKeyboardButton("انتخاب رنگ ", callback_data = "  از دستور /color  استفاده کنید" ),
        ],
        
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("سلام به ربات روان یار خوش آمدید لطفا یکی از گزینه های زیر را انتخاب کنید" , reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    
    await query.answer()

    await query.edit_message_text(text=f"{query.data}")

async def point(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_1 = [
        [
            InlineKeyboardButton("نمره بین 0 و 19"  , callback_data= " بیماری شما سطح یک است" ),
            InlineKeyboardButton(" نمره بین 20 و 28 ", callback_data= "  بیماری شما سطح دو است"),
        ],
         [

            InlineKeyboardButton("نمره بین 29 و 63", callback_data = "   بیماری شما سطح سه است " ),
        ],
    ] 
    reply_markup = InlineKeyboardMarkup(keyboard_1)
    await update.message.reply_text ("حدود نمره دریافتی شما:", reply_markup=reply_markup)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(
        " با توجه به سطحی که ربات به شما اعلام کرد یرنامه خود را مشاهده کنید "      
        "با استفاده از دکمه (برنامه روزانه) پایین صفحه میتوانید به همه برنامه ها دسترسی پیدا کنیدا"     
        " در صورت نیاز به کلید از این کد استفاده کنید (96XX00tjG47MtZvcprrBfQ) " ))      

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(" با استفاده از دکمه (برنامه روزانه) پایین صفحه میتوانید به همه برنامه ها دسترسی پیدا کنیدا" ))      
    await context.bot.send_message(chat_id=update.effective_chat.id, text=("  در صورت نیاز به کلید از این کد استفاده کنید (96XX00tjG47MtZvcprrBfQ) " ))      

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=(" از دستورات زیر میتوانید استفاده کنید'/start - /help - /point - /set_time - plan'"))
 

async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("با استفاده از این قسمت برای خودت یادآور تنظبم کن. برای تنظیم زمان از دستور (برحسب ثانیه) set/  استفاده کنید")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"اوه!   یه نگاهی به برنامت بنداز!  ")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("متاسفم به عقب نمیتونیم برگردیم!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

        text = "هشدار با موفقیت تنظیم شد."
        if job_removed:
            text += "هشدار قبلی حذف شد."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text(" بری تنظیم هشدار /set <seconds>از این دستور استفاده کن: ")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "آلارم با موفقیت لغو شد" if job_removed else "هشدار فعالی نداری."
    await update.message.reply_text(text)



async def color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        ".",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="اینجا کلیک کن تا اپ رنگ برات باز بشه!",
                web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),
            )
        ),
    )


# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    await update.message.reply_text("با استفاده از رنگی که انتخاب کردی محیط اطراف رو تزیین کن تا استرس کاهش پیدا کنه(:")

    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=f" HEX value <code>{data['hex']}</code>.  کد رنگ انتخاب شده: The "
        f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>.",
        reply_markup=ReplyKeyboardRemove(),
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token("5971839805:AAGLh6bZcTT6yfgSi-ZqlBCfLLjMGBn4p3U").build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    point_handler = CommandHandler('point', point)
    application.add_handler(point_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    application.add_handler(CommandHandler("set", set_timer))

    application.add_handler(CommandHandler("set_time", set_time))

    application.add_handler(CommandHandler("unset", unset))

    application.add_handler(CallbackQueryHandler(button))

    application.add_handler(CommandHandler("color", color))

    application.add_handler(CommandHandler("plan", plan))

    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    

application.run_polling()
