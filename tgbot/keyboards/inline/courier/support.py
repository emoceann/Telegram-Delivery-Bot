import random

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.manager.callback_data import support_callback, cancel_support_callback


async def check_support_available(support_id, state: FSMContext):
    state = await state.storage.get_data(chat=support_id, user=support_id)
    # state_str =
    if str(state) == "in_support":
        return
    else:
        return support_id


async def get_support_manager(state: FSMContext):
    support_ids = [1722307137, 418609567]  # @TODO записать всех менеджеров в бд
    random.shuffle(support_ids)
    for support_id in support_ids:
        # Проверим если оператор в данное время не занят
        support_id = await check_support_available(support_id, state=state)

        # Если такого нашли, что выводим
        if support_id:
            return support_id
    else:
        return


async def support_keyboard(messages, state: FSMContext, user_id=None):
    if user_id:
        # Есле указан второй айдишник - значит эта кнопка для оператора

        contact_id = int(user_id)
        as_user = "no"
        text = "Ответить пользователю"

    else:
        # Есле не указан второй айдишник - значит эта кнопка для пользователя
        # и нужно подобрать для него оператора

        contact_id = await get_support_manager(state=state)
        as_user = "yes"
        if messages == "many" and contact_id is None:
            # Если не нашли свободного оператора - выходим и говорим, что его нет
            return False
        text = "Написать оператору"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=support_callback.new(
                messages=messages,
                user_id=contact_id,
                as_user=as_user
            )
        )
    )

    if messages == "many":
        # Добавляем кнопку завершения сеанса, если передумали звонить в поддержку
        keyboard.add(
            InlineKeyboardButton(
                text="Завершить сеанс",
                callback_data=cancel_support_callback.new(
                    user_id=contact_id
                )
            )
        )
    return keyboard


def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить сеанс",
                    callback_data=cancel_support_callback.new(
                        user_id=user_id
                    )
                )
            ]
        ]
    )
