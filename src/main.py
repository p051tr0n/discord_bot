import config
from app.bot import BotClient

config._prepare_config()

if __name__ == '__main__':
    bot = BotClient()
    bot.start()