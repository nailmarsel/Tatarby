import razdel
import pandas as pd

def tg_text_processing(text_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        counter = 0
        c_500 = 0
        file_str = file.read()
        new_file = file_str
        while counter < len(file_str):
            if file_str[counter] in '.?!:;' and 400 < c_500 < 500:
                c_500 = 0
                new_file[:counter + 1] + '|' + new_file[counter - 1:]
            else:
                c_500 += 1
            counter += 1

        with open('outp.txt', 'w') as outp_file:
            outp_file.write(new_file)


tg_text_processing(r"C:\Users\user\Downloads\tom1.txt")
def simple_processing():
    with open(r"C:\Users\user\Downloads\train_tat (1).txt", 'r', encoding='utf-8') as file:
        tat_lst = file.read().split('\n\n')
        tat_lst = [sent.strip().replace('\t', '') for sent in tat_lst]
        tat_lst = [sent for sent in tat_lst if sent != '' and not sent.isdigit() and not sent[0] == '[' and not sent[0].isdigit()]


        new_tat = []
        i = 1
        while i < len(tat_lst):
            if tat_lst[i - 1][-1] == ':':
                # print(tat_lst[i - 1])
                new_tat.append(tat_lst[i - 1] + tat_lst[i])
                # print(tat_lst[i - 1] + tat_lst[i])
                i += 1
            else:
                new_tat.append(tat_lst[i - 1])
            i += 1



        #print(tat_lst[49])
        print(len(tat_lst))

        print(new_tat[33])
        print(len(new_tat))


    print()
    print()
    print()
    print()
    print()
    print()


    with open(r"C:\Users\user\Downloads\train_rus (1).txt", 'r', encoding='utf-8') as file:
        rus_lst = file.read().split('\n\n')
        rus_lst = [sent.strip().replace('\t', '') for sent in rus_lst]
        rus_lst = [sent for sent in rus_lst if sent != '' and not sent.isdigit() and not sent[0] == '[']

        new_rus = []
        i = 1
        while i < len(rus_lst):
            if rus_lst[i - 1][-1] == ':':
                # print(i)
                new_rus.append(rus_lst[i - 1] + rus_lst[i])
                i += 1
            else:
                new_rus.append(rus_lst[i - 1])

            i += 1

        #print(rus_lst[50])
        print(len(rus_lst))

        print(new_rus[33])
        print(len(new_rus))


        with open('train.txt', 'w', encoding='utf-8') as file:
            for r, t in zip(new_rus[:34], new_tat[:34]):
                file.write(r + '\t' + t + '\n')
        return new_rus[:34], new_tat[:34]

with open(r"C:\Users\user\Downloads\train_rus.txt", 'r', encoding='utf-8') as file:
    sent_ru = list(x.text for x in razdel.sentenize(file.read()))
    #print(sent_ru[100])


print()
print()
print()
print()
print()
print()
print()
print()
print()


with open(r"C:\Users\user\Downloads\train_tat.txt", 'r', encoding='utf-8') as file:
    sent_tat = list(x.text for x in razdel.sentenize(file.read()))
    #print(sent_tat[100])



simple_processing()