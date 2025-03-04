from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from app.database.requests import set_user, get_category, get_card_by_id


user = Router()

@user.callback_query(F.data == 'start')
@user.message(CommandStart())
async def cmd_start(event: Message | CallbackQuery):
    await set_user(event.from_user.id)
    if isinstance(event, Message):
        await event.answer('Добро пожаловать', reply_markup=kb.menu)
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.delete()
        await event.message.answer('Добро пожаловать', reply_markup=kb.menu)


@user.callback_query(F.data == 'catalog')
async def get_catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete() # удаляет с чата предыдущее сообщение
    await callback.message.answer_photo(photo='AgACAgIAAxkBAAMRZ8NHhvqbLMEr5aHqXYK17SF1lYsAAp3rMRueOBlKAAET'
                                              '-bBslr5uAQADAgADbQADNgQ', caption='Выберите категорию',
                                        reply_markup=await kb.categories())


@user.callback_query(F.data.startswith('cat_'))
async def get_cards(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    category_info = await get_category(category_id)
    await callback.answer()
    await callback.message.delete() # удаляет с чата предыдущее сообщение
    await callback.message.answer_photo(photo=category_info.image, caption=f'<b>{category_info.title}</b>\n\n'
                                                                           f'{category_info.about}',
                                        reply_markup=await kb.item_cards(category_id))


@user.callback_query(F.data.startswith('card_'))
async def get_card(callback: CallbackQuery):
    card = await get_card_by_id(callback.data.split('_')[1])
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(f'{card.title}\n\n{card.about}\n\nЦена:{card.price}$',reply_markup=await
    kb.add_to_cart(card))







@user.message(F.photo)
async def get_photo(message: Message):
    '''Хендлер для добавления фото в бд по айди
    кидаешь в бот картинку получаешь айди'''
    await message.answer(text=message.photo[-1].file_id)