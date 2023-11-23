Token = "6889649357:AAHu1XmHalCpvZYSqQRfVstmWXXIhjQcR7s"

import os
import telebot
import subprocess
import shutil

# Source path (current location of the file/directory)
source_path = r'C:\Users\Johan Sebastian Cuel\Downloads\bot_yolo\yolov5\runs\detect\exp'
# Destination path (where you want to move the file/directory)
destination_path = r'C:\Users\Johan Sebastian Cuel\Downloads\bot_yolo\image'
PHOTO_PATH = r'C:\Users\Johan Sebastian Cuel\Downloads\bot_yolo\image\exp\image.jpg'
CHAT_id  = 1126497289
bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

#@bot.message_handler(func=lambda msg: True)
#def echo_all(message):
#    bot.reply_to(message, message.text)

@bot.message_handler(commands=['foto', 'photo'])
def send_foto(message):
    bot.send_photo(chat_id=message.chat.id, photo=open(PHOTO_PATH, 'rb'))

@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    # Eject script in system
    #subprocess.run(r'python C:\Users\Johan Sebastian Cuel\Downloads\bot_yolo\yolov5\detect.py --weights C:\Users\Johan Sebastian Cuel\Downloads\bot_yolo\yolov5\runs\train\yolov5s_results\weights\best.pt --img 512 --conf 0.4 --source C:\Users\Johan Sebastian Cuel\Downloads\bot_yolo\image.jpg')

    subprocess.run(r'python yolov5\detect.py --weights yolov5\runs\train\yolov5s_results\weights\best.pt --img 512 --conf 0.4 --source image.jpg')
    # Move the file/directory
    shutil.move(source_path, destination_path)
    # bot send photo
    bot.send_photo(chat_id=message.chat.id, photo=open(PHOTO_PATH, 'rb'))
    # Delete the file/directory
    shutil.rmtree(destination_path+r'\exp')

#bot.send_message(chat_id=CHAT_id, text="the door")

bot.infinity_polling()