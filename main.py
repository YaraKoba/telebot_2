from envparse import Env
from functions import database, mess
from functions.row_request import RowReq, MyBot
from functions.get_meteo import go_fly
import functions.button


def main():
    env = Env()
    TOKEN = env.str("TOKEN")
    ADMIN_ID = env.str("ADMIN_ID")
    row_req = RowReq(token=TOKEN, base_url='https://api.telegram.org')
    bot = MyBot(token=TOKEN, row_req=row_req)

    @bot.message_handler(commands=['start'])
    def start(message):
        mes = mess.header_mess(message)
        bot.send_message(message.chat.id, mes, parse_mode='html')
        database.add_user(message)

    @bot.message_handler(commands=['help'])
    def helper(message):
        params = {
            "chat_id": f'{ADMIN_ID}',
            "text": "test test"
        }
        lst = [1, 2]
        print(lst[3])
        mes = mess.header_mess(message)
        bot.send_message(message.chat.id, mes, parse_mode='html')
        bot.row_req.post(method='sendmessage', params=params)

    @bot.message_handler(commands=['days'])
    def show_days(message):
        markup = functions.button.day_btn()
        bot.send_message(message.chat.id, "Даты обновлены", parse_mode='html', reply_markup=markup)

    # @bot.message_handler(commands=['go', 'stop'])
    # def remeber(message):
    #     if message.text == '/go':
    #         exit_even.clear()
    #         bot.send_message(message.chat.id, 'Уведомления запущены')
    #     else:
    #         bot.send_message(message.chat.id, 'Уведомления отключены')
    #         exit_even.set()
    #
    # @bot.message_handler(regexp=r'Все летные дни!')
    # def all_call(message):
    #     date_all = [f'{d1}...', f'{d2}...', f'{d3}...', f'{d4}...', f'{d5}...']
    #     res = go_fly(date_all)
    #     repost(message, res)

    @bot.message_handler(regexp=r"[А-Я][а-я]\s\d{2}\s[а-я]+\b")
    def get_usre_text(message):
        date_f = [mess.re_amdate(message.text)]
        print(date_f)
        res = go_fly(date_f)
        bot.send_message(message.chat.id, res, parse_mode='html')

    while True:
        try:
            bot.polling()
        except Exception as err:
            params = {
                "chat_id": f'{ADMIN_ID}',
                "text": mess.err_mess(err)}
            bot.row_req.post(method="sendmessage", params=params)


if __name__ == '__main__':
    main()
