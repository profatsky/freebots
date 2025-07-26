import os
from collections.abc import Mapping

from aiogram import types, filters, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import config
from db.catalog import get_products, add_product, delete_product
from loader import db_connector, bot

router = Router()


class CatalogState(StatesGroup):
    show_product = State()


button_next = types.InlineKeyboardButton(text="Вперед ▶", callback_data="next_product")
button_back = types.InlineKeyboardButton(text="◀ Назад", callback_data="prev_product")
button_delete = types.InlineKeyboardButton(text="❌ Удалить", callback_data="delete_product")


@router.message(filters.StateFilter(None), filters.Command("catalog"))
async def get_catalog(
        message: types.Message,
        state: FSMContext,
        counter: int = 0,
        products: list[Mapping] = None,
        sent_message: types.Message = None,
        is_admin: bool = False,
):
    if products is None:
        products = await get_products(db_connector)

    if not products:
        if state:
            await state.clear()
        if sent_message:
            await bot.delete_message(
                chat_id=sent_message.chat.id,
                message_id=sent_message.message_id,
            )
        return await message.answer('☹ Нет доступных товаров')

    if not is_admin and message.from_user.id == int(config.ADMIN_ID):
        is_admin = True

    buttons = []
    jump_buttons_row = []
    if counter > 0:
        jump_buttons_row.append(button_back)
    if len(products) - (counter + 1) > 0:
        jump_buttons_row.append(button_next)

    if jump_buttons_row:
        buttons.append(jump_buttons_row)

    if is_admin:
        buttons.append([button_delete])

    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None

    product = products[counter]
    image = types.FSInputFile(product["image_path"])

    caption = (
        f"<b>{product['name']}</b>\n\n"
        f"{product['description']}\n\n"
        f"Цена: <i>{product['price']}</i>\n\n"
        f"Обращаться к {product['seller_username']}"
    )

    if sent_message is None:
        sent_message = await message.answer_photo(
            photo=image,
            caption=caption,
            reply_markup=kb
        )
    else:
        sent_message = await bot.edit_message_media(
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id,
            media=types.InputMediaPhoto(media=image.filename.rsplit('.')[0], caption=caption),
            reply_markup=kb,
        )

    await state.set_state(CatalogState.show_product)
    await state.update_data(
        products=products,
        counter=counter,
        sent_message=sent_message,
        is_admin=is_admin,
    )


@router.callback_query(filters.StateFilter(CatalogState.show_product))
async def catalog_operation(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()

    if callback.data == "next_product":
        await get_catalog(
            message=callback.message,
            state=state,
            counter=data["counter"] + 1,
            products=data["products"],
            sent_message=data["sent_message"],
            is_admin=data["is_admin"]
        )
    elif callback.data == "prev_product":
        await get_catalog(
            message=callback.message,
            state=state,
            counter=data["counter"] - 1,
            products=data["products"],
            sent_message=data["sent_message"],
            is_admin=data["is_admin"]
        )
    elif callback.data == "delete_product":
        current_product = data["products"].pop(data["counter"])
        await delete_product(db_connector, current_product["name"])
        await callback.message.answer('✅ Товар успешно удален!')
        await get_catalog(
            message=callback.message,
            state=state,
            counter=0,
            products=data["products"],
            sent_message=data["sent_message"],
            is_admin=data["is_admin"]
        )


@router.message(filters.StateFilter(CatalogState.show_product))
async def exit_catalog(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(
        chat_id=data["sent_message"].chat.id,
        message_id=data["sent_message"].message_id,
    )
    await state.clear()
    await message.answer('❎ Каталог закрыт. Теперь вы можете отправлять любые сообщения!')


start_keyboard_buttons = [
    [
        types.InlineKeyboardButton(text="Начать", callback_data="start_add_product"),
    ]
]
start_keyboard = types.InlineKeyboardMarkup(inline_keyboard=start_keyboard_buttons)


class AddProductState(StatesGroup):
    specify_name = State()
    specify_description = State()
    specify_price = State()
    specify_image = State()
    specify_seller_username = State()


@router.message(filters.StateFilter(None), filters.Command("add_product"))
async def add_product_command(message: types.Message):
    if message.from_user.id == int(config.ADMIN_ID):
        await message.answer(
            "❗ Для добавления товара необходимо предоставить следующие данные о нем:\n\n"
            "- ✏ Название\n\n"
            "- 📑 Описание\n\n"
            "- 💵 Стоимость\n\n"
            "- 🖼 Изображение\n\n"
            "- 👤 Username продавца в Telegram",
            reply_markup=start_keyboard,
        )


@router.callback_query(filters.StateFilter(None), F.data == "start_add_product")
async def start_add_product(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('✏ Укажите название товара')
    await state.set_state(AddProductState.specify_name)


@router.message(filters.StateFilter(AddProductState.specify_name))
async def specify_product_name(message: types.Message, state: FSMContext):
    if message.text is None:
        return await message.answer('❗ Необходимо отправить текстовое сообщение!')

    await state.update_data(name=message.text)

    await message.answer('📑 Укажите описание товара')
    await state.set_state(AddProductState.specify_description)


@router.message(filters.StateFilter(AddProductState.specify_description))
async def specify_product_description(message: types.Message, state: FSMContext):
    if message.text is None:
        return await message.answer('❗ Необходимо отправить текстовое сообщение!')

    await state.update_data(description=message.text)

    await message.answer('💵 Укажите стоимость товара\n\n'
                         '<i>Разрешается вводить не только числа, но и текст</i>')
    await state.set_state(AddProductState.specify_price)


@router.message(filters.StateFilter(AddProductState.specify_price))
async def specify_product_price(message: types.Message, state: FSMContext):
    if message.text is None:
        return await message.answer('❗ Необходимо отправить текстовое сообщение!')

    await state.update_data(price=message.text)

    await message.answer('🖼 Загрузите изображение товара')
    await state.set_state(AddProductState.specify_image)


@router.message(filters.StateFilter(AddProductState.specify_image))
async def specify_product_image(message: types.Message, state: FSMContext):
    if not message.photo:
        return await message.answer('❗ Необходимо отправить изображение!')

    image_path = os.path.join("img", f"{message.photo[-1].file_id}.jpg")

    await bot.download(
        message.photo[-1],
        destination=image_path
    )

    await state.update_data(image_path=image_path)
    await message.answer('👤 Укажите username продавца в Telegram\n\n'
                         '<i>Username начинается с символа @</i>')
    await state.set_state(AddProductState.specify_seller_username)


@router.message(filters.StateFilter(AddProductState.specify_seller_username))
async def specify_seller_username(message: types.Message, state: FSMContext):
    if message.text is None:
        return await message.answer('❗ Необходимо отправить текстовое сообщение!')

    if not message.text.startswith('@'):
        return await message.answer('❗ Username продавца должен начинаться с @!')

    await state.update_data(seller_username=message.text)

    data = await state.get_data()

    await add_product(
        db_connector=db_connector,
        name=data["name"],
        description=data["description"],
        price=data["price"],
        image_path=data["image_path"],
        seller_username=data["seller_username"]
    )
    await state.clear()
    await message.answer("✅ Товар успешно добавлен!")

    image = types.FSInputFile(data["image_path"])

    await message.answer_photo(
        photo=image,
        caption=f"<b>{data['name']}</b>\n\n"
                f"{data['description']}\n\n"
                f"Цена: <i>{data['price']}</i>\n\n"
                f"Обращаться к {data['seller_username']}"
    )
