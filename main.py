from datetime import datetime
from docxtpl import DocxTemplate
from vkbottle.bot import rules
from vkbottle import BaseStateGroup, DocMessagesUploader
from vkbottle import Keyboard, Text
from vkbottle.bot import Bot, Message
# from vkbottle.dispatch.rules.base import AttachmentTypeRule
import os
from user import User

bot = Bot(
    os.environ['TOKEN']
)


class Branch(BaseStateGroup):
    HELLO = 0
    INFO = 1
    NAME = 2
    BDAY = 3
    GROUP = 4
    LEARN = 5
    ADDR = 6
    NUMBER = 7
    LS = 8
    CHECK = 9
    PROVE = 10
    PDF = 11


async def docx(context):
    doc = DocxTemplate("template.docx")
    doc.render(context)
    doc.save(f'{context["name"]}.docx')


@bot.on.private_message(text=["Начать"])
async def start(m: Message):
    user = User(m.peer_id)
    keyboard = (
        Keyboard(inline=False, one_time=True).add(Text("Заполнить заявление"))
    ).get_json()
    await m.answer(
        "Здравствуй! Рады приветствовать тебя в помощнике профкома, который создан для упрощения жизни студентов. Здесь ты с легкостью сможешь подать заявление на вступление в профсоюз. Просто жми на кнопку.",
        keyboard=keyboard,
    )
    await bot.state_dispenser.set(m.peer_id, Branch.INFO, user=user)


@bot.on.private_message(state=Branch.INFO)
async def info(m: Message):
    user = m.state_peer.payload["user"]
    keyboard = (Keyboard(inline=False, one_time=True).add(Text("Приступим"))).get_json()
    await m.answer(
        "Всё просто, ты будешь вводить необходимые данные, а в заявлении они будут заполняться автоматически. После полного заполнения ты получишь готовое заявление, которое остается напечатать. Не переживай, нести куда-либо его не придется, необходимо только поставить подпись, отсканировать и отправить мне в формате PDF. И через время тебе придет подтверждение, что ты - член профсоюза!",
        keyboard=keyboard,
    )
    await bot.state_dispenser.set(m.peer_id, Branch.NAME, user=user)


@bot.on.private_message(state=Branch.NAME)
async def name(m: Message):
    user = m.state_peer.payload["user"]
    await m.answer("Для начала полностью введи ФИО.")
    await bot.state_dispenser.set(m.peer_id, Branch.BDAY, user=user)


@bot.on.private_message(state=Branch.BDAY)
async def bday(m: Message):
    user = m.state_peer.payload["user"]
    user.set_name(m.text)
    await m.answer(
        "Первый шаг позади, теперь необходимо ввести дату рождения в формате 00.00.0000."
    )
    await bot.state_dispenser.set(m.peer_id, Branch.GROUP, user=user)


@bot.on.private_message(state=Branch.GROUP)
async def group(m: Message):
    user = m.state_peer.payload["user"]
    user.set_birthday(m.text)
    await m.answer(
        "Следующее действие - твоя группа. Впиши номер группы в виде АБВ-00."
    )
    await bot.state_dispenser.set(m.peer_id, Branch.LEARN, user=user)


@bot.on.private_message(state=Branch.LEARN)
async def learn(m: Message):
    user = m.state_peer.payload["user"]
    user.set_group(m.text)
    keyboard = (
        Keyboard(inline=False, one_time=True).add(Text("Бюджет")).add(Text("Контракт"))
    ).get_json()
    await m.answer("Осталось немного, выбери свою основу обучения.", keyboard=keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.ADDR, user=user)


@bot.on.private_message(state=Branch.ADDR)
async def addres(m: Message):
    user = m.state_peer.payload["user"]
    user.set_learn(m.text)
    await m.answer("Укажи адрес проживания в Петербурге формате: г. Санкт-Петербург, улица, дом, квартира")
    await bot.state_dispenser.set(m.peer_id, Branch.NUMBER, user=user)


@bot.on.private_message(state=Branch.NUMBER)
async def number(m: Message):
    user = m.state_peer.payload["user"]
    user.set_addres(m.text)
    await m.answer("И последний шаг - введи свой контактный номер телефона. Обратите внимение на формат: 89219072414")
    await bot.state_dispenser.set(m.peer_id, Branch.LS, user=user)


@bot.on.private_message(state=Branch.LS)
async def check(m: Message):
    user = m.state_peer.payload["user"]
    if user.prove:
        if user.prove == "1":
            user.set_name(m.text)
        if user.prove == "2":
            user.set_birthday(m.text)
        if user.prove == "3":
            user.set_group(m.text)
        if user.prove == "4":
            user.set_learn(m.text) 
        if user.prove == "5":
            user.set_addres(m.text)
        if user.prove == "6":
            user.set_number(m.text)
        await bot.state_dispenser.set(m.peer_id, Branch.LS, user=user)
    else:
        user.set_number(m.text)
    keyboard = (
        Keyboard(inline=False, one_time=True).add(Text("Да")).add(Text("Нет"))
    ).get_json()
    await m.answer(
        f"Перед отправкой заявления проверь свои данные: \n1. ФИО: {user.name}\n2. Дата рождения: {user.bday}\n3. Твоя академическая группа: {user.group}\n4. Основа обучения: {user.learn}\n5. Адрес проживания: {user.addr}\n6. Твой номер: {user.number}\nВсё верно?",
        keyboard=keyboard,
    )
    await bot.state_dispenser.set(m.peer_id, Branch.CHECK, user=user)


@bot.on.private_message(state=Branch.CHECK)
async def yes_or_not(m: Message):
    user = m.state_peer.payload["user"]
    months = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    }

    if m.text == "Да":
        context = {
        "name": user.name,
        "bday": user.bday,
        "group": user.group,
        "learn": user.learn,
        "addr": user.addr,
        "number": user.number,
        "date": datetime.today().day,
        "month": months[datetime.today().month],

        }
        await docx(context)
        doc_to_send = await DocMessagesUploader(bot.api).upload(
        f"{user.name}.docx", f"{user.name}.docx", peer_id=m.peer_id
        )
        await m.answer("Полдела сделано, осталось - распечатать, поставить подпись и отправить обратно в формате PDF. Мы с нетерпением ждем отсканированный документ.",attachment=doc_to_send)
        os.remove(f"{user.name}.docx")
        await bot.state_dispenser.set(m.peer_id, Branch.PDF)
    if m.text == "Нет":
        keyboard = (
            Keyboard(inline=False, one_time=True)
            .add(Text("1"))
            .add(Text("2"))
            .add(Text("3"))
            .row()
            .add(Text("4"))
            .add(Text("5"))
            .add(Text("6"))
        ).get_json()
        await m.answer(
            "Где ты совершил ошибку?\n1. ФИО\n2. Дата рождения\n3. Группа\n4. Основа обучения\n5. Адрес проживания\n6. Номер",
            keyboard=keyboard,
        )
        await bot.state_dispenser.set(m.peer_id, Branch.PROVE, user=user)


@bot.on.private_message(state=Branch.PROVE)
async def prove(m: Message):
    user = m.state_peer.payload["user"]
    user.set_prove(m.text)
    if m.text == "1":
        await m.answer("Введите исправленный вариант")
    elif m.text == "2":
        await m.answer("Введите исправленный вариант")
    elif m.text == "3":
        await m.answer("Введите исправленный вариант")
    elif m.text == "4":
        await m.answer("Введите исправленный вариант")
    elif m.text == "5":
        await m.answer("Введите исправленный вариант")
    elif m.text == "6":
        await m.answer("Введите исправленный вариант")
    await bot.state_dispenser.set(m.peer_id, Branch.LS, user=user)


# @bot.on.private_message(rules.AttachmentTypeRule("doc"))

@bot.on.private_message(rules.AttachmentTypeRule("doc"), state=Branch.PDF)
async def pdf(m: Message):
    # print(m)
    # await m.answer("1")
    if m.attachments[0].doc.ext != 'pdf':
        await m.answer("Произошла ошибка, формат заявления не верен. Отправь, пожалуйста, повторно, но использую PDF-файл.")
    else:
        await m.answer("Заявление находится на рассмотрении. В ближайшее время модератор осуществит проверку.")
        return

if __name__ == "__main__":
    bot.run_forever()
