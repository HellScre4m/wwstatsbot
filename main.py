#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wolfcardbot.py - Extracts Werewolf for Telegram Stats & Displays in Chat
# author - Carson True
# license - GPL

# edited by @jeffffc

import requests
import logging

from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from bs4 import BeautifulSoup
import datetime
import random
	
from config import *
import wwstats

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

telegram_api_token =  BOT_TOKEN

#@run_async
def get_stats(user_id):
    stats = {}
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerStats/?pid={}"

    r = requests.get(wuff_url.format(user_id))

    dump = BeautifulSoup(r.json(), 'html.parser')

    stats['games_played'] = dump('td')[1].string
    stats['games_won'] = { 'number': dump('td')[3].string, 'percent': dump('td')[4].string }
    stats['games_lost'] = { 'number': dump('td')[6].string, 'percent': dump('td')[7].string }
    stats['games_survived'] = { 'number': dump('td')[9].string, 'percent': dump('td')[10].string  }
    stats['most_common_role'] = { 'role': dump('td')[12].string, 'times': dump('td')[13].string[:-6] }
    stats['most_killed'] = { 'name': dump('td')[15].string, 'times': dump('td')[16].string[:-6] }
    stats['most_killed_by'] = { 'name': dump('td')[18].string, 'times': dump('td')[19].string[:-6] }

    return stats


#@run_async
def get_achievement_count(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerAchievements/?pid={}"

    r = requests.get(wuff_url.format(user_id))

    dump = BeautifulSoup(r.json(), 'html.parser')

    count = int(len(dump('td')) / 2)

    return count


#@run_async
def display_stats(bot, update):
    chat_id = update.message.chat_id
    if update.message.reply_to_message is not None:
        if update.message.reply_to_message.forward_from is not None:
            user_id = update.message.reply_to_message.forward_from.id
            name = update.message.reply_to_message.forward_from.first_name
            username = update.message.reply_to_message.forward_from.username
        else:
            user_id = update.message.reply_to_message.from_user.id
            name = update.message.reply_to_message.from_user.first_name
            username = update.message.reply_to_message.from_user.username
    else:
        user_id = update.message.from_user.id
        name = update.message.from_user.first_name
        username = update.message.from_user.username

    print("%s - %s (%d) - stats" % (str(datetime.datetime.now()+datetime.timedelta(hours=8)), name, user_id))

    stats = get_stats(user_id)
    achievements = get_achievement_count(user_id)


    if username is None:
        msg =  "<a href='tg://" + str(user_id) + "'>" + str(name) + " the " + stats['most_common_role']['role'] + "</a>\n"
    else:
        msg =  "<a href='https://telegram.me/" + str(username) + "'>" + str(name) + " the " + stats['most_common_role']['role'] + "</a>\n"
    msg += "<code>{:<5}</code> دستاورد داری 🏆\n".format(achievements)
    msg += "<code>{:<5}</code> بازی رو بردی <code>({})</code>\n".format(stats['games_won']['number'], stats['games_won']['percent'])
    msg += "<code>{:<5}</code> بازی رو باختی <code>({})</code>\n".format(stats['games_lost']['number'], stats['games_lost']['percent'])
    msg += "<code>{:<5}</code> بازی رو تا آخرش زنده موندی <code>({})</code>\n".format(stats['games_survived']['number'], stats['games_survived']['percent'])
    msg += "<code>{:<5}</code> تعداد کل بازیاته 🤷‍♂️\n".format(stats['games_played'])
    killed = ["<code>{:<5}</code> بار خبیثانه {} رو کشتی 😈\n", "<code>{:<5}</code> بار حال {} رو گرفتی 🤤\n", 
    "<code>{:<5}</code> بار خون {} رو ریختی 🔪\n", "<code>{:<5}</code> دفعه {} رو ضربه فنیش کردی 💪\n"]
    died = ["<code>{:<5}</code> بار {} لهت کرده 🤕\n", "<code>{:<5}</code> دفعه {} حالتو گرفته 😜\n",
    "<code>{:<5}</code> بار {} صورتت رو خط خطی کرده ⚡️\n"]
    msg += random.choice(killed).format(stats['most_killed']['times'], stats['most_killed']['name'])
    msg += random.choice(died).format(stats['most_killed_by']['times'], stats['most_killed_by']['name'])
    msg += "<a href='https://telegram.me/CafeWerewolf'>cαғε шεяεшσʟғ 🇮🇷</a>\n"
    

    bot.sendMessage(chat_id, msg, parse_mode="HTML", disable_web_page_preview=True)

#@run_async
def display_about(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    username = update.message.from_user.username
    msg = "Use /stats for stats. Use /achievements or /achv for achivement list."
    msg += "\n\nThis is an edited version to the old wolfcardbot.\n"
    msg += "Click [here](http://pastebin.com/efZ4CPXJ) to check the original source code.\n"
    msg += "Click [here](https://github.com/jeffffc/wwstatsbot) for the source code of the current project.\n"
    msg += "<a href='https://telegram.me/CafeWerewolf'>cαғε шεяεшσʟғ 🇮🇷</a>\n"

    bot.sendMessage(chat_id, msg, parse_mode="Markdown", disable_web_page_preview=True)


def startme(bot, update):
    if update.message.chat.type == 'private':
        update.message.reply_text("مرسی که هستی 😐❤️ اگه می‌خوایی آمار بازیتو ببینی بزن /stats و اگه می‌خوایی ببینی دستاوردات چیان بزن /achievements.")
    else:
        return


#@run_async
def display_achv(bot, update):
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name

    print("%s - %s (%d) - achv" % (str(datetime.datetime.now()+datetime.timedelta(hours=8)), name, user_id))

    msgs = wwstats.check(user_id)

    try:
        for msg in msgs:
            if msg != "":
                bot.sendMessage(chat_id = user_id, text = msg, parse_mode='Markdown')
        if update.message.chat.type != 'private':
            update.message.reply_text("دستاورداتو فرستادم پیوی مشتی 😘")
    except Exception as e:
        url = "telegram.me/" + BOT_USERNAME
        keyboard = [[InlineKeyboardButton("Start Me!", url = url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("داداچ پیوی یه استارت میزنی قربونت؟؟", reply_markup = reply_markup)
        print (e)


def main():
    u = Updater(token=telegram_api_token)
    d = u.dispatcher

    d.add_handler(CommandHandler('start', startme))
    d.add_handler(CommandHandler('stats', display_stats))
    d.add_handler(CommandHandler('about', display_about))
    d.add_handler(CommandHandler('achievements', display_achv))
    d.add_handler(CommandHandler('achv', display_achv))
    u.start_polling(clean=True)
    u.idle()

if __name__ == '__main__':
    main()