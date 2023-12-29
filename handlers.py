from aiogram import Router, Bot, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

router = Router()


class Form(StatesGroup):
    start_check = State()
    name = State()
    depart_city = State()
    resort = State()
    quan = State()
    dates = State()
    nights = State()
    budget = State()
    messanger = State()
    numbers = State()
    end = State()
    start_again = State()
    name_alt = State()
    numbers_alt = State()


# name_introduced = 0
# depart_city_introduced = 0
# resort_introduced = 0
# quan_introduced = 0
# dates_introduced = 0
# nights_introduced = 0
# budget_introduced = 0
# messanger_introduced = 0
# numbers_introduced = 0


@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext) -> None:
    kb = [
        [
            types.KeyboardButton(text="Связаться с менеджером📞"),
            types.KeyboardButton(text="Заполнить анкету📋")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        "Здравствуйте!) Вы попали в чат-бот «Маркет Слетать»🛫\n\n"
        "Наша команда более 10 лет работает в сфере туризма, поэтому мы точно организуем для вас лучший отдых!💙\n\n"
        "Мы всегда профессионально:\n"
        "✔️Расскажем, где выгоднее и комфортнее отдохнуть исходя из вашего запроса\n"
        "✔️Подберем самые выгодные условия только от проверенных и надежных туроператоров\n\n"
        "Ответьте на несколько наших вопросов, которые займут не более 2 минут👇🏼",
        reply_markup=keyboard
    )
    await state.set_state(Form.start_check)


@router.callback_query(F.data == "inline_manager_pressed")
async def process_buttons_inline_manager_press(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer("🛫")
    # inline_start = InlineKeyboardButton(
    #     text="Хочу оставить заявку",
    #     callback_data="inline_start_pressed"
    # )
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_start]])
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Для связи с вами нам потребуется:\n\n"
                                "1️⃣Ваше имя. Подскажите, как мы можем к вам обращаться?"  # reply_markup=keyboard
                           )
    await state.set_state(Form.name_alt)


@router.callback_query(F.data == "inline_start_pressed")
async def process_buttons_inline_start_press(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(Form.name)
    await callback.answer("🛫")
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"Давайте приступим👋🏼 Подскажите, как я могу к вам обращаться?",
                           )


@router.message(Form.start_check)
async def process_start_check(message: Message, state: FSMContext) -> None:
    await state.update_data(start_check=message.text)
    data = await state.get_data()
    print(data['start_check'])
    if data['start_check'] == "Заполнить анкету📋":
        await state.set_state(Form.name)
        await message.answer("Давайте приступим👋🏼 Подскажите, как я могу к вам обращаться?")
    else:
        # inline_start = InlineKeyboardButton(
        #    text="Хочу оставить заявку.",
        #    callback_data="inline_start_pressed"
        # )
        # keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_start]])
        await message.answer("Для связи с вами нам потребуется:\n\n"
                             "1️⃣Ваше имя. Подскажите, как мы можем к вам обращаться?")  # reply_markup=keyboard
        await state.set_state(Form.name_alt)


@router.message(Form.name_alt)
async def process_name_alt(message: Message, state: FSMContext) -> None:
    await state.update_data(name_alt=message.text)
    data = await state.get_data()
    await message.answer("Спасибо!)\n\n"
                         "2️⃣А также ваш номер телефона. Напишите, пожалуйста, его в формате 8хххххххххх")
    await state.set_state(Form.numbers_alt)


@router.message(Form.numbers_alt)
async def process_numbers_atl(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(numbers_alt=message.text)
    data = await state.get_data()
    if data['numbers_alt'].isdigit() and len(data['numbers_alt']) == 11:
        inline_start = InlineKeyboardButton(
            text="Оставить еще одну заявку",
            callback_data="inline_start_pressed"
        )
        inline_manager = InlineKeyboardButton(
            text="Связатся с нашим менеджером",
            callback_data="inline_manager_pressed"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [inline_start],
            [inline_manager]
        ])
        await message.answer("Благодарим вас за оставленный номер, мы уже передали его менеджеру💙\n\n"
                             "Ожидайте звонка в течение часа📞")
        await message.answer(
            f"Спасибо, что выбрали наше агентство🛫\n\n"
            f"Мы – не просто команда коллег, а люди, которые стараются "
            f"<i>сделать жизнь наших туристов более комфортной. "
            f"Вы можете расслабиться и не переживать за запланированный отдых))</i> "
            f"Поэтому мы говорим, что <b>ваш отдых начинается не с самолета, а с нас!</b>\n\n"
            f"Все в одном окне — мы работаем не только с пакетными предложениями, но и <u>оформляем визы под туры</u>, "
            f"помогаем с <u>покупкой отдельно авиабилетов</u>, <u>бронированием проживания</u>. "
            f"Предлагаем <b>VIP-сервис</b>⭐️ и организацию <b>индивидуальных, "
            f"групповых, корпоративных и других туров!</b>\n\n"
            f"<i>Подпишитесь на полезные каналы «Маркет Слетать»:</i>\n\n"
            f"1️⃣<i><a href='https://t.me/marketsletat_tours'>Здесь будем делиться с вами нашими акционными предложениями и горячими🔥 подборками</a></i>\n"
            f"2️⃣<i><a href='https://t.me/marketsletatspb'>Тут новости туризма, наши счастливые клиенты и интересные посты🗺️</a></i>\n"
            f"<b>Поддержите нас подпиской и не забывайте ставить реакции, писать комментарии!</b>\n\n"
            f"<i>Или используйте любой другой удобный канал связи:</i>\n\n"
            f"<a href='https://market-sletat.ru/'>Сайт</a>\n"
            f"<a href='https://vk.com/officsletat'>ВКонтакте</a>\n"
            f"<a href='https://instagram.com/marketsletat?igshid=MzRlODBiNWFlZA=='>In$tagr@m</a>",
            parse_mode="HTML", disable_web_page_preview=True, reply_markup=keyboard,
        )
        user = f"{message.from_user.username}"
        await bot.send_message(chat_id=-1002060096138, text=f"Имя: {data['name_alt']}\n"
                                                            f"Номер: {data['numbers_alt']}\n"
                                                            f"ТГ username: @{user}"
                               )
    else:
        await message.answer(
            "❗️Вы можете использовать только цифры. Напишите, пожалуйста, номер в формате 8хххххххххх"
        )


@router.message(Form.name)
async def process_name(message: Message, state: FSMContext, ) -> None:
    await state.set_state(Form.depart_city)
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(
        f"{message.text}, из какого города планируете вылет?",
    )
    # global name_introduced
    # name_introduced = f"Имя: {message.text}"


@router.message(Form.depart_city)
async def process_depart_city(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.resort)
    await state.update_data(depart_city=message.text)
    data = await state.get_data()
    await message.answer(
        "Какое направление для отдыха рассматриваете? Напишите ниже все интересующие вас варианты🖋️\n\n"
        "Наши эксперты по турам включат в подборку несколько предложений по каждому!)"
    )
    # global depart_city_introduced
    # depart_city_introduced = f"Город вылета: {message.text}"


@router.message(Form.resort)
async def process_resort(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.quan)
    await state.update_data(resort=message.text)
    data = await state.get_data()
    await message.answer(
        "Отлично!) Сколько человек отправятся в путешествие?👩🏻🧑🏼‍🦱 Будут ли с вами дети, сколько?👧🏼"
    )
    # global resort_introduced
    # resort_introduced = f"Курорт: {message.text}"


@router.message(Form.quan)
async def process_dates(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.dates)
    await state.update_data(quan=message.text)
    data = await state.get_data()
    await message.answer(
        f"{data['name']}, укажите пожалуйста, на какие даты планируете путешествие?🗓️"
    )
    # global quan_introduced
    # quan_introduced = f"Количество человек: {message.text}"


@router.message(Form.dates)
async def process_quan(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.nights)
    await state.update_data(dates=message.text)
    data = await state.get_data()
    await message.answer(
        "Сколько ночей закладываете на отпуск?"
    )
    # global dates_introduced
    # dates_introduced = f"Даты поездки: {message.text}"


@router.message(Form.nights)
async def process_nights(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.budget)
    await state.update_data(nights=message.text)
    data = await state.get_data()
    await message.answer(
        f"Спасибо! Уточните свой бюджет на поездку💵"
    )


# global nights_introduced
# nights_introduced = f"Количетсво ночей: {message.text}"


@router.message(Form.budget)
async def process_budget(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.messanger)
    await state.update_data(budget=message.text)
    data = await state.get_data()
    kb = [
        [
            types.KeyboardButton(text="Позвонить📲"),
            types.KeyboardButton(text="WhatsApp💬"),
            types.KeyboardButton(text="Telegram💬")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer(f"Каким способом вам было бы удобнее получить персональную подборку от наших экспертов?",
                         reply_markup=keyboard)
    # global budget_introduced
    # budget_introduced = f"Бюджет: {message.text}"


@router.message(Form.messanger)
async def process_messanger(message: Message, state: FSMContext) -> None:
    await state.update_data(messanger=message.text)
    data = await state.get_data()
    if data['messanger'] == "Позвонить📲" or data['messanger'] == "WhatsApp💬" or data['messanger'] == "Telegram💬":
        await state.set_state(Form.numbers)
        await message.answer(f"Для связи с вами нам потребуется номер телефона📲\n\n"
                             f"Напишите его ниже, пожалуйста, в формате 8хххххххххх")
        # global messanger_introduced
        # messanger_introduced = f"Способ связи: {message.text}"
    else:
        kb = [
            [
                types.KeyboardButton(text="Позвонить📲"),
                types.KeyboardButton(text="WhatsApp💬"),
                types.KeyboardButton(text="Telegram💬")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer(f"Пожалуйста, выберите способ связи из предложенных вариантов🙏🏼", reply_markup=keyboard)


@router.message(Form.numbers)
async def process_numbers(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(numbers=message.text)
    data = await state.get_data()
    if data['numbers'].isdigit() and len(data['numbers']) == 11:
        inline_start = InlineKeyboardButton(
            text="Оставить еще одну заявку",
            callback_data="inline_start_pressed"
        )
        inline_manager = InlineKeyboardButton(
            text="Связатся с нашим менеджером",
            callback_data="inline_manager_pressed"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [inline_start],
            [inline_manager]
        ])
        await message.answer(
            f"Мы справились!\n"
            f"Благодарим вас за заполнение анкеты, мы уже взяли ее в работу💙\n\n"
            f"Как только наш эксперт подготовит персональную подборку для вас, он свяжется указанным способом😌"
        )
        await message.answer(
            f"Спасибо, что выбрали наше агентство🛫\n\n"
            f"Мы – не просто команда коллег, а люди, которые стараются "
            f"<i>сделать жизнь наших туристов более комфортной. "
            f"Вы можете расслабиться и не переживать за запланированный отдых))</i> "
            f"Поэтому мы говорим, что <b>ваш отдых начинается не с самолета, а с нас!</b>\n\n"
            f"Все в одном окне — мы работаем не только с пакетными предложениями, но и <u>оформляем визы под туры</u>, "
            f"помогаем с <u>покупкой отдельно авиабилетов</u>, <u>бронированием проживания</u>. "
            f"Предлагаем <b>VIP-сервис</b>⭐️ и организацию "
            f"<b>индивидуальных, групповых, корпоративных и других туров!</b>\n\n"
            f"<i>Подпишитесь на полезные каналы «Маркет Слетать»:</i>\n\n"
            f"1️⃣<i><a href='https://t.me/marketsletat_tours'>Здесь будем делиться с вами нашими акционными предложениями и горячими🔥 подборками</a></i>\n"
            f"2️⃣<i><a href='https://t.me/marketsletatspb'>Тут новости туризма, наши счастливые клиенты и интересные посты🗺️</a></i>\n"
            f"<b>Поддержите нас подпиской и не забывайте ставить реакции, писать комментарии!</b>\n\n"
            f"<i>Или используйте любой другой удобный канал связи:</i>\n\n"
            f"<a href='https://market-sletat.ru/'>Сайт</a>\n"
            f"<a href='https://vk.com/officsletat'>ВКонтакте</a>\n"
            f"<a href='https://instagram.com/marketsletat?igshid=MzRlODBiNWFlZA=='>In$tagr@m</a>",
            parse_mode="HTML", disable_web_page_preview=True, reply_markup=keyboard,
        )
        # print(await bot.get_webhook_info())
        # await state.set_state(Form.end)
        user = f"{message.from_user.username}"
        # global numbers_introduced
        # numbers_introduced = f"Номер телефона: {message.text}"
        await bot.send_message(chat_id=-1002060096138,
                               text=f"Имя: {data['name']}\n"  # ID 443453297 мой,  канал -1002060096138
                                    f"Город вылета: {data['depart_city']}\n"
                                    f"Курорт: {data['resort']}\n"
                                    f"Количество человек: {data['quan']}\n"
                                    f"Даты поездки: {data['dates']}\n"
                                    f"Количетсво ночей: {data['nights']}\n"
                                    f"Бюджет: {data['budget']}\n"
                                    f"Способ связи: {data['messanger']}\n"
                                    f"ТГ username: @{user}\n"
                                    f"Номер телефона: {data['numbers']}"
                               )
    else:
        await message.answer(
            f"❗️Вы можете использовать только цифры. Напишите, пожалуйста, номер в формате 8хххххххххх")
