import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- تنظیمات اولیه ---
# در این قسمت توکن ربات خود را قرار دهید
BOT_TOKEN = "7440922727:AAEMmpc3V-wvHDifg9uCV4h0mXxk_IqIqh4"

# فعال کردن لاگ برای دیباگ کردن
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- داده‌های سوالات و گروه‌ها ---
QUESTIONS = [
    {
        "text": "سؤال ۱: اگر ببینی کسی در خیابان گرسنه است چه کار می‌کنی؟",
        "answers": [
            {"text": "غذایم را با او تقسیم می‌کنم", "scores": {"angel": 2, "human": 1, "demon": 0}},
            {"text": "به او پول می‌دهم", "scores": {"angel": 1, "human": 2, "demon": 0}},
            {"text": "بی‌تفاوت رد می‌شوم", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "مسخره‌اش می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "وانمود می‌کنم ندیدم", "scores": {"angel": 0, "human": 1, "demon": 1}},
        ],
    },
    {
        "text": "سؤال ۲: اگر دشمن تو زخمی روی زمین افتاده باشد؟",
        "answers": [
            {"text": "او را درمان می‌کنم", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "به او آب می‌دهم", "scores": {"angel": 2, "human": 1, "demon": 0}},
            {"text": "فقط رد می‌شوم", "scores": {"angel": 0, "human": 1, "demon": 1}},
            {"text": "به او ضربه آخر را می‌زنم", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "به او می‌خندم و می‌روم", "scores": {"angel": 0, "human": 0, "demon": 2}},
        ],
    },
    {
        "text": "سؤال ۳: وقتی به قدرت می‌رسی، با مردم چه می‌کنی؟",
        "answers": [
            {"text": "از قدرت برای کمک استفاده می‌کنم", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "عدالت را برقرار می‌کنم", "scores": {"angel": 1, "human": 2, "demon": 0}},
            {"text": "برای سود شخصی استفاده می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "مخالفان را نابود می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "فقط از خودم و خانواده‌ام حمایت می‌کنم", "scores": {"angel": 0, "human": 2, "demon": 0}},
        ],
    },
    {
        "text": "سؤال ۴: اگر راز بزرگی درباره دوستت بدانی؟",
        "answers": [
            {"text": "حفظش می‌کنم", "scores": {"angel": 2, "human": 2, "demon": 0}},
            {"text": "در شرایط لازم به او کمک می‌کنم", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "از آن علیه او استفاده می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "برای سرگرمی لو می‌دهم", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "بی‌تفاوت می‌مانم", "scores": {"angel": 0, "human": 1, "demon": 0}},
        ],
    },
    {
        "text": "سؤال ۵: در نبرد سخت، وقتی یار تو زخمی می‌شود؟",
        "answers": [
            {"text": "او را از میدان بیرون می‌برم", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "کنارش می‌مانم تا بمیریم یا زنده بمانیم", "scores": {"angel": 1, "human": 2, "demon": 0}},
            {"text": "او را رها می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "از ضعف او استفاده می‌کنم تا خودم قوی‌تر شوم", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "با بی‌خیالی ادامه می‌دهم", "scores": {"angel": 0, "human": 1, "demon": 1}},
        ],
    },
        {
        "text": "سؤال ۶: وقتی کسی تو را تحقیر می‌کند؟",
        "answers": [
            {"text": "می‌بخشمش", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "نادیده می‌گیرم", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "نقشه انتقام می‌کشم", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "او را مسخره می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "با آرامش جواب می‌دهم", "scores": {"angel": 2, "human": 0, "demon": 0}},
        ],
    },
    {
        "text": "سؤال ۷: اگر بتوانی ذهن مردم را کنترل کنی؟",
        "answers": [
            {"text": "هرگز استفاده نمی‌کنم", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "فقط برای کمک استفاده می‌کنم", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "برای منافع خودم استفاده می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "همه را برده می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "برای عدالت و نظم", "scores": {"angel": 0, "human": 2, "demon": 0}},
        ],
    },
    {
        "text": "سؤال ۸: در برابر وسوسه قدرت سیاه؟",
        "answers": [
            {"text": "مقاومت می‌کنم", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "مردد می‌شوم ولی نمی‌پذیرم", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "از آن استفاده می‌کنم", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "با شوق می‌پذیرم", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "فقط امتحان می‌کنم", "scores": {"angel": 0, "human": 1, "demon": 1}},
        ],
    },
    {
        "text": "سؤال ۹: اگر انتخاب بین نجات یک نفر یا هزار نفر داشته باشی؟",
        "answers": [
            {"text": "هزار نفر", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "کسی که به من نزدیک‌تر است", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "کسی که منافع بیشتری دارد", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "هیچ‌کس", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "قرعه می‌کشم", "scores": {"angel": 0, "human": 1, "demon": 0}},
        ],
    },
    {
        "text": "سؤال ۱۰: بزرگ‌ترین ارزش تو چیست؟",
        "answers": [
            {"text": "ایثار", "scores": {"angel": 3, "human": 0, "demon": 0}},
            {"text": "عدالت", "scores": {"angel": 0, "human": 3, "demon": 0}},
            {"text": "قدرت", "scores": {"angel": 0, "human": 0, "demon": 3}},
            {"text": "آزادی", "scores": {"angel": 2, "human": 1, "demon": 0}},
            {"text": "برتری شخصی", "scores": {"angel": 0, "human": 0, "demon": 2}},
        ],
    },
]

GROUP_LINKS = {
    "angel": "https://t.me/+3znA_SaGOJo0Mzg8",
    "human": "https://t.me/+DIN_scA0cg5lNmM8",
    "demon": "https://t.me/+iUrNvTrK1mxmYjRk",
    "main": "https://t.me/+OpZRxrzRTyQ5OTc8"
}

# --- توابع اصلی ربات ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start را مدیریت می‌کند. شروع آزمون."""
    context.user_data.clear() # پاک کردن داده‌های قبلی کاربر
    context.user_data['state'] = 'awaiting_name'
    await update.message.reply_text("سلام! به رول پلی میستریس ورلد خوش اومدی.\nبرای شروع، لطفاً نام خودت رو وارد کن:")

async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نام کاربر را دریافت و آزمون را شروع می‌کند."""
    user_name = update.message.text
    context.user_data['player_name'] = user_name
    context.user_data['current_question'] = 0
    context.user_data['answers'] = {} # برای ذخیره پاسخ‌های کاربر
    context.user_data['scores'] = {"angel": 0, "human": 0, "demon": 0}

    await update.message.reply_text(f"خوش اومدی {user_name}!\nبریم سراغ سوال اول:")
    await send_question(update.message, context)

def build_question_keyboard(question_index, user_answers):
    """دکمه‌های گزینه‌ها و دکمه‌های ناوبری را می‌سازد."""
    keyboard = []
    question = QUESTIONS[question_index]
    
    # ساخت دکمه‌های گزینه‌ها
    for i, answer in enumerate(question["answers"]):
        prefix = "✅ " if user_answers.get(question_index) == i else ""
        button = InlineKeyboardButton(f'{prefix}{answer["text"]}', callback_data=f"ans_{question_index}_{i}")
        keyboard.append([button])
        
    # ساخت دکمه‌های ناوبری
    nav_buttons = []
    if question_index > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ سوال قبلی", callback_data=f"nav_prev_{question_index}"))
    if question_index < len(QUESTIONS) - 1:
        # فقط در صورتی دکمه بعدی را نشان بده که به این سوال جواب داده شده باشد
        if question_index in user_answers:
             nav_buttons.append(InlineKeyboardButton("سوال بعدی ➡️", callback_data=f"nav_next_{question_index}"))
    else:
        # اگر سوال آخر است، دکمه "مشاهده نتیجه" را نشان بده
        if question_index in user_answers:
            nav_buttons.append(InlineKeyboardButton("🏆 مشاهده نتیجه", callback_data="finish_quiz"))

    keyboard.append(nav_buttons)
    return InlineKeyboardMarkup(keyboard)

async def send_question(message, context: ContextTypes.DEFAULT_TYPE, message_id=None):
    """یک سوال مشخص را با گزینه‌ها ارسال یا ویرایش می‌کند."""
    question_index = context.user_data['current_question']
    question = QUESTIONS[question_index]
    keyboard = build_question_keyboard(question_index, context.user_data.get('answers', {}))
    
    # اگر message_id داده شده باشد، پیام را ویرایش می‌کند، در غیر این صورت پیام جدید می‌فرستد
    if message_id:
        await context.bot.edit_message_text(
            chat_id=message.chat_id,
            message_id=message_id,
            text=question["text"],
            reply_markup=keyboard
        )
    else:
        await message.reply_text(question["text"], reply_markup=keyboard)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ‌های دکمه‌ای را مدیریت می‌کند."""
    query = update.callback_query
    await query.answer() # برای اینکه تلگرام بفهمد که کلیک دریافت شده است
    
    data = query.data.split('_')
    action = data[0]

    if action == "ans":
        question_index = int(data[1])
        answer_index = int(data[2])
        
        # ذخیره پاسخ
        context.user_data['answers'][question_index] = answer_index
        
        # بروزرسانی و نمایش مجدد سوال با تیک کنار گزینه انتخاب شده
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
        await calculate_and_send_result(query.message, context)


def calculate_scores(user_answers):
    """امتیازات نهایی را بر اساس پاسخ‌ها محاسبه می‌کند."""
    scores = {"angel": 0, "human": 0, "demon": 0}
    for q_idx, a_idx in user_answers.items():
        selected_answer_scores = QUESTIONS[q_idx]["answers"][a_idx]["scores"]
        for race, score in selected_answer_scores.items():
            scores[race] += score
    return scores

async def calculate_and_send_result(message, context: ContextTypes.DEFAULT_TYPE):
    """نتیجه نهایی را محاسبه و ارسال می‌کند."""
    final_scores = calculate_scores(context.user_data['answers'])
    
    # پیدا کردن نژاد با بیشترین امتیاز
    # اولویت در صورت تساوی: فرشته > انسان > شیطان
    races_sorted = sorted(final_scores.items(), key=lambda item: (-item[1], ['angel', 'human', 'demon'].index(item[0])))
    result_race = races_sorted[0][0]

    race_names = {"angel": "فرشته 👼", "human": "انسان 👤", "demon": "شیطان 😈"}
    
    player_name = context.user_data.get('player_name', 'بازیکن')
    
    # ساخت متن نتیجه
    result_text = (
        f"خب {player_name}، آزمون تموم شد!\n\n"
        f"امتیازات شما:\n"
        f"👼 فرشته: {final_scores['angel']}\n"
        f"👤 انسان: {final_scores['human']}\n"
        f"😈 شیطان: {final_scores['demon']}\n\n"
        f"نتیجه نهایی: **شما یک {race_names[result_race]} هستید!**\n\n"
        f"بر اساس شخصیت شما، به گروه زیر دعوت می‌شوید:"
    )
    
    # ساخت دکمه‌های لینک
    keyboard = [
        [InlineKeyboardButton(f"ورود به گروه {race_names[result_race]}", url=GROUP_LINKS[result_race])],
        [InlineKeyboardButton("ورود به گپ اصلی", url=GROUP_LINKS["main"])]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
    # پاک کردن داده‌های کاربر برای آزمون بعدی
    context.user_data.clear()

async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیام‌های متنی را به تابع مناسب هدایت می‌کند."""
    if context.user_data.get('state') == 'awaiting_name':
        await name_handler(update, context)
    else:
        await update.message.reply_text("برای شروع آزمون جدید، دستور /start را ارسال کنید.")


# --- تابع اصلی برای اجرای ربات ---

def main():
    """ربات را اجرا می‌کند."""
    application = Application.builder().token(BOT_TOKEN).build()

    # تعریف دستورات
    application.add_handler(CommandHandler("start", start_command))
    
    # تعریف کنترل‌گر دکمه‌ها
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # تعریف کنترل‌گر پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))

    # اجرای ربات
    print("ربات در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()

