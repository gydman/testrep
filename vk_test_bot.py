import vk_api
import time
import random
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from auth_data import token
from func_and_var import list_answer

# Создание переменной с функцией вызова клавиатуры (одно нажатие)
keyboard = VkKeyboard()
# Создание кнопок
keyboard.add_button('a', color=VkKeyboardColor.PRIMARY)
# перенос кнопки на следующую строку
keyboard.add_line()
keyboard.add_button('s', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('p', color=VkKeyboardColor.NEGATIVE)
keyboard.add_line()
keyboard.add_openlink_button('Ссылка', link='https://github.com/gydman')


# отправить ответ на новое сообщение
def write_message(sender, message):
    vk_session.method('messages.send',
                      {
                          'user_id': sender,
                          'message': message,
                          'random_id': get_random_id()
                          })


# отправить картинку
def send_photo(sender):
    vk_session.method('messages.send',
                      {
                          'user_id': sender,
                          'message': 'Понравилась картинка?',
                          'attachment': ','.join(attachments),
                          'random_id': get_random_id(),
                          # вызов json клавиатуры
                          'keyboard': keyboard.get_keyboard()
                          })


def view_keybord(sender):
    vk_session.method('messages.send',
                      {
                          'user_id': sender,
                          'message': '',
                          'random_id': get_random_id(),
                          # вызов json клавиатуры
                          'keyboard': keyboard.get_keyboard()
                          })


vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)

image = "C:/test/1.jpg"
upload = VkUpload(vk_session)

while True:
    # Прослушиваем сервер
    for event in longpoll.listen():
        # Обработка нового сообщения
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # для сообщения
            received_message = event.text.lower()
            sender = event.user_id

            # для картинки
            attachments = []
            upload_image = upload.photo_messages(photos=image)[0]
            attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))

            # анализ полученного текста и реакция
            if received_message == 'a':
                write_message(sender, list_answer['A'][random.randint(0, 4)])
                # send_photo(sender)
            elif received_message == 's':
                write_message(sender, list_answer['B'][random.randint(0, 4)])
            elif received_message == 'p':
                send_photo(sender)
            elif received_message == 'l':
                view_keybord(sender)
            else:
                write_message(sender, list_answer['C'][random.randint(0, 4)])

        time.sleep(0.5)
