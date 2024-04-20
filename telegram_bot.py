import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from keys import TELEGRAM_KEY

# Importation de la fonction text_to_text depuis text_to_text.py
from text_to_text import text_to_text

# Clé de l'API Telegram Bot
TOKEN = TELEGRAM_KEY

TEXT, TARGET_LANGUAGE = range(2)

# Fonction pour gérer la commande /text2text
def text2text(update, context):
    update.message.reply_text("Envoyez le texte que vous souhaitez traduire :")
    return TEXT

# Fonction pour demander la langue cible
def ask_target_language(update, context):
    text_to_translate = update.message.text

    # Sauvegarde du texte à traduire dans le contexte
    context.user_data['text_to_translate'] = text_to_translate

    update.message.reply_text("Entrez le code de la langue cible (par ex. fr pour le français) :")
    return TARGET_LANGUAGE

# Fonction pour traduire le texte et envoyer la traduction
def translate_text(update, context):
    target_language_code = update.message.text

    # Récupération du texte à traduire depuis le contexte
    text_to_translate = context.user_data['text_to_translate']

    # Appel à la fonction text_to_text avec les arguments requis
    translated_text = text_to_text(text_to_translate, target_language_code)

    update.message.reply_text(f"Traduction : {translated_text}")

    return ConversationHandler.END

# Fonction principale pour démarrer le bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('text2text', text2text)],
        states={
            TEXT: [MessageHandler(Filters.text & ~Filters.command, ask_target_language)],
            TARGET_LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, translate_text)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    # Démarrage du bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()