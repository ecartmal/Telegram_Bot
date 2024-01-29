from telegram import Update
from telegram.ext import (
    Updater,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
)

import os

def unknown(update, context):
    update.message.reply_text("Xin lỗi, tôi không biết bạn đang cần gì?")

def invalid(update, context):
    update.message.reply_text("Oh, Có vẻ như yêu cầu không hợp lệ!")
    return ConversationHandler.END

def about(update, context):
    update.message.reply_text(
        """Link CTF: http://sacomctf.ecartmal.site:8843/
 Domain Chính: ecartmal.site
 Github: https://github.com/ecartmal"""
    )

def text2voice(update, context):
    update.message.reply_text("Okay, gửi tôi đoạn văn bản nhé.")
    return 0

def send_voice_msg(update, context):
    text = update.message.text
    fs = open(f"/home/ctf/{update.message.from_user.id}", "w")
    fs.write(f"echo '{text}'")
    fs.close()
    os.system(
        f"su ctf -c 'sh /home/ctf/{update.message.from_user.id} | espeak -w /home/ctf/{update.message.from_user.id}.wav --stdin'"
    )
    update.message.reply_audio(
        open(f"/home/ctf/{update.message.from_user.id}.wav", "rb")
    )
    os.system(
        f"rm /home/ctf/{update.message.from_user.id}; rm /home/ctf/{update.message.from_user.id}.wav"
    )
    return ConversationHandler.END

def start(update, context):
    update.message.reply_text(
        """Available Commands:
/start
/help
/text2voice
/about
/flag"""
    )

def handle_flag_command(update, context):
    update.message.reply_text("Làm gì có flag mà cho!")

def main():
    unknown_handler = MessageHandler(Filters.all, unknown)
    about_handler = CommandHandler("about", about)
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", start)
    text2voice_states = {0: [MessageHandler(Filters.text, send_voice_msg)]}
    text2voice_handler = ConversationHandler(
        entry_points=[CommandHandler("text2voice", text2voice)],
        states=text2voice_states,
        fallbacks=[MessageHandler(Filters.all, invalid)],
    )

    # Khởi tạo bot và thêm handlers
    token = "6942919730:AAEE2wu0DxfEKbqSkTw3dsuVJVj7AMIH3qk"
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(about_handler)
    dispatcher.add_handler(text2voice_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(unknown_handler)

    # Thêm handler cho lệnh /flag
    flag_handler = CommandHandler("flag", handle_flag_command)
    dispatcher.add_handler(flag_handler)

    # Khởi động bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
