# -*- coding: utf-8 -*-

import logging
import random # این کتابخانه برای بُر زدن گزینه‌ها اضافه شد
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- تنظیمات اولیه ---
BOT_TOKEN = "7440922727:AAEMmpc3V-wvHDifg9uCV4h0mXxk_IqIqh4"
ADMIN_IDS = [5044871490, 5107444649]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- داده‌های سوالات و گروه‌ها ---
# ✨✨✨ بخش سوالات با محتوای جدید شما جایگزین شد ✨✨✨
QUESTIONS = [
    {
        "text": "❖ سؤال ۱\n\nدر رویا، کسی درِ چوبی را نیمه‌باز می‌گذارد و می‌رود. درونش نوری لرزان است.",
        "answers": [
            {"text": "صبر می‌کنم تا خودش بازگردد.", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "وارد می‌شوم؛ هر دری برای رفتن ساخته شده.", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "از کنارش رد می‌شوم.", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "پشت در می‌ایستم و گوش می‌دهم.", "scores": {"angel": 1, "human": 1, "demon": 0}},
            {"text": "در را می‌بندم تا نور بماند همان‌جا.", "scores": {"angel": 1, "human": 0, "demon": 1}},
        ],
    },
    {
        "text": "❖ سؤال ۲\n\nپرنده‌ای زخمی روی شانه‌ات می‌نشیند و می‌گوید: «پرواز فراموشم شده.»",
        "answers": [
            {"text": "سکوت می‌کنم؛ گاهی فراموشی نوعی آرامش است.", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "می‌پرسم: «می‌خواهی یاد بگیری یا بیاسایی؟»", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "پرهایش را نوازش می‌کنم.", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "چشم می‌بندم تا هر دو رویا ببینیم.", "scores": {"angel": 1, "human": 1, "demon": 0}},
            {"text": "پرنده را رها می‌کنم؛ پرواز باید خودش بازگردد.", "scores": {"angel": 1, "human": 0, "demon": 2}},
        ],
    },
    {
        "text": "❖ سؤال ۳\n\nدر اتاقی پر از آینه، تنها یکی تصویرت را نشان نمی‌دهد.",
        "answers": [
            {"text": "در آن آینه خیره می‌شوم تا ببینم چه پنهان کرده.", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "از کنارش می‌گذرم؛ بعضی چیزها باید خاموش بمانند.", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "تصویر دیگر آینه‌ها را نگاه می‌کنم تا یادم بیاید کی هستم.", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "آینه‌ی خاموش را لمس می‌کنم.", "scores": {"angel": 0, "human": 1, "demon": 1}},
            {"text": "چراغ را خاموش می‌کنم تا هیچ‌کدام تصویر ندهند.", "scores": {"angel": 1, "human": 0, "demon": 1}},
        ],
    },
    {
        "text": "❖ سؤال ۴\n\nزمانی که باران از یاد می‌رود و زمین تشنه است،",
        "answers": [
            {"text": "دعا می‌کنم تا آسمان به‌خاطر بیاورد.", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "چاهی می‌کنم تا خودم آب را بیابم.", "scores": {"angel": 0, "human": 3, "demon": 0}},
            {"text": "لبخند می‌زنم؛ هر تشنگی درسی دارد.", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "قطره‌ای اشک بر خاک می‌چکانم.", "scores": {"angel": 1, "human": 1, "demon": 0}},
            {"text": "زمین را می‌بوسم و می‌گذرم.", "scores": {"angel": 0, "human": 0, "demon": 2}},
        ],
    },
    {
        "text": "❖ سؤال ۵\n\nدر برابر دو صدای درونی ایستاده‌ای؛ یکی می‌گوید “ببخش”، دیگری “به‌یاد بسپار”.",
        "answers": [
            {"text": "هر دو را می‌پذیرم.", "scores": {"angel": 0, "human": 3, "demon": 0}},
            {"text": "اولی را خاموش می‌کنم تا دومی بماند.", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "دومی را آرام می‌کنم تا سکوت بماند.", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "از هر دو می‌خواهم با هم سخن بگویند.", "scores": {"angel": 1, "human": 1, "demon": 0}},
            {"text": "لبخند می‌زنم و راه خودم را می‌روم.", "scores": {"angel": 0, "human": 0, "demon": 2}},
        ],
    },
    {
        "text": "❖ سؤال ۶\n\nکتابی بی‌نام در برابرت باز می‌شود و واژه‌هایت را بر صفحه می‌نویسد.",
        "answers": [
            {"text": "می‌خوانم تا خودم را بشناسم.", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "می‌گذارم بنویسد، بدون خواندن.", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "قلم را می‌گیرم و خودم ادامه می‌دهم.", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "کتاب را می‌بندم؛ بعضی سرنوشت‌ها ناتمام باید بمانند.", "scores": {"angel": 1, "human": 1, "demon": 0}},
            {"text": "چند واژه پاک می‌کنم و می‌نویسم: «شروع دوباره».", "scores": {"angel": 0, "human": 1, "demon": 2}},
        ],
    },
    {
        "text": "❖ سؤال ۷\n\nکسی می‌گوید: «جهان تو را تماشا می‌کند.»",
        "answers": [
            {"text": "پاسخ می‌دهم: «باشد، اما من نیز او را می‌بینم.»", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "می‌گویم: «بگذار ببیند، من چیزی پنهان نمی‌کنم.»", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "لبخند می‌زنم: «تماشا می‌کند، چون دیگر کاری ندارد.»", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "شانه بالا می‌اندازم.", "scores": {"angel": 0, "human": 1, "demon": 1}},
            {"text": "چشمانم را می‌بندم تا هر دو ناپدید شویم.", "scores": {"angel": 1, "human": 1, "demon": 0}},
        ],
    },
    {
        "text": "❖ سؤال ۸\n\nاز تو می‌پرسند: «آیا به سرنوشت ایمان داری؟»",
        "answers": [
            {"text": "نه؛ ایمان فقط برای بی‌قدرت‌هاست.", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "آری؛ چون معنا می‌دهد به رنج.", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "نمی‌دانم؛ شاید ما هم بخشی ازش باشیم.", "scores": {"angel": 0, "human": 3, "demon": 0}},
            {"text": "به لبخند جواب می‌دهم.", "scores": {"angel": 1, "human": 1, "demon": 0}},
            {"text": "می‌گویم: «اگر سرنوشت من را باور داشته باشد، من هم او را.»", "scores": {"angel": 0, "human": 1, "demon": 2}},
        ],
    },
    {
        "text": "❖ سؤال ۹\n\nکسی در کنار جاده افتاده و نام تو را زمزمه می‌کند.",
        "answers": [
            {"text": "می‌ایستم و گوش می‌دهم.", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "خم می‌شوم تا چشمانش را ببینم.", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "نامش را تکرار می‌کنم تا صدا گم شود.", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "عبور می‌کنم؛ شاید خواب باشد.", "scores": {"angel": 0, "human": 1, "demon": 1}},
            {"text": "در سکوت دعا می‌کنم که فراموشم کند.", "scores": {"angel": 1, "human": 1, "demon": 0}},
        ],
    },
    {
        "text": "❖ سؤال ۱۰\n\nدر آستانه‌ی دریا، صدایی از عمق می‌گوید: «بازگرد، هنوز وقت نیست.»",
        "answers": [
            {"text": "بازمی‌گردم.", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "پیش می‌روم؛ هر صدا آزمونی‌ست.", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "می‌ایستم تا موج تصمیم بگیرد.", "scores": {"angel": 0, "human": 3, "demon": 0}},
            {"text": "می‌گویم: «اگر هنوز وقت نیست، پس چرا صدام زدی؟»", "scores": {"angel": 0, "human": 1, "demon": 2}},
            {"text": "لبخند می‌زنم و رد صدایم را دنبال می‌کنم.", "scores": {"angel": 1, "human": 1, "demon": 0}},
        ],
    },
]

GROUP_LINKS = {
    "angel": "https://t.me/+3znA_SaGOJo0Mzg8",
    "human": "https://t.me/+DIN_scA0cg5lNmM8",
    "demon": "https://t.me/+iUrNvTrK1mxmYjRk",
    "main": "https://t.me/+OpZRxrzRTyQ5OTc8"
}

race_names = {"angel": "فرشته 👼", "human": "انسان 👤", "demon": "شیطان 😈"}

# --- توابع اصلی ربات ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'result_race' in context.user_data:
        player_name = context.user_data.get('player_name', 'شما')
        result_race = context.user_data['result_race']
        result_text = (f"سلام {player_name}!\n"
                       f"شما قبلاً در آزمون شرکت کرده‌اید.\n\n"
                       f"نتیجه شما: **{race_names[result_race]}**\n\n"
                       f"می‌توانید از طریق دکمه‌های زیر وارد گروه‌ها شوید:")
        keyboard = [[InlineKeyboardButton(f"ورود به گروه {race_names[result_race]}", url=GROUP_LINKS[result_race])],
                    [InlineKeyboardButton("ورود به گپ اصلی", url=GROUP_LINKS["main"])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
        return
    context.user_data['state'] = 'awaiting_name'
    await update.message.reply_text("سلام! به رول پلی میستریس ورلد خوش اومدی.\nبرای شروع، لطفاً نام خودت رو وارد کن:")

async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    context.user_data['player_name'] = user_name
    context.user_data['current_question'] = 0
    context.user_data['answers'] = {} 
    context.user_data['scores'] = {"angel": 0, "human": 0, "demon": 0}
    await update.message.reply_text(f"خوش اومدی {user_name}!\nبریم سراغ سوال اول:")
    await send_question(update.message, context)

# --- ✨ تابع build_question_keyboard تغییر کرد ---
def build_question_keyboard(question_index, user_answers):
    """دکمه‌های گزینه‌ها را به صورت نامرتب و دکمه‌های ناوبری را می‌سازد."""
    keyboard = []
    question = QUESTIONS[question_index]
    
    # جدید: گزینه‌ها را همراه با ایندکس اصلی‌شان ذخیره کرده و سپس بُر می‌زنیم
    indexed_answers = list(enumerate(question["answers"]))
    random.shuffle(indexed_answers)
    
    # ساخت دکمه‌های گزینه‌ها بر اساس ترتیب جدید (نامرتب)
    for original_index, answer in indexed_answers:
        # چک می‌کنیم آیا کاربر قبلا این گزینه را انتخاب کرده یا نه
        prefix = "✅ " if user_answers.get(question_index) == original_index else ""
        # در callback_data از ایندکس اصلی استفاده می‌کنیم تا امتیازدهی درست انجام شود
        button = InlineKeyboardButton(f'{prefix}{answer["text"]}', callback_data=f"ans_{question_index}_{original_index}")
        keyboard.append([button])
        
    # ساخت دکمه‌های ناوبری (بدون تغییر)
    nav_buttons = []
    if question_index > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ سوال قبلی", callback_data=f"nav_prev_{question_index}"))
    if question_index < len(QUESTIONS) - 1:
        if question_index in user_answers:
             nav_buttons.append(InlineKeyboardButton("سوال بعدی ➡️", callback_data=f"nav_next_{question_index}"))
    else:
        if question_index in user_answers:
            nav_buttons.append(InlineKeyboardButton("🏆 مشاهده نتیجه", callback_data="finish_quiz"))

    keyboard.append(nav_buttons)
    return InlineKeyboardMarkup(keyboard)

async def send_question(message, context: ContextTypes.DEFAULT_TYPE, message_id=None):
    question_index = context.user_data['current_question']
    question = QUESTIONS[question_index]
    keyboard = build_question_keyboard(question_index, context.user_data.get('answers', {}))
    if message_id:
        await context.bot.edit_message_text(chat_id=message.chat_id, message_id=message_id, text=question["text"], reply_markup=keyboard)
    else:
        await message.reply_text(question["text"], reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    data = query.data.split('_')
    action = data[0]
    if action == "ans":
        question_index = int(data[1])
        answer_index = int(data[2])
        context.user_data['answers'][question_index] = answer_index
        await send_question(query.message, context, message_id=query.message.message_id)
    elif action == "nav":
        direction = data[1]
        current_index = int(data[2])
        if direction == "next":
            context.user_data['current_question'] = current_index + 1
        elif direction == "prev":
            context.user_data['current_question'] = current_index - 1
        await send_question(query.message, context, message_id=query.message.message_id)
    elif action == "finish":
        await calculate_and_send_result(query.message, context, update.effective_user)

def calculate_scores(user_answers):
    scores = {"angel": 0, "human": 0, "demon": 0}
    for q_idx, a_idx in user_answers.items():
        selected_answer_scores = QUESTIONS[q_idx]["answers"][a_idx]["scores"]
        for race, score in selected_answer_scores.items():
            scores[race] += score
    return scores

# --- ⚠️ این تابع تغییر کرده است ⚠️ ---
async def calculate_and_send_result(message, context: ContextTypes.DEFAULT_TYPE, user):
    final_scores = calculate_scores(context.user_data['answers'])
    
    # --- ✨ تغییر جدید: حذف موقت نتیجه شیطان ---
    # برای اینکه تا اطلاع ثانوی کسی شیطان نشود، امتیاز آن را منفی می‌کنیم
    final_scores['demon'] = -1 
    # --- پایان تغییر ---

    races_sorted = sorted(final_scores.items(), key=lambda item: (-item[1], ['angel', 'human', 'demon'].index(item[0])))
    result_race = races_sorted[0][0]
    context.user_data['result_race'] = result_race
    player_name = context.user_data.get('player_name', 'بازیکن')
    
    result_text_user = (f"خب {player_name}، آزمون تموم شد!\n\n"
                       f"نتیجه نهایی: **شما یک {race_names[result_race]} هستید!**\n\n"
                       f"بر اساس شخصیت شما، به گروه زیر دعوت می‌شوید:")
    keyboard = [[InlineKeyboardButton(f"ورود به گروه {race_names[result_race]}", url=GROUP_LINKS[result_race])],
                [InlineKeyboardButton("ورود به گپ اصلی", url=GROUP_LINKS["main"])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(result_text_user, reply_markup=reply_markup, parse_mode='Markdown')

    if ADMIN_IDS:
        # برای گزارش به ادمین، امتیاز اصلی شیطان را نمایش می‌دهیم
        original_demon_score = calculate_scores(context.user_data['answers'])['demon']
        admin_report_text = (f"👤 گزارش تست جدید:\n\n"
                           f"نام بازیکن: {player_name}\n"
                           f"نام کاربری تلگرام: @{user.username or 'ندارد'}\n"
                           f"آیدی عددی: `{user.id}`\n\n"
                           f"نتیجه تست (بدون شیطان): **{race_names[result_race]}**\n\n"
                           f"امتیازات:\n"
                           f"👼 فرشته: {final_scores['angel']}\n"
                           f"👤 انسان: {final_scores['human']}\n"
                           f"😈 شیطان (امتیاز اصلی): {original_demon_score}") # نمایش امتیاز واقعی
        if 'all_results' not in context.bot_data:
            context.bot_data['all_results'] = []
        context.bot_data['all_results'].append(admin_report_text)
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(chat_id=admin_id, text=admin_report_text, parse_mode='Markdown')
            except Exception as e:
                logger.error(f"ارسال پیام به ادمین {admin_id} با خطا مواجه شد: {e}")

async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == 'awaiting_name':
        context.user_data['state'] = ''
        await name_handler(update, context)
    else:
        await update.message.reply_text("برای شروع آزمون، دستور /start را ارسال کنید. اگر قبلا آزمون داده‌اید، نتیجه شما نمایش داده خواهد شد.")

async def get_results_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ شما اجازه دسترسی به این دستور را ندارید.")
        return
    all_results = context.bot_data.get('all_results', [])
    if not all_results:
        await update.message.reply_text("هنوز هیچ نتیجه‌ای در ربات ثبت نشده است.")
        return
    last_10_results = all_results[-10:]
    response_text = "📋 **آخرین نتایج ثبت شده:**\n\n" + "\n\n---\n\n".join(last_10_results)
    await update.message.reply_text(response_text, parse_mode='Markdown')

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("results", get_results_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))
    print("ربات در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()
