from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler,filters
from encode import create_qrcode
from encode import read_qrcode
from PIL import Image
import io

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message.photo:
        photo = message.photo[-1]
        file = await photo.get_file()
        photo_bytes = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(photo_bytes))
        result = read_qrcode(img)
        if result:
            await message.reply_text(result[0][0].decode('utf-8'))
        else:
            await message.reply_text('未找到二维码，请发送包含二维码的图片')
    else:
        await message.reply_text('请发送包含二维码的图片')



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="输入/encode+需要转二维码的文字或者链接以进行转码\n比如:\n/encode 需要转码的内容\n或者直接在对话框中发送二维码图片进行解码")

async def encode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = context.args[0]
    file = create_qrcode(data)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)


app = ApplicationBuilder().token("6154192211:AAGBR4yF5AtcZbh-A8dLWMe9JQhYIx5BkLQ").build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("encode", encode))

app.add_handler(MessageHandler(filters.ALL, handle_message))

app.run_polling()