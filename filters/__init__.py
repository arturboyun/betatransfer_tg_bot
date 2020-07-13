from aiogram import Dispatcher


def setup(dispatcher: Dispatcher):
    from .is_owner import IsOwnerFilter
    dispatcher.filters_factory.bind(IsOwnerFilter)
