import telebot
from telebot import types
import Translate
from book import Book
import os 
import sqlite3
import sqlite3                                                                                                          
from flask import Flask                                                                                                 
from contextlib import closing    
import poisk
import sys
import random
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/ips/projects/bd/Tatarby/hachaton')

from initdb import connect_db
sys.path.insert(1, '/home/ips/projects/bd/Tatarby/bot')

# stable_dif.init()

bot = telebot.TeleBot('6616135293:AAF5sIwAMVvBVY_70Dgq8dnv2UsdpjUPfOs')

ru = "ru"
tat = "tat"

liked = "liked"
advice = "advice"
top = "top"
search = "search"
back = "back"
selected = "selected"
languages_keyboard_text = {ru: 'Русский язык', tat: 'Татарча'}

menu_text = {
    "options": {
        ru: "Что вас интересует?",
        tat: "Cезне нәрсә кызыксындыра?"
    },
    "language_change": {
        ru: "Ваш язык  изменён на русский",
        tat: "Татар теленә үзгәртелде"
    }
}

options_text = {
    liked: {
        ru: "Начатые книги",
        tat: "Башылган китаплар"
    },
    selected: {
        ru: "Избранные книги",
        tat: "Сайланган китаплар"
    },
    advice: {
        ru: "Посоветовать книгу",
        tat: "Китап киңәшерю"
    },
    top: {
        ru: "Популярные",
        tat: "Танылган"
    },
    search: {
        ru: "Поиск",
        tat: "Эзләү"
    },
    back: {
        ru: "Назад",
        tat: "Артка"
    }
}

extra = {
    "no_page": {
        ru: "Страницы нет",
        tat: "Битләр юк"
    }
}

books = {}
DATABASE = './tatarlit.db'                                                                  
DEBUG = True
# create our little application :)                                                                                      
app = Flask(__name__)                                                                                                   
app.config.from_object(__name__)             


def connect_db():   
        return sqlite3.connect('/home/ips/projects/bd/Tatarby/hachaton/tatarlit.db')
        
    


def init_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book")
    for i in cursor.fetchall():
        
        book_id, book_name, description, content, author_id, year_ofw = i
        with open(content, 'r', encoding="utf-8") as file:
 
            books[book_id] = Book(int(book_id), book_name, description, content, author_id, year_ofw)
    cursor.close()
    conn.close()

init_books()

def check_user(user_id,conn):
    cursor = conn.cursor()
    x = cursor.execute("SELECT COUNT(*) FROM Users WHERE UserID = ?",(user_id,)).fetchall()[0][0]==1
    cursor.close()
    return x
                          
def get_user(user_id,username,conn):
    cursor = conn.cursor()
    c = cursor.execute("SELECT COUNT(*) FROM Users WHERE UserID = ?",(user_id,)).fetchall()[0][0]
    if c!=0:
        c = cursor.execute("SELECT Language FROM Users WHERE UserID = ?",(user_id,)).fetchall()[0][0]
        cursor.close()
        return {"language":c}
    else:
        cursor.execute("INSERT INTO Users VALUES (?,?,?)",(user_id,username,"ru",))
        conn.commit()
        cursor.close()
        return {"language": ru}
    
def save_user(user_id, user,conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Language = ? WHERE UserID=?",(user["language"],user_id,))
    conn.commit()
    cursor.close()
    
def get_language(user_id,username,conn):
    return get_user(user_id,username,conn)["language"]


users1 = {}


def change_language_keyboard():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=languages_keyboard_text[tat], callback_data=tat)
    btn2 = types.InlineKeyboardButton(text=languages_keyboard_text[ru], callback_data=ru)
    markup.add(btn1, btn2)

    return markup


def options_key_board(lang):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text=options_text[liked][lang], callback_data=liked)
    btn2 = types.InlineKeyboardButton(text=options_text[advice][lang], callback_data=advice)
    btn3 = types.InlineKeyboardButton(text=options_text[top][lang], callback_data=top)
    btn4 = types.InlineKeyboardButton(text=options_text[search][lang], callback_data=search)
    btn5 = types.InlineKeyboardButton(text=options_text[selected][lang], callback_data=selected)
    
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    markup.add(btn5)

    return markup

def options_key_board_back(lang):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text=options_text[back][lang], callback_data=back)
    markup.add(btn1)

    return markup


controls_keyboard_text = {
    "next": {
        ru: "Далее▶️",
        tat: "Алга▶️"
    },
    "prev": {
        ru: "◀️Назад",
        tat: "◀️Артка"
    },
    "mark": {
        ru: "Оценить книгу",
        tat: "Китапны бәяләү"
    },
    "select": {
        ru: "Добавить книгу в избранные",
        tat: "Сайланганнарга Китап өстәргә"
    },
    "select-no": {
        ru: "Убрать книгу из избранных",
        tat: "Сайланганнардан китапны алып ташлау"
    },
}


def feedback_controls(book_id, page,command,flag):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='1', callback_data=f"mark:1:{command}:{book_id}:{page}:{flag}")
    btn2 = types.InlineKeyboardButton(text='2', callback_data=f"mark:2:{command}:{book_id}:{page}:{flag}")
    btn3 = types.InlineKeyboardButton(text='3', callback_data=f"mark:3:{command}:{book_id}:{page}:{flag}")
    btn4 = types.InlineKeyboardButton(text='4', callback_data=f"mark:4:{command}:{book_id}:{page}:{flag}")
    btn5 = types.InlineKeyboardButton(text='5', callback_data=f"mark:5:{command}:{book_id}:{page}:{flag}")
    markup.add(btn1,btn2,btn3,btn4,btn5)

    return markup

def book_controls(book_id, page, language,user_id):
    conn = connect_db()
    cursor = conn.cursor()
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=controls_keyboard_text["next"][language], callback_data=f"controls:next:{book_id}:{page}")
    btn2 = types.InlineKeyboardButton(text=controls_keyboard_text["prev"][language], callback_data=f"controls:prev:{book_id}:{page}")
    btn31 = types.InlineKeyboardButton(text=controls_keyboard_text["select"][language], callback_data=f"controls:select:{book_id}:{page}")
    btn32 = types.InlineKeyboardButton(text=controls_keyboard_text["select-no"][language], callback_data=f"controls:select-no:{book_id}:{page}")
    btn4 = types.InlineKeyboardButton(text=languages_keyboard_text[tat], callback_data=f"controls:tat:{book_id}:{page}")
    btn5 = types.InlineKeyboardButton(text=languages_keyboard_text[ru], callback_data=f"controls:ru:{book_id}:{page}")
    btn6 = types.InlineKeyboardButton(text=controls_keyboard_text["mark"][language], callback_data=f"controls:mark:{book_id}:{page}")
    markup.add(btn2, btn1)
    if cursor.execute("SELECT COUNT(*) FROM SelectedBook WHERE UserID=? and BookID=?",(user_id,book_id,)).fetchall()[0][0]==0:
        markup.add(btn31)
    else:
        markup.add(btn32)              
    if language == ru:
        markup.add(btn4)
    else:
        markup.add(btn5)
    cursor.close()
    conn.close()
    #markup.add(btn6)

    return markup

def change_language(message):
    bot.send_message(message.from_user.id, "Выберите язык\n\nТелне сайлагыз", reply_markup=change_language_keyboard())


def ask_options(user_id, language):
    bot.send_message(user_id, menu_text["options"][language], reply_markup=options_key_board(language))

@bot.message_handler(commands=['menu'])
def menu(message):
    conn=connect_db()
    language = get_language(message.from_user.id,message.from_user.username,conn)
    ask_options(message.from_user.id, language)
    conn.close()
@bot.message_handler(commands=['start'])
def start(message):
    conn=connect_db()
    bot.send_message(message.from_user.id,
                     "Здравствуйте и Исәнмесез\n\nДля того что бы изменить язык нажмите /settings\n\nТелне үзгәртү өчен, /settings басыгыз")
    language = get_language(message.from_user.id,message.from_user.username,conn)
    ask_options(message.from_user.id, language)
    conn.close()
    
@bot.message_handler(commands=['settings'])
def settings(message):
    change_language(message)


@bot.message_handler(func=lambda message: message.text.startswith("/book"))
def open_book(message):
    conn = connect_db()
    cursor = conn.cursor()
    
    user=get_user(message.from_user.id,message.from_user.username,conn)
    cid = message.chat.id
    mid = message.message_id
    book_id = int(message.text[5:])
    language = get_language(message.from_user.id,message.from_user.username,conn)
    user_id = message.from_user.id
    
    cursor.execute("SELECT COUNT(*) FROM CurrentBook WHERE UserID=? and BookID=?",(int(user_id),book_id,))
    if cursor.fetchall()[0][0]==0:
        cursor.execute("""INSERT INTO CurrentBook                                                                                              VALUES (?, ?, ?);""", (user_id,book_id,0))
        page=0
        conn.commit()
    else:
        cursor.execute("SELECT PageNumber FROM CurrentBook WHERE UserID=? and BookID=?",(user_id,book_id,))
        page=cursor.fetchall()[0][0]
    
    user = get_user(message.from_user.id,message.from_user.username,conn)
    save_user(message.from_user.id, user,conn)

    text = books[book_id].pages[language][page]

    cursor.execute("SELECT TatAudioId FROM TatarTranslation WHERE BookID=? and TatPage = ?",(int(book_id),page,)) # 
    result=cursor.fetchall()[0][0]
    if result==None:
            
        with open(books[book_id].pages["audio_tat"][page], "rb") as file:
            msg=bot.send_audio(message.from_user.id,audio=file, caption=text, reply_markup=book_controls(book_id, page, language,user_id))
            audio_id=msg.audio.file_id
            cursor.execute("UPDATE TatarTranslation SET TatAudioId=? WHERE BookID=? and TatPage = ? ",(audio_id,int(book_id),page,)) 
            conn.commit()
    else:
        bot.send_audio(message.from_user.id,audio=result, caption=text, reply_markup=book_controls(book_id, page, language,user_id))
    
    #bot.send_message(chat_id=cid, text=text,
                             #reply_markup=book_controls(book_id, page, language)) #audio=file
    cursor.close()
    conn.close() 

@bot.callback_query_handler(func=lambda call: call.data in [liked,selected, advice, top, search, back])
def callback1(call):
    conn = connect_db()
    cursor = conn.cursor()
    
    liked_books=[]
    language = get_language(call.from_user.id,call.from_user.username,conn)
    user = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id
    
    
    
    if call.data == back:
        bot.edit_message_text(chat_id=cid, message_id=mid, text=menu_text["options"][language], reply_markup=options_key_board(language))
    elif call.data == selected:
        
        cursor.execute("SELECT BookID FROM SelectedBook WHERE UserID=?",(int(user),))
        result=cursor.fetchall()
        for res in result:
            liked_books.append(books[res[0]])
        if len(liked_books)>0:
            bot.edit_message_text(chat_id=cid, message_id=mid, text="\n\n\n".join([i.to_string(language) for i in liked_books]), reply_markup=options_key_board_back(language))
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='У вас нет книг в списке избранных')
        
    elif call.data == liked:
        cursor.execute("SELECT BookID FROM CurrentBook WHERE UserID=? ",(int(user),))
        result=cursor.fetchall()
        for res in result:
            liked_books.append(books[res[0]])
        if len(liked_books)>0:
            [bot.send_message(chat_id=cid, text=i.to_string(language)) for i in list(set(liked_books))[:5]]
            ask_options(user,language)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Вы пока не начали читать книги')

    elif call.data == advice:
        [bot.send_message(chat_id=cid, text=i.to_string(language)) for i in random.sample(list(set(books.values())), 5)]
        ask_options(user,language)
    elif call.data == top:
        [bot.send_message(chat_id=cid, text=i.to_string(language)) for i in list(set(books.values()))[:5]]
        ask_options(user,language)
    elif call.data == search:
        if language == tat:
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Табарга теләгән китапның исемен языгыз", reply_markup=options_key_board_back(language))
        else:
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Напишите название книги, которую хотите найти", reply_markup=options_key_board_back(language))

    bot.answer_callback_query(callback_query_id=call.id, text='<3')
    cursor.close()
    conn.close()

@bot.callback_query_handler(func=lambda call: call.data in [ru, tat])
def callback_language(call):
    
    conn=connect_db()
    user = get_user(call.from_user.id,call.from_user.username,conn)
    user["language"] = call.data
    save_user(call.from_user.id, user,conn)

    bot.answer_callback_query(callback_query_id=call.id, text=menu_text["language_change"][call.data])

    ask_options(call.from_user.id, call.data)
    conn.close()
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("mark"))
def feed_back(call):
    cont, mark, command, book_id, page, flag = call.data.split(":")
    page=int(page)
    user_id=int(call.from_user.id)
    book_id = int(book_id)
    conn = connect_db()
    cursor = conn.cursor()
    print(flag,type(flag))
    if flag=='1':
        result=cursor.execute("SELECT COUNT(*) FROM TranslationMark").fetchall() # 
        cursor.execute("INSERT INTO TranslationMark VALUES (?,?,?,?)",(str(int(result[0][0])+1),book_id,str(mark),None,)) # 
        conn.commit()
    else:
        result=cursor.execute("SELECT COUNT(*) FROM BookMark").fetchall() # 
        cursor.execute("INSERT INTO BookMark VALUES (?,?,?,?,?)",(str(int(result[0][0])+1),book_id,str(mark),None,user_id)) # 
        conn.commit()
    cursor.close()
    conn.close()
    bot.delete_message(call.message.chat.id, call.message.message_id)
    flip_pages(users1[user_id])
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("controls"))
def flip_pages(call):
    conn = connect_db()
    cursor = conn.cursor()

    cont, command, book_id, page = call.data.split(":")
    page=int(page)
    user_id=int(call.from_user.id)
    cid = call.message.chat.id
    mid = call.message.message_id
    book_id = int(book_id)
    book = books[book_id]
    
    
    
    language = get_language(call.from_user.id,call.from_user.username,conn)
    drop=random.randint(1,10)
    cursor.execute("SELECT COUNT(*) FROM BookMark WHERE UserID=? and BookID=?",(user_id,book_id,))
    if page == (len(book.pages[language]) - 2) and cursor.fetchall()[0][0]==0:
        users1[user_id]=call
        bot.send_message(call.from_user.id, text='Оцените, пожалуйста, книгу от 1 до 5\n\n', reply_markup=feedback_controls(book_id, page, command, 0))
    if drop==1 and language=='tat':
        if page == 0 and command == "prev" or command == "next" and page == len(book.pages[language]) - 1:
            
            bot.answer_callback_query(callback_query_id=call.id, text=extra["no_page"][language], show_alert=True)
            return
        else:
            users1[user_id]=call
            if command == "prev":
                page1=page-1
            else:
                page1=page+1
            bot.send_message(call.from_user.id, text='Оцените, пожалуйста, перевод выше написанного текста от 1 до 5\n\n'+book.pages['ru'][page1], reply_markup=feedback_controls(book_id, page1, command, 1))
            
    if command == "ilus":

        return

    if command == tat or command == ru:
        user = get_user(call.from_user.id,call.from_user.username,conn)
        user["language"] = command
        save_user(call.from_user.id, user,conn)
        
    if page == len(book.pages[language]) - 1:
        cursor.execute("INSERT INTO ReadBook VALUES (?,?)",(int(user_id),int(book_id),))
        cursor.execute("DELETE FROM SelectedBook WHERE UserID=? and BookID=?",(int(user_id),int(book_id),))
        conn.commit()
    if command == "prev":
        if page == 0:
            bot.answer_callback_query(callback_query_id=call.id, text=extra["no_page"][language], show_alert=True)
            return
        page -= 1
    elif command == "next":
        if page == len(book.pages[language]) - 1:
            bot.answer_callback_query(callback_query_id=call.id, text=extra["no_page"][language], show_alert=True)
            return
        page += 1
    language = get_language(call.from_user.id,call.from_user.username,conn)
    text = book.pages[language][page]
    user=get_user(call.from_user.id,call.from_user.username,conn)
    save_user(call.from_user.id, user,conn)
    if command == "next" or command == "prev":
        cursor.execute("SELECT TatAudioId FROM TatarTranslation WHERE BookID=? and TatPage = ?",(int(book_id),page,)) # 
        result=cursor.fetchall()[0][0]
        if result==None:
            
            with open(book.pages["audio_tat"][page], "rb") as file:
                msg=bot.edit_message_media(chat_id=cid, message_id=mid, media=types.InputMediaAudio(file))
                audio_id=msg.audio.file_id
                cursor.execute("UPDATE TatarTranslation SET TatAudioId=? WHERE BookID=? and TatPage = ? ",(audio_id,int(book_id),page,)) 
                conn.commit()
        else:
            bot.edit_message_media(chat_id=cid, message_id=mid, media=types.InputMediaAudio(result))
    elif command == "select":
        cursor.execute("INSERT INTO SelectedBook VALUES (?,?)",(user_id,book_id,))
        conn.commit()
    elif command == "select-no":
        cursor.execute("DELETE FROM SelectedBook WHERE UserID=? and BookID=?",(user_id,book_id,))
        conn.commit()
        
    sql_update_query = """UPDATE CurrentBook SET PageNumber = ? WHERE UserID = ? and BookID = ?"""
    cursor.execute(sql_update_query,(page, user_id, book_id))
    conn.commit()
    bot.edit_message_caption(chat_id=cid, message_id=mid, caption=text,
                             reply_markup=book_controls(book_id, page, language,user_id))
    #bot.edit_message_text(chat_id=cid, message_id=mid, text=text, reply_markup=book_controls(book_id, page, language))
    #bot.answer_callback_query(callback_query_id=call.id, text="...")
    cursor.close()
    conn.close() 

@bot.message_handler(content_types=['text'])
def start_handler(message):
    conn=connect_db()
    language = get_language(message.from_user.id,message.from_user.username,conn)

    a = poisk.poisk(message.text, books)
    [bot.send_message(message.from_user.id, text=i.to_string(language),reply_markup=options_key_board_back(language)) for i in a]
    ask_options(message.from_user.id,language)
    conn.close()

if __name__ == '__main__':
    print("started")
    bot.polling(none_stop=True, interval=0)
