from envparse import env

env.read_envfile()

BOT_TOKEN = env.str('BOT_TOKEN')
OWNER_TELEGRAM_ID = env.int('OWNER_TELEGRAM_ID')
API_TOKEN_PUBLIC = env.str('API_TOKEN_PUBLIC')
API_TOKEN_PRIVATE = env.str('API_TOKEN_PRIVATE')
