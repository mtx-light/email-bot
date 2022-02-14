from email_bot.root import app
import email_bot.utils.email
from email_bot.utils.dative import get_dative


@app.handle(intent='start')
def start(request, responder):
    responder.reply('Здравствуйте, я имэйл-бот компании Смидл.'
                    ' Пока что я умею отправлять имейл вашим коллегам, но скоро научусь делать много других вещей.'
                    ' Чем я могу вам помочь?')


@app.handle(intent='competence')
def competence(request, responder):
    responder.reply('Пока что я могу только помочь вам отправить имэйл.'
                    ' Вы же не умеете пользоваться интернетом, судя по всему.')


@app.handle(intent='small_talk')
def small_talk(request, responder):
    responder.reply('Я не умею говорить на отвлеченные темы. Чем я еще могу вам помочь?')


@app.handle(default=True)
def default(request, responder):
    responder.reply('Да-да, я вас слушаю.')


@app.handle(intent='send_email')
def send_email(request, responder):
    responder.params.target_dialogue_state = 'send_email2'
    responder.reply('Кому вы хотите отправит имейл?')


@app.handle(intent='send_email', has_entity='employee')
def send_email2(request, responder):
    if request.intent == 'exit':
        responder.reply('Ошибочка вышла. Чем еще я могу вам помочь?')
        return
    elif request.intent == 'small_talk':
        responder.reply('Извините, не могу найти такого сотрудника. Чем еще я могу вам помочь?')
        return
    employees = [e['value'][0]['cname'] for e in request.entities if e['type'] == 'employee' and e['value']]
    if employees:
        responder.frame['employee'] = employees[0]
        id_dative = get_dative(responder.frame['employee'])
        responder.params.target_dialogue_state = 'confirm_email'
        responder.reply(f'Вы хотите отправить письмо {id_dative}?')
        return
    else:
        responder.params.target_dialogue_state = 'send_email2'
        responder.reply(f'Пользователь "{request.entities[0]["text"]}" не распознан, обозначтье его еще как-то.')
        #responder.reply('Извините, не расслышал. Повторите имя адресата еще раз.')

@app.handle(targeted_only=True)
def confirm_email(request, responder):
    if request.intent == 'confirmation':
        responder.params.target_dialogue_state = 'email_topic'
        responder.reply('Хорошо. Какая тема этого письма?')
        return
    else:
        responder.params.target_dialogue_state = 'send_email2'
        responder.reply('Кому вы хотите отправит имейл?')


@app.handle(targeted_only=True)
def email_topic(request, responder):
    responder.frame['topic'] = request.text
    responder.params.target_dialogue_state = 'email_topic_confirm'
    responder.reply(f'Тема письма звучит так: {responder.frame["topic"]}. Правильно?')


@app.handle(targeted_only=True)
def email_topic_confirm(request, responder):
    if request.intent == 'exit':
        responder.reply('Чем еще я могу вам помочь?')
        return
    elif request.intent == 'confirmation':
        responder.params.target_dialogue_state = 'email_body'
        responder.reply('Отлично. Теперь продиктуйте, пожалуйста, текст вашего письма.')
        return
    else:
        responder.params.target_dialogue_state = 'email_topic'
        responder.reply('Тогда продиктуйте тему письма еще раз, пожалуйста.')


@app.handle(targeted_only=True)
def email_body(request, responder):
    responder.frame['body'] = request.text
    responder.params.target_dialogue_state = 'email_final'
    responder.reply(f'Спасибо. Если я правильно расслышал, то текст письма такой: {responder.frame["body"]}.'
                    f' Это письмо с темой {responder.frame["topic"]} будет отправлено {get_dative(responder.frame["employee"])}.'
                    f' Вы подтверждаете, что все правильно?')


@app.handle(targeted_only=True)
def email_final(request, responder):
    if request.intent == 'confirmation':
        email_bot.utils.email.send_email(responder.frame["employee"], responder.frame["topic"], responder.frame["body"])
        responder.reply('Прекрасно. Ваше письмо отправлено. Чем еще я могу вам помочь?')
        return
    else:
        responder.reply('Как вы меня заебали. Научитесь пользоваться интернетом. Всего вам наилучшего.')
