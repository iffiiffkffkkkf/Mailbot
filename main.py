#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import requests
import utils
import json
import os
from telebot import types
from telebot.util import quick_markup
from utils import Generate_Email, Load_Mail_Box

# Connect to bot
TempMailBot = telebot.TeleBot(utils.Token)
print(f"The Bot is online (id: {TempMailBot.get_me().id})...")

# Permanent keyboard layout
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💻 PROFILE", "💡 REFERRAL")
    markup.row("🔧 MY MAILS", "📧 GENERATE EMAIL")
    return markup

# Start command
@TempMailBot.message_handler(commands=["start", "restart"])
def start_command_handler(message):
    ufile = f"{message.from_user.id}"
    if ufile not in os.listdir("Accounts/"):
        os.mkdir(f"Accounts/{ufile}")
        os.mkdir(f"Accounts/{ufile}/mails/")
    TempMailBot.send_message(
        message.chat.id,
        f"Welcome {message.from_user.first_name}!\nUse the menu below to navigate.",
        reply_markup=main_menu()
    )

# Profile command
@TempMailBot.message_handler(func=lambda m: m.text == "💻 PROFILE")
def profile_handler(message):
    uid = message.from_user.id
    name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "None"
    mails_count = len(os.listdir(f"Accounts/{uid}/mails/")) if os.path.exists(f"Accounts/{uid}/mails/") else 0

    TempMailBot.send_message(
        message.chat.id,
        f"🆔 User: {name}\n"
        f"👤 Username: {username}\n"
        f"📬 Total Emails: {mails_count}",
        reply_markup=main_menu()
    )

# Referral command (placeholder)
@TempMailBot.message_handler(func=lambda m: m.text == "💡 REFERRAL")
def referral_handler(message):
    TempMailBot.send_message(
        message.chat.id,
        "Invite friends to use this bot!\n(Referral system not implemented yet)",
        reply_markup=main_menu()
    )

# My Mails
@TempMailBot.message_handler(func=lambda m: m.text == "🔧 MY MAILS")
def my_mails_handler(message):
    uid = message.from_user.id
    if not os.path.exists(f"Accounts/{uid}/mails/"):
        TempMailBot.send_message(message.chat.id, "You don't have any emails yet.", reply_markup=main_menu())
        return
    mails = sorted(os.listdir(f"Accounts/{uid}/mails/"))
    if not mails:
        TempMailBot.send_message(message.chat.id, "You don't have any emails yet.", reply_markup=main_menu())
        return
    msg = "📬 Your Emails:\n" + "\n".join([f"{i+1}. {mail}" for i, mail in enumerate(mails)])
    TempMailBot.send_message(message.chat.id, msg, reply_markup=main_menu())

# Generate Email
@TempMailBot.message_handler(func=lambda m: m.text == "📧 GENERATE EMAIL")
def generate_email_handler(message):
    try:
        TempMailBot.send_message(message.chat.id, "Generating your email, please wait...")
        result = "".join(Generate_Email(message))
        TempMailBot.send_message(message.chat.id, f"✅ New Email: {result}", reply_markup=main_menu())
    except Exception as e:
        TempMailBot.send_message(message.chat.id, f"❌ Could not generate email: {e}", reply_markup=main_menu())

# Keep other original callback functions if needed
# ...

if __name__ == "__main__":
    try:
        TempMailBot.infinity_polling(skip_pending=True, none_stop=True)
    except:
        print("Lost connection!")