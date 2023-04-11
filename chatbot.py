import configparser
import pymysql
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import configparser
import logging
import os

def main():
   
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    #updater = Updater(token='6003544672:AAFYUCXaALM9fgFtPZ9rHXz_Ft5r4z7OzAk', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

     # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("sights", sights_command))
    dispatcher.add_handler(CommandHandler("movies", movies_command))
    dispatcher.add_handler(CommandHandler("search", search_command))
    # To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Command:'+ '\n' + 
                              '/movies   Recommended Movies'+'\n'+
                              '/sights   Suggested places to visit in Hong Kong')

def sights_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Suggested places to visit in Hong Kong:' + '\n'+
                              '\n' + '1: Tai Ping Shan, Hong Kong' + 
                              'The top-ranked Hong Kong attraction by the Hong Kong Tourism Board and a favourite of tens of millions of visitors to Hong Kong.Take the Peak Tram to the Peak Tower Skyline for a night view of the million dollar Mount Tai Ping.' + '\n' +
                              '\n' + '2: Victoria Harbour' + '\n' +
                              'The world\'s largest musical light show "A Symphony of Lights" is a collaboration with 47 buildings in Victoria Harbour, combining laser lights, LED lights and background music.' +
                              'Over the past decade, the show has attracted over 4 million spectators. The most romantic attraction in Hong Kong is the quaint "Cheung Po Chai", where you can enjoy a cocktail.' + '\n'
                              '\n' + '3: Hong Kong Disneyland' + '\n' +
                              'The second Disney theme park in Asia after Tokyo Disneyland in Japan.' +
                              'It consists of seven themed areas, including Adventureland, Tomorrowland and Toy Story Land, with special events on Halloween and New Year\'s Eve.')

def movies_command(update: Update, context: CallbackContext) -> None:
    #connect to database
    #conn = pymysql.connect(host='localhost', user='root', password="hemi7940",db='7940', port=3306)
    
    conn = pymysql.connect(host=(os.environ['LOCAL']), 
                           user=(os.environ['USER']), 
                           password=(os.environ['PASSWORD']),
                           db=(os.environ['DB']), 
                           port=3306)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT movie_type FROM movie;")
    tlists= cursor.fetchall()

    update.message.reply_text('Which type of movie would you want to know?🤔')
       
    logging.info(tlists)
    for type in tlists:    
        update.message.reply_text('/search '+str(type)[2:-3])
    conn.close()
    update.message.reply_text('Please copy one of the above messages and send it!')
    
def search_command(update: Update, context: CallbackContext) -> None:
    conn = pymysql.connect(host=(os.environ['LOCAL']), 
                           user=(os.environ['USER']), 
                           password=(os.environ['PASSWORD']),
                           db=(os.environ['DB']), 
                           port=3306)
    cursor = conn.cursor()
    logging.info(str(context.args[0]))
    cursor.execute('SELECT * FROM movie WHERE movie_type=\''+str(context.args[0])+'\';')
    mlists= cursor.fetchall() 
    for row in mlists:   
        update.message.reply_text(row[1] + ' movies with an overall rating of ' + str(row[2]) + ' out of 10 《' + row[0] + '》')
    
if __name__ == '__main__':
    main()