from Translate import translate_text,synth_tatar_speach,translate_other
import os
import sqlite3
import io

class Book:


    def __init__(self, book_id: int, bookname: str, description: str, content: str, authorid: int, year:int):
        self.book_id = book_id
        self.bookname = {
            "ru": [],
            "tat": []
        }
        self.bookname["ru"] = bookname
        self.bookname["tat"] = translate_other(0, bookname)
        self.description = {
            "ru": [],
            "tat": []
        }
        with open(description,'r') as file:
            txt=file.read()
            self.description["ru"] = txt
            self.description["tat"] = translate_other(0, txt)
        self.content = content
        self.authorid = int(authorid)
        self.year = year
        self.pages = {
            "ru": [],
            "tat": [],
            "audio_ru": [],
            "audio_tat": []
        }
        counter=0
        actual_page=""
        page=0
        conn = sqlite3.connect('/home/ips/projects/bd/Tatarby/hachaton/tatarlit.db')

        file=open(content,"r")
        txt=file.read()
        splited=txt.split(' ')
        print(self.bookname["ru"])
        for spl in splited:
            if len(spl)+counter>700:
                self.pages["ru"].append(actual_page)
                self.pages["tat"].append(translate_text(0,actual_page,self.book_id,page,conn))
                self.pages["audio_tat"].append(synth_tatar_speach(translate_text(0,actual_page,self.book_id,page,conn),
                                                  f'''/home/ips/projects/bd/Tatarby/hachaton/audiofiles/{book_id}_{page}_tat.wav'''))
                self.pages["audio_ru"].append(synth_tatar_speach(translate_text(0,actual_page,self.book_id,page,conn),
                                                  f'''/home/ips/projects/bd/Tatarby/hachaton/audiofiles/{book_id}_{page}_tat.wav'''))
                actual_page=spl
                counter=len(spl)
                page+=1
                print(page)
            else:
                actual_page+=" "+spl
                counter+=len(spl)+1
                    
        if actual_page!="":
            self.pages["ru"].append(actual_page)
            self.pages["tat"].append(translate_text(0,actual_page,self.book_id,page,conn))
            self.pages["audio_tat"].append(synth_tatar_speach(translate_text(0,actual_page,self.book_id,page,conn),
                                                  f'''/home/ips/projects/bd/Tatarby/hachaton/audiofiles/{book_id}_{page}_tat.wav'''))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Author WHERE AuthorID=?",(self.authorid,))
        for i in cursor.fetchall():
            author_id, aname, asurname, amiddlename, dateofbirth, astyle = i
            self.author = Author(author_id, aname, asurname, amiddlename, dateofbirth, astyle)
    
        cursor.close()
        conn.close() 
    def to_string(self, language):
        return f"""{self.bookname[language]}
        
{self.author.get_author_string()}

{self.description[language]}

/book{self.book_id}"""

    
class Author:


    def __init__(self, author_id: int, aname: str, asurname: str, amiddlename: str, dateofbirth: str, astyle: str):
        self.author_id=author_id
        self.aname=aname
        self.asurname=asurname
        self.amiddlename=amiddlename
        self.dateofbirth=dateofbirth
        self.astyle=astyle
        
    def get_author_string(self):
        return f"""{self.asurname} {self.aname} {self.amiddlename} {self.dateofbirth}
                style: {self.astyle}"""
        
        
        