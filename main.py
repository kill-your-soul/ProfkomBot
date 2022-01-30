from docxtpl import DocxTemplate
from vkbottle import BaseStateGroup, DocMessagesUploader, LoopWrapper
from vkbottle.bot import Bot, Message
import os
from user import User

# doc = DocxTemplate('test.docx')
# context = {
#     'my_var': 'Test String'
# }
# doc.render(context=context)
# doc.save('gen.docx')
bot = Bot(
    "d0e78fb81e2f2af25d291a1a65e50c232e7ade6ff4ce33937b11a5999523bb69a16b2271b4f8d7eed1c99"
)


class Branch(BaseStateGroup):
    START = 0
    BDAY = 1
    GROUP = 2
    LEARN = 3
    ADDR = 4
    NUMBER = 5
    END = 6


async def docx(context):
    doc = DocxTemplate("template.docx")
    doc.render(context)
    doc.save(f'{context["name"]}.docx')


@bot.on.private_message(text=["Начать"])
async def start(m: Message):
    user = User(m.peer_id)
    await m.answer("Привет, это бот для профкома(dev)")
    await m.answer("Введите свое ФИО")
    await bot.state_dispenser.set(m.peer_id, Branch.BDAY, user=user)


@bot.on.private_message(state=Branch.BDAY)
async def birth_day(m: Message):
    user = m.state_peer.payload["user"]
    user.set_name(m.text)
    await m.answer("Введите дату рождения в формате(dev)")
    await bot.state_dispenser.set(m.peer_id, Branch.GROUP, user=user)


@bot.on.private_message(state=Branch.GROUP)
async def group(m: Message):
    user = m.state_peer.payload["user"]
    user.set_birthday(m.text)
    await m.answer("Введите вашу группу в формате(dev)")
    await bot.state_dispenser.set(m.peer_id, Branch.LEARN, user=user)


@bot.on.private_message(state=Branch.LEARN)
async def learn(m: Message):
    user = m.state_peer.payload["user"]
    user.set_group(m.text)
    await m.answer("Введите бюджет вы или коммерция(dev)")
    await bot.state_dispenser.set(m.peer_id, Branch.ADDR, user=user)


@bot.on.private_message(state=Branch.ADDR)
async def addres(m: Message):
    user = m.state_peer.payload["user"]
    user.set_learn(m.text)
    await m.answer("Введите адрес своего проживания(dev)")
    await bot.state_dispenser.set(m.peer_id, Branch.NUMBER, user=user)


@bot.on.private_message(state=Branch.NUMBER)
async def number(m: Message):
    user = m.state_peer.payload["user"]
    user.set_addres(m.text)
    await m.answer("Введите ваш номер(dev)")
    await bot.state_dispenser.set(m.peer_id, Branch.END, user=user)


@bot.on.private_message(state=Branch.END)
async def learn(m: Message):
    user = m.state_peer.payload["user"]
    user.set_number(m.text)
    context = {
        "name": user.name,
        "bday": user.bday,
        "group": user.group,
        "learn": user.learn,
        "addr": user.addr,
        "number": user.number,
    }
    await docx(context)
    doc_to_send = await DocMessagesUploader(bot.api).upload(
        f"{user.name}.docx", f"{user.name}.docx", peer_id=m.peer_id
    )
    await m.answer(attachment=doc_to_send)
    os.remove(f"{user.name}.docx")
    del user
    # await m.answer(str(user))
    # await bot.state_dispenser(m.peer_id, Branch.ADDR, user=user)


if __name__ == "__main__":
    bot.run_forever()
