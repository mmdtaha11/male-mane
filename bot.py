# -*- coding: utf-8 -*-

import logging
import random # این کتابخانه برای بُر زدن گزینه‌ها اضافه شد
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- تنظیمات اولیه ---
# ⚠️ توکن ربات خود را در اینجا قرار دهید
BOT_TOKEN = "7440922727:AAEMmpc3V-wvHDifg9uCV4h0mXxk_IqIqh4"
# ⚠️ آیدی عددی ادمین‌ها را در اینجا قرار دهید
ADMIN_IDS = [5044871490, 5107444649]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- داده‌های سوالات و گروه‌ها ---
# ✨✨✨ بخش سوالات با محتوای جدید شما جایگزین شد ✨✨✨
QUESTIONS = [
    {
        "text": "🧩 سؤال ۱\n\nوقتی بین دو دوستت اختلاف پیش میاد، معمولاً چی‌کار می‌کنی؟",
        "answers": [
            {"text": "سعی می‌کنم هر دو طرف رو آروم کنم.", "scores": {"angel": 2}},
            {"text": "اول گوش می‌دم، بعد تصمیم می‌گیرم کدوم حق داره.", "scores": {"human": 2}},
            {"text": "نمی‌خوام درگیر شم، ولی یادم می‌مونه کی باعث دردسر شد.", "scores": {"demon": 2}},
            {"text": "سعی می‌کنم کنترل موقعیت رو بگیرم تا دعوا تموم شه.", "scores": {"demon": 1, "human": 1}},
            {"text": "کاری می‌کنم هر دو بفهمن که بی‌فایده بود بحث کنن.", "scores": {"human": 1, "angel": 1}},
        ],
    },
    {
        "text": "🧩 سؤال ۲\n\nوقتی اشتباه بزرگی می‌کنی، اولین فکرت چیه؟",
        "answers": [
            {"text": "باید جبرانش کنم، حتی اگه سخته.", "scores": {"angel": 2}},
            {"text": "همه اشتباه می‌کنن، مهم اینه یاد بگیرم.", "scores": {"human": 2}},
            {"text": "نباید بذارم کسی بفهمه.", "scores": {"demon": 2}},
            {"text": "دنیا ناعادله، ولی باید قوی‌تر شم.", "scores": {"demon": 1, "human": 1}},
            {"text": "شاید این اشتباه دلیل خاصی داشته.", "scores": {"angel": 1, "human": 1}},
        ],
    },
    {
        "text": "🧩 سؤال ۳\n\nتو خلوتت بیشتر به چی فکر می‌کنی؟",
        "answers": [
            {"text": "آینده‌ای بهتر برای همه.", "scores": {"angel": 2}},
            {"text": "راهی برای پیشرفت خودم.", "scores": {"human": 2}},
            {"text": "اینکه چه‌طور میشه دیگران رو درک کرد.", "scores": {"angel": 1, "human": 1}},
            {"text": "کنترل و قدرتی که هنوز ندارم.", "scores": {"demon": 2}},
            {"text": "اینکه دنیا چرا این‌قدر بی‌نظم و بی‌رحمه.", "scores": {"demon": 1, "human": 1}},
        ],
    },
    {
        "text": "🧩 سؤال ۴\n\nوقتی یه نفر ناامید و خسته‌ست، چطور رفتار می‌کنی؟",
        "answers": [
            {"text": "باهاش حرف می‌زنم تا حس بهتری پیدا کنه.", "scores": {"angel": 2}},
            {"text": "بهش یادآوری می‌کنم که خودش باید قوی بمونه.", "scores": {"human": 2}},
            {"text": "اگه خودش خواست، کمکش می‌کنم.", "scores": {"human": 1, "angel": 1}},
            {"text": "سکوت می‌کنم؛ بعضی چیزا نیاز به حرف ندارن.", "scores": {"human": 1, "demon": 1}},
            {"text": "می‌ذارم خودش تا ته سقوط بره، چون فقط اونطوری رشد می‌کنه.", "scores": {"demon": 2}},
        ],
    },
    {
        "text": "🧩 سؤال ۵\n\nکدوم جمله بیشتر شبیه طرز فکرت هست؟",
        "answers": [
            {"text": "نور همیشه در تاریکی هم راهی پیدا می‌کنه.", "scores": {"angel": 2}},
            {"text": "هیچ چیز مطلق نیست؛ فقط انتخاب‌ها مهمن.", "scores": {"human": 2}},
            {"text": "قدرت یعنی آزادی.", "scores": {"demon": 2}},
            {"text": "همه‌چیز بهایی داره، حتی خوبی.", "scores": {"demon": 1, "human": 1}},
            {"text": "عدالت بدون احساس، بی‌ارزشه.", "scores": {"angel": 1, "human": 1}},
        ],
    },
    {
        "text": "🧩 سؤال ۶\n\nوقتی یه نفر بی‌دلیل ازت متنفره، چه واک-نشون می‌دی؟",
        "answers": [
            {"text": "سعی می‌کنم دلیلش رو بفهمم.", "scores": {"angel": 2}},
            {"text": "برام مهم نیست، هرکس نظر خودش رو داره.", "scores": {"human": 2}},
            {"text": "ازش استفاده می‌کنم تا قوی‌تر شم.", "scores": {"demon": 2}},
            {"text": "فقط لبخند می‌زنم — نفرتش خودش رو می‌سوزونه.", "scores": {"angel": 1, "demon": 1}},
            {"text": "بهش نشون می‌دم که اشتباه کرده.", "scores": {"human": 1, "demon": 1}},
        ],
    },
    {
        "text": "🧩 سؤال ۷\n\nدر انتخاب بین «آرامش» و «قدرت»، کدوم رو ترجیح می‌دی؟",
        "answers": [
            {"text": "آرامش، چون بدونش هیچ ارزشی نیست.", "scores": {"angel": 2}},
            {"text": "قدرت، چون باهاش میشه از آرامش محافظت کرد.", "scores": {"human": 2}},
            {"text": "هیچ‌کدوم مطلق نیست، باید بینش تعادل ساخت.", "scores": {"human": 1, "angel": 1}},
            {"text": "قدرت، چون فقط قوی‌ها زنده می‌مونن.", "scores": {"demon": 2}},
            {"text": "آرامش، اما نه به قیمت سکوت در برابر ظلم.", "scores": {"angel": 1, "demon": 1}},
        ],
    },
    {
        "text": "🧩 سؤال ۸\n\nوقتی همه علیه تو هستن، چطور ادامه می‌دی؟",
        "answers": [
            {"text": "با ایمان به خودم پیش می‌رم.", "scores": {"angel": 2}},
            {"text": "با منطق و صبر منتظر فرصت می‌مونم.", "scores": {"human": 2}},
            {"text": "با هر وسیله‌ای که دارم مقابله می‌کنم.", "scores": {"demon": 2}},
            {"text": "ساکت می‌مونم و اجازه می‌دم زمان قضاوت کنه.", "scores": {"angel": 1, "human": 1}},
            {"text": "می‌خندم، چون این یعنی خطرناک شدم.", "scores": {"demon": 1, "human": 1}},
        ],
    },
    {
        "text": "🧩 سؤال ۹\n\nکدوم حس بیشتر درونت غالب‌تره؟",
        "answers": [
            {"text": "همدلی.", "scores": {"angel": 2}},
            {"text": "کنجکاوی.", "scores": {"human": 2}},
            {"text": "جاه‌طلبی.", "scores": {"demon": 2}},
            {"text": "بی‌اعتمادی.", "scores": {"demon": 1, "human": 1}},
            {"text": "نظم و کنترل.", "scores": {"human": 1, "angel": 1}},
        ],
    },
    {
        "text": "🧩 سؤال ۱۰\n\nوقتی باید بین نجات یک بی‌گناه و نجات هزار نفر تصمیم بگیری، چطور انتخاب می‌کنی؟",
        "answers": [
            {"text": "بی‌گناه رو نجات می‌دم، چون ارزش یک روح بی‌اندازه‌ست.", "scores": {"angel": 2}},
            {"text": "هزار نفر، چون منطق مهم‌تر از احساسه.", "scores": {"human": 2}},
            {"text": "بستگی داره کدوم برام سود بیشتری داره.", "scores": {"demon": 2}},
            {"text": "هیچ‌کدوم، چون هیچ انتخابی درست نیست.", "scores": {"human": 1, "demon": 1}},
            {"text": "هر دو رو نجات می‌دم، حتی اگه ممکن نباشه.", "scores": {"angel": 1, "human": 1}},
        ],
    },
]

# ⚠️ لینک گروه‌های خود را در اینجا قرار دهید
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

def build_question_keyboard(question_index, user_answers):
    """دکمه‌های گزینه‌ها را به صورت نامرتب و دکمه‌های ناوبری را می‌سازد."""
    keyboard = []
    question = QUESTIONS[question_index]
    
    indexed_answers = list(enumerate(question["answers"]))
    random.shuffle(indexed_answers)
    
    for original_index, answer in indexed_answers:
        prefix = "✅ " if user_answers.get(question_index) == original_index else ""
        button = InlineKeyboardButton(f'{prefix}{answer["text"]}', callback_data=f"ans_{question_index}_{original_index}")
        keyboard.append([button])
        
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
        selected_answer_scores = QUESTIONS[q_idx]["answers"][a_idx].get("scores", {})
        for race, score in selected_answer_scores.items():
            if race in scores:
                scores[race] += score
    return scores

# --- ⚠️ این تابع تغییر کرده است ⚠️ ---
async def calculate_and_send_result(message, context: ContextTypes.DEFAULT_TYPE, user):
    final_scores = calculate_scores(context.user_data['answers'])
    
    # --- ✨ تغییر جدید: منطق حذف شیطان حذف شد و اکنون به درستی محاسبه می‌شود ---
    # final_scores['demon'] = -1  <- این خط حذف شد

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
        # --- ✨ تغییر جدید: گزارش ادمین اصلاح شد ---
        admin_report_text = (f"👤 گزارش تست جدید:\n\n"
                           f"نام بازیکن: {player_name}\n"
                           f"نام کاربری تلگرام: @{user.username or 'ندارد'}\n"
                           f"آیدی عددی: `{user.id}`\n\n"
                           f"نتیجه تست: **{race_names[result_race]}**\n\n"
                           f"امتیازات:\n"
                           f"👼 فرشته: {final_scores['angel']}\n"
                           f"👤 انسان: {final_scores['human']}\n"
                           f"😈 شیطان: {final_scores['demon']}") # امتیاز شیطان اکنون به درستی گزارش می‌شود
        
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

async def get_results_command(update: Update, context: ContextTypes.DEFAULT_T-YPE):
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
