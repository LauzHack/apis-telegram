import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from datetime import datetime

# Importation des fonctions text_to_text, text_to_speech et speech_to_text depuis les fichiers correspondants
from text_to_text import text_to_text
from text_to_speech import text_to_speech
from speech_to_text import speech_to_text
from speech_to_speech import speech_to_speech

from keys import TELEGRAM_KEY

# Clé de l'API Telegram Bot
TOKEN = TELEGRAM_KEY

TEXT, TARGET_LANGUAGE, TEXT_SPEECH, TARGET_LANGUAGE_SPEECH, AUDIO_FILE, TARGET_LANGUAGE_AUDIO, AUDIO_FILE_SPEECH, TARGET_LANGUAGE_AUDIO_SPEECH = range(8)

# Fonction pour gérer la commande /text2text
def text2text(update, context):
    update.message.reply_text("Envoyez le texte que vous souhaitez traduire :")
    return TEXT

# Fonction pour demander la langue cible
def ask_target_language(update, context):
    text_to_translate = update.message.text

    # Sauvegarde du texte à traduire dans le contexte
    context.user_data['text_to_translate'] = text_to_translate

    update.message.reply_text("Entrez le code de la langue cible (par ex. fr_XX pour le français, en_XX, it_IT) :")
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

# Fonction pour gérer la commande /text2speech
def text2speech(update, context):
    update.message.reply_text("Envoyez le texte que vous souhaitez convertir en audio :")
    return TEXT_SPEECH

# Fonction pour demander la langue cible pour la conversion en audio
def ask_target_language_speech(update, context):
    text_to_convert = update.message.text

    # Sauvegarde du texte à convertir dans le contexte
    context.user_data['text_to_convert'] = text_to_convert

    update.message.reply_text("Entrez le code de la langue cible (par ex. fr_XX pour le français, en_XX, it_IT) :")
    return TARGET_LANGUAGE_SPEECH

# Fonction pour convertir le texte en audio et envoyer le fichier audio
def convert_to_speech(update, context):
    target_language_code = update.message.text

    # Récupération du texte à convertir depuis le contexte
    text_to_convert = context.user_data['text_to_convert']

    # Appel à la fonction text_to_speech avec les arguments requis
    audio_file = text_to_speech(text_to_convert, target_language_code)

    # Envoi du fichier audio à l'utilisateur
    update.message.reply_audio(open(audio_file, 'rb'))

    return ConversationHandler.END

# Fonction pour gérer la commande /speech2text
def speech2text(update, context):
    update.message.reply_text("Envoyez l'audio que vous souhaitez transcrire en texte :")
    return AUDIO_FILE

# Fonction pour demander la langue cible pour la transcription audio
def ask_target_language_audio(update, context):
    audio_file = update.message.voice.get_file()

    # Génération d'un nom de fichier unique basé sur la date et l'heure actuelles
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file_path = f"{current_time}_audio.ogg"

    # Sauvegarde du fichier audio dans le contexte
    audio_file.download(audio_file_path)
    context.user_data['audio_file'] = audio_file_path

    update.message.reply_text("Entrez le code de la langue cible (par ex. fr_XX pour le français, en_XX, it_IT) :")
    return TARGET_LANGUAGE_AUDIO

# Fonction pour transcrire l'audio en texte et envoyer la transcription
def transcribe_audio(update, context):
    target_language_code = update.message.text

    # Récupération du fichier audio depuis le contexte
    audio_file_path = context.user_data['audio_file']

    # Appel à la fonction speech_to_text avec les arguments requis
    transcribed_text = speech_to_text(audio_file_path, target_language_code)

    update.message.reply_text(f"Transcription audio : {transcribed_text}")

    return ConversationHandler.END

# Fonction pour gérer la commande /speech2speech
def speech2speech(update, context):
    update.message.reply_text("Envoyez l'audio que vous souhaitez traduire :")
    return AUDIO_FILE_SPEECH

# Fonction pour demander la langue cible pour la conversion audio à audio
def ask_target_language_audio_speech(update, context):
    audio_file = update.message.voice.get_file()

    # Génération d'un nom de fichier unique basé sur la date et l'heure actuelles
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file_path = f"{current_time}_audio.ogg"

    # Sauvegarde du fichier audio dans le contexte
    audio_file.download(audio_file_path)
    context.user_data['audio_file'] = audio_file_path

    update.message.reply_text("Entrez le code de la langue cible (par ex. fr_XX pour le français, en_XX, it_IT) :")
    return TARGET_LANGUAGE_AUDIO_SPEECH

# Fonction pour convertir l'audio en audio traduit et envoyer le fichier audio
def convert_to_audio_speech(update, context):
    target_language_code = update.message.text

    # Récupération du fichier audio depuis le contexte
    audio_file_path = context.user_data['audio_file']

    # Appel à la fonction speech_to_speech avec les arguments requis
    translated_audio_file = speech_to_speech(audio_file_path, target_language_code)

    # Envoi du fichier audio traduit à l'utilisateur
    update.message.reply_audio(open(translated_audio_file, 'rb'))

    return ConversationHandler.END

# Fonction principale pour démarrer le bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler_text = ConversationHandler(
        entry_points=[CommandHandler('text2text', text2text)],
        states={
            TEXT: [MessageHandler(Filters.text & ~Filters.command, ask_target_language)],
            TARGET_LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, translate_text)],
        },
        fallbacks=[],
    )

    conv_handler_speech = ConversationHandler(
        entry_points=[CommandHandler('text2speech', text2speech)],
        states={
            TEXT_SPEECH: [MessageHandler(Filters.text & ~Filters.command, ask_target_language_speech)],
            TARGET_LANGUAGE_SPEECH: [MessageHandler(Filters.text & ~Filters.command, convert_to_speech)],
        },
        fallbacks=[],
    )

    conv_handler_audio = ConversationHandler(
        entry_points=[CommandHandler('speech2text', speech2text)],
        states={
            AUDIO_FILE: [MessageHandler(Filters.voice & ~Filters.command, ask_target_language_audio)],
            TARGET_LANGUAGE_AUDIO: [MessageHandler(Filters.text & ~Filters.command, transcribe_audio)],
        },
        fallbacks=[],
    )

    conv_handler_audio_speech = ConversationHandler(
        entry_points=[CommandHandler('speech2speech', speech2speech)],
        states={
            AUDIO_FILE_SPEECH: [MessageHandler(Filters.voice & ~Filters.command, ask_target_language_audio_speech)],
            TARGET_LANGUAGE_AUDIO_SPEECH: [MessageHandler(Filters.text & ~Filters.command, convert_to_audio_speech)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler_text)
    dp.add_handler(conv_handler_speech)
    dp.add_handler(conv_handler_audio)
    dp.add_handler(conv_handler_audio_speech)

    # Démarrage du bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
