import requests
import base64

def Translation(tr_mode:int, text:str):

    translate = requests.get("https://translate.tatar/translate?lang="+str(tr_mode)+"&text=" + text)

    return translate.text

def Synth(text:str):

    response = requests.get('https://tat-tts.api.tatarby.tugantel.tatar/listening/?text='+text)

    with open('temp.wav',mode='bx') as f: #проблема в FileExistsError поэтому удаляйте предыдущий temp.wav
            f.write(base64.b64decode(response.text[15:response.text.find(',')])) #т.к. при вызове создаётся новый
            f.close()

    return 0
