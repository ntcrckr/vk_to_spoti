import telebot
from vk_to_spotify import VkToSpotify

API_TOKEN = "1803983650:AAGCE8Cb00TAkcFzmTk5t0HALw_N0XOZ0DM"

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am vk_to_spotify_bot.\
""")


@bot.message_handler(commands=["work"])
def ask_for_data(message):
    msg = bot.reply_to(message, """\
Send me the url for vk group.\
""")
    bot.register_next_step_handler(msg, get_vk_url)


def get_vk_url(message):
    vk_group_url = message.text
    msg = bot.reply_to(message, """\
Send me the name for playlist.\
""")
    bot.register_next_step_handler(msg, work, vk_group_url)


def work(message, vk_group_url):
    playlist_name = message.text
    bot.reply_to(message, """\
Processing.\
""")
    vk_to_spoti = VkToSpotify(
        vk_group_url=vk_group_url,
        playlist_name=playlist_name,
        playlist_description=f"Playlist made by emo vk fetcher bot. Songs fetched from {vk_group_url}"
    )
    vk_to_spoti.work()
    bot.reply_to(message, """\
Finished.\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling()