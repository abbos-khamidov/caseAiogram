import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = '8422643227:AAFppSmJFxxW1JA36YJGs91uSuuv6Xtv6nY'
bot = Bot(token=TOKEN)
dp = Dispatcher()


products = [
    {
        'name': 'Nike Air',
        'description': 'Good sneakers for running',
        'price': 120,
        'photo': 'https://m.media-amazon.com/images/I/71Ru+PAVZCL._AC_SL1000__.jpg'
    },
    {
        'name': 'Adidas Pro',
        'description': 'Famous sneakers for street',
        'price': 120,
        'photo': 'https://www.misterrunning.com/images/2025-media-02/adidas-adizero-adios-pro-4-scarpe-da-running-uomo-cloud-white-jr1094-A.jpg'
    },
    {
        'name': 'Puma Street',
        'description': 'Best choice for runners and who loves puma',
        'price': 210,
        'photo': 'https://cdn.afew-store.com/assets/48/487132/2400/puma-h-street-og-white-403692-05-footwear%20%3E%20sneaker-packshots-0.jpg'
    }
]


user_positions = {}
user_cart = {}

def product_keyboard(index: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Prev', callback_data='prev'),
        InlineKeyboardButton(text='Next', callback_data='next'),
    )
    builder.row(
        InlineKeyboardButton(text='To cart', callback_data='add')
    )
    return builder.as_markup()

def product_caption(index: int):
    product = products[index]
    return (
        f'{product['name']}\n'
        f'{product['description']}\n'
        f'${product['price']}\n'
        f'\nProduct {index + 1} from {len(products)}'
    )

@dp.message(CommandStart())
async def start_handler(message: Message):
    user_positions[message.from_user.id] = 0
    index = 0
    await message.answer_photo(
        photo = products[index]['photo'],
        caption=product_caption(index),
        reply_markup=product_keyboard(index)
    )

@dp.callback_query(F.data.in_(['next', 'prev']))
async def navigate_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    index = user_positions.get(user_id, 0)

    if callback.data == 'next':
        index = (index + 1) % len(products)
    else:
        index = (index - 1) % len(products)

    user_positions[user_id] = index

    await callback.message.edit_media(
        media = {
            'type': 'photo',
            'media': products[index]['photo'],
            'caption': product_caption(index),
        },
        reply_markup=product_keyboard(index)
    )

    await callback.answer()

@dp.callback_query(F.data == 'add')
async def add_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    index = user_positions.get(user_id, 0)

    user_cart.setdefault(user_id, [])
    user_cart[user_id].append(products[index])

    await callback.answer('Added to cart', show_alert=False)


@dp.message(F.text == 'Cart')
async def cart_handler(message: Message):
    cart = user_cart.get(message.from_user.id, [])

    if not cart:
        await message.answer('Cart is empty')
        return
    
    total = sum(item['price'] for item in cart)
    text = 'Your cart:\n\n'
    for i, item in enumerate(cart, 1):
        text += f'{i}. {item['name']} - ${item['price']}\n'
    text += f'All in: {total}'

    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())