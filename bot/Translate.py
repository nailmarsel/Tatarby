import requests
import base64
import os.path
import sqlite3

def translate_other(tr_mode:int, text:str):
   
    text = text.replace(':', '')
    text = text.replace('"', '')
    text = text.replace('-', '')
    text = text.replace('—', '')
    text = text.replace(';', '')
    text = text.replace('\t', '')
    translate = requests.get("https://translate.tatar/translate?lang="+str(tr_mode)+"&text=" + text)
    text = translate.text
    if '<mt>' in text:
        text=text[
            translate.text.find("<mt>")+4: translate.text.rfind("</mt>")
        ]
        
    
    return text
    
def translate_text(tr_mode:int, text:str,book_id:int,page:int,conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TatarTranslation WHERE BookID=? and TatPage=?",(book_id,page,))
    result=cursor.fetchall()
    if len(result)>0:
        return result[0][1]
    else:
        text = text.replace(':', '')
        text = text.replace('"', '')
        text = text.replace('-', '')
        text = text.replace('—', '')
        text = text.replace(';', '')
        text = text.replace('\t', '')
        translate = requests.get("https://translate.tatar/translate?lang="+str(tr_mode)+"&text=" + text)
        text = translate.text
        if '<mt>' in text:
            text=text[
                translate.text.find("<mt>"): translate.text.rfind("</mt>")
            ]
        cursor.execute("INSERT INTO TatarTranslation VALUES (?,?,?,?)",(book_id,text,page,None,))
        conn.commit()
        cursor.close()
        return text

def synth_tatar_speach(text:str, path: str):
    if not os.path.exists(path):
        
        response = requests.get('https://tat-tts.api.translate.tatar/listening/?text='+text)

        with open(f'{path}' ,mode='wb') as f: #проблема в FileExistsError поэтому удаляйте предыдущий temp.wav
                f.write(base64.b64decode(response.text[15:response.text.find(',')])) #т.к. при вызове создаётся новый

    return path