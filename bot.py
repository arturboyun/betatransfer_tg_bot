import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import CommandStart, Text
from prettytable import PrettyTable

import config

# Configure logging
import filters
from api import API, StatusCodes, TransTypes
from filters.is_owner import IsOwnerFilter

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s',
    datefmt='%d-%m-%yy %H:%M:%S'
)

logger = logging.getLogger(__name__)


# Initialize bot, dispatcher and api
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
api = API(config.API_TOKEN_PUBLIC, config.API_TOKEN_PRIVATE)


# Setup filters
filters.setup(dp)


async def generate_table(th, td):
    table = PrettyTable(th)
    columns = len(th)
    td_data = td[:]
    while td_data:
        table.add_row(td_data[:columns])
        td_data = td_data[columns:]
    return table


async def menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Аккаунт')
    markup.row('Последние 5 платежей', '✅Последние 5 платежей')
    markup.row('Последние 10 платежей', '✅Последние 10 платежей')
    markup.row('Последние 25 платежей', '✅Последние 25 платежей')
    markup.row('Последние 50 платежей', '✅Последние 50 платежей')
    markup.row('Последние 75 платежей', '✅Последние 75 платежей')
    return markup


@dp.message_handler(CommandStart(), IsOwnerFilter())
async def _(message: types.Message):
    markup = await menu_markup()
    await message.answer(f'Welcome {message.from_user.full_name}', reply_markup=markup)


@dp.message_handler(Text(contains=['Аккаунт']), IsOwnerFilter())
async def _(message: types.Message):
    account_info = await api.get_account_info()
    lock_withdraw_text = 'Да' if account_info.lock_withdrawal != 0 else 'Нет'
    lock_account_text = 'Да' if account_info.lock_account != 0 else 'Нет'
    text = [
        '<b>Аккаунт</b>', '',
        '<b>Баланс:</b>',
        f'RUB: {account_info.balance_rub}',
        f'USD: {account_info.balance_usd}',
        f'UAH: {account_info.balance_uah}', '',
        '<b>Задержка баланса:</b>',
        f'RUB: {account_info.balance_on_hold_rub}',
        f'USD: {account_info.balance_on_hold_usd}',
        f'UAH: {account_info.balance_on_hold_uah}', '',
        '<b>Доп. инфо:</b>',
        f'Блокировка вывода: {lock_withdraw_text}',
        f'Блокировка аккаунта: {lock_account_text}'
    ]
    await message.answer('\n'.join(text))


@dp.message_handler(Text(contains=['Последние']), IsOwnerFilter())
async def _(message: types.Message):
    text = f'<b>{message.text}</b>\n'
    markup = await menu_markup()
    try:
        limit = int(message.text.split(' ')[1])
        status = None

        if message.text.startswith('✅'):
            status = StatusCodes.SUCCESS

        td = []
        th = ['', 'id', 'amount', 'currency', 'status', 'type']
        transactions = await api.get_transactions_history(limit=limit, status=status)

        for i, transaction in enumerate(transactions, 1):
            td.extend([i, transaction.id, transaction.amount, transaction.currency, transaction.status, transaction.type])

        table = await generate_table(th, td)
        text += f'<code>{table}</code>'
        await message.answer(text, reply_markup=markup)
        logger.info(f'{message.from_user.full_name} ({message.from_user.username or message.from_user.id}) '
                    f'success get {message.text}')
    except Exception as e:
        logger.info(f'{message.from_user.full_name} ({message.from_user.username or message.from_user.id}) '
                    f'ERROR with get {message.text}')
        logger.error(f'Error: {e}')
        await message.answer('<b>Что-то пошло не так🤷‍♂</b>', reply_markup=markup)


@dp.message_handler(IsOwnerFilter)
async def echo(message: types.Message):
    await message.answer(f'{message.text} from owner.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
