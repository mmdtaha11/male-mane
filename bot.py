# -*- coding: utf-8 -*-

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# اینها ایمپورت‌های نسخه ۲۰ هستند و درستند
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- تنظیمات اولیه ---
BOT_TOKEN = "7440922727:AAEMmpc3V-wvHDifg9uCV4h0mXxk_IqIqh4"
ADMIN_IDS = [5044871490, 5107444649]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- داده‌های سوالات و گروه‌ها (کد خودت - بدون تغییر) ---
QUESTIONS = [
    {
        "text": "🧩 سؤال ۱\n\nوقتی بین دو دوستت اختلاف پیش میاد، معمولاً چی‌کار می‌کنی؟",
        "answers": [
            {"text": "سعی می‌کنم هر دو طرف رو آروم کنم.", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "اول گوش می‌دم، بعد تصمیم می‌گیرم کدوم حق داره.", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "نمی‌خوام درگیر شم، ولی یادم می‌مونه کی باعث دردسر شد.", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "سعی می‌کنم کنترل موقعیت رو بگیرم تا دعوا تموم شه.", "scores": {"angel": 0, "human": 1, "demon": 1}},
            {"text": "کاری می‌کنم هر دو بفهمن که بی‌فایده بود بحث کنن.", "scores": {"angel": 1, "human": 1, "demon": 0}},
        ],
    },
    {
        "text": "🧩 سؤال ۲\n\nوقتی اشتباه بزرگی می‌کنی، اولین فکرت چیه؟",
        "answers": [
            {"text": "باید جبرانش کنم، حتی اگه سخته.", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "همه اشتباه می‌کنن، مهم اینه یاد بگیرم.", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "نباید بذارم کسی بفهمه.", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "دنیا ناعادله، ولی باید قوی‌تر شم.", "scores": {"angel": 0, "human": 1, "demon": 1}},
            {"text": "شاید این اشتباه دلیل خاصی داشته.", "scores": {"angel": 1, "human": 1, "demon": 0}},
        ],
    },
    # ... (بقیه سوالات حذف شدند تا کد کوتاه شود، تو از کد کامل خودت استفاده کن) ...
    {
        "text": "🧩 سؤال ۱۰\n\nوقتی باید بین نجات یک بی‌گناه و نجات هزار نفر تصمیم بگیری، چطور انتخاب می‌کنی؟",
        "answers": [
            {"text": "بی‌گناه رو نجات می‌دم، چون ارزش یک روح بی‌اندازه‌ست.", "scores": {"angel": 2, "human": 0, "demon": 0}},
            {"text": "هزار نفر، چون منطق مهم‌تر از احساسه.", "scores": {"angel": 0, "human": 2, "demon": 0}},
            {"text": "بستگی داره کدوم برام سود بیشتری داره.", "scores": {"angel": 0, "human": 0, "demon": 2}},
            {"text": "هیچ‌کدوم، چون هیچ انتخابی درست نیست.", "scores": {"angel": 0, "human": 1, "demon": 1}},
            {"text": "هر دو رو نجات می‌دم، حتی اگه ممکن نباشه.", "scores": {"angel": 1, "human": 1, "demon": 0}},
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

# --- توابع اصلی ربات (کد خودت - بدون تغییر) ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if 'result_race' in context.user_data:
        player_name = context.user_data.get('player_name', 'شما')
        result_race = context.user_data['result_race']
        
        if result_race == "human":
             result_text = (f"سلام {player_name}!\n"
                       f"شما قبلاً در آزمون شرکت کرده‌اید.\n\n"
                       f"نتیجه شما: **{race_names[result_race]}**\n\n"
                       f"می‌توانید وارد گپ اصلی شوید:")
             keyboard = [[InlineKeyboardButton("ورود به گپ اصلی", url=GROUP_LINKS["main"])]]
        else:
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
        # این خط از کد تو کار می‌کرد، پس درسته
        await context.bot.edit_message_text(chat_id=message.chat_id, message_id=message_id, text=question["text"], reply_markup=keyboard)
    else:
        await message.reply_text(question["text"], reply_markup=keyboard)

def calculate_scores(user_answers):
    scores = {"angel": 0, "human": 0, "demon": 0}
    for q_idx, a_idx in user_answers.items():
        selected_answer_scores = QUESTIONS[q_idx]["answers"][a_idx]["scores"]
        for race, score in selected_answer_scores.items():
            scores[race] += score
    return scores

async def calculate_and_send_result(message, context: ContextTypes.DEFAULT_TYPE, user):
    final_scores = calculate_scores(context.user_data['answers'])
    player_name = context.user_data.get('player_name', 'بازیکن')
    
    scores_for_user_result = {
        "angel": final_scores["angel"],
        "demon": final_scores["demon"]
    }
    
    user_races_sorted = sorted(scores_for_user_result.items(), 
                               key=lambda item: (-item[1], ['angel', 'demon'].index(item[0])))
    result_race = user_races_sorted[0][0]

    context.user_data['result_race'] = result_race
    
    result_text_user = (f"خب {player_name}، آزمون تموم شد!\n\n"
                       f"نتیجه نهایی: **شما یک {race_names[result_race]} هستید!**\n\n"
                       f"بر اساس شخصیت شما، به گروه زیر دعوت می‌شوید:")
    keyboard = [[InlineKeyboardButton(f"ورود به گروه {race_names[result_race]}", url=GROUP_LINKS[result_race])],
                [InlineKeyboardButton("ورود به گپ اصلی", url=GROUP_LINKS["main"])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(result_text_user, reply_markup=reply_markup, parse_mode='Markdown')

    if ADMIN_IDS:
        admin_report_text = (f"👤 گزارش تست جدید:\n\n"
                           f"نام بازیکن: {player_name}\n"
                           f"نام کاربری تلگرام: @{user.username or 'ندارد'}\n"
                           f"آیدی عددی: `{user.id}`\n\n"
                           f"نتیجه اعلام شده به کاربر: **{race_names[result_race]}** (بین 👼/😈)\n\n"
                           f"امتیازات کامل (برای بررسی ادمین):\n"
                           f"👼 فرشته: {final_scores['angel']}\n"
                           f"👤 انسان: {final_scores['human']}\n"
                           f"😈 شیطان: {final_scores['demon']}")
        
        result_data = {
            "user_id": user.id,
            "player_name": player_name,
            "username": user.username or 'ندارد',
            "result_race_user": result_race,
            "final_scores": final_scores,
            "report_text": admin_report_text
        }

        if 'structured_results' not in context.bot_data:
            context.bot_data['structured_results'] = {}
        
        context.bot_data['structured_results'][user.id] = result_data

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

# --- بخش پنل ادمین (کد خودت - بدون تغییر) ---

def get_admin_panel_keyboard(context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    all_results_data = context.bot_data.get('structured_results', {})
    if not all_results_data:
        return None

    sorted_users = sorted(all_results_data.values(), key=lambda x: x['player_name'])
    
    for user_data in sorted_users:
        user_id = user_data['user_id']
        player_name = user_data['player_name']
        username = user_data['username']
        button_text = f"{player_name} (@{username})"
        callback_data = f"admin_show_{user_id}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    return InlineKeyboardMarkup(keyboard)

async def admin_panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ شما اجازه دسترسی به این دستور را ندارید.")
        return

    keyboard = get_admin_panel_keyboard(context)
    
    if not keyboard:
        await update.message.reply_text("هنوز هیچ نتیجه‌ای در ربات ثبت نشده است.")
        return
    
    # --- ✨ تعمیر: حذف parse_mode از اینجا ---
    await update.message.reply_text("بخش مدیریت ادمین:\n\n" # متن دیگر بولد نیست
                                   "لطفاً کاربری را برای مشاهده نتیجه (جداگانه) انتخاب کنید:", 
                                   reply_markup=keyboard
                                   # parse_mode='Markdown' <-- حذف شد
                                   )

# --- ✨✨✨ تابع دکمه‌ها (کد خودت + تعمیر نهایی) ✨✨✨
async def global_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    
    data = query.data.split('_')
    action_group = data[0] 

    # --- بخش آزمون (کد خودت - بدون تغییر) ---
    if action_group == "ans":
        question_index = int(data[1])
        answer_index = int(data[2])
        context.user_data['answers'][question_index] = answer_index
        await send_question(query.message, context, message_id=query.message.message_id)
        
    elif action_group == "nav":
        direction = data[1]
        current_index = int(data[2])
        if direction == "next":
            context.user_data['current_question'] = current_index + 1
        elif direction == "prev":
            context.user_data['current_question'] = current_index - 1
        await send_question(query.message, context, message_id=query.message.message_id)
        
    elif action_group == "finish":
        await calculate_and_send_result(query.message, context, update.effective_user)
        
    # --- بخش ادمین (تعمیر شده با حذف parse_mode) ---
    elif action_group == "admin":
        user_id = query.effective_user.id
        if user_id not in ADMIN_IDS:
            await query.answer("❌ دسترسی غیرمجاز.", show_alert=True)
            return

        action_type = data[1] 
        
        if action_type == "show":
            try:
                target_user_id = int(data[2])
                all_results_data = context.bot_data.get('structured_results', {})
                target_data = all_results_data.get(target_user_id)
                
                if not target_data:
                    await context.bot.edit_message_text(
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text="خطا: اطلاعات این کاربر یافت نشد."
                    )
                    return
                
                # گزارش را بدون مارک‌داون می‌خوانیم که متن بولد نداشته باشد
                report_text = target_data.get('report_text', "گزارشی یافت نشد.")
                keyboard = [[InlineKeyboardButton("⬅️ بازگشت به لیست", callback_data="admin_back_list")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                # --- ✨ تعمیر ۱: استفاده از context.bot و حذف parse_mode ---
                await context.bot.edit_message_text(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text=report_text, 
                    reply_markup=reply_markup 
                    # parse_mode='Markdown'  <--- عامل کرش حذف شد
                )
            
            except Exception as e:
                logger.warning(f"Failed to edit message for admin panel: {e}")
                # --- fallback ساده بدون parse_mode ---
                await query.message.reply_text(text=report_text, reply_markup=reply_markup)

        elif action_type == "back": 
            keyboard = get_admin_panel_keyboard(context)
            if not keyboard:
                await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="هنوز هیچ نتیجه‌ای ثبت نشده است.")
                return
            
            # --- ✨ تعمیر ۲: استفاده از context.bot و حذف parse_mode ---
            await context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="بخش مدیریت ادمین:\n\n" # متن دیگر بولد نیست
                     "لطفاً کاربری را برای مشاهده نتیجه انتخاب کنید:", 
                reply_markup=keyboard
                # parse_mode='Markdown'  <--- عامل کرش حذف شد
            )
# --- ✨✨✨ پایان تعمیرات ---


def main():
    # این ساختار (Application.builder) کد نسخه ۲۰ است و درست است
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("admin", admin_panel_command))
    
    # --- استفاده از همان ساختار سالم کد خودت ---
    application.add_handler(CallbackQueryHandler(global_button_handler))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))
    
    print("ربات (نسخه نهایی تعمیر شده - حذف parse_mode) در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()
