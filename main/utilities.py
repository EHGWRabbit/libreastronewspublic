from django.template.loader import render_to_string
from django.core.signing import Signer
from astron.settings import ALLOWED_HOSTS
from datetime import datetime 
from os.path import splitext 



signer = Signer()


#пишем функцию отправки сообщений на почту
def send_activation_note(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


#функция, генерирующая именя сохраняемых выгружаемых файлов
def get_time_stamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
    