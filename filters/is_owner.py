from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import config


@dataclass
class IsOwnerFilter(BoundFilter):
    key = "is_owner"

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id == config.OWNER_TELEGRAM_ID
