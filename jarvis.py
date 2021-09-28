"""
Jarvis by Gabriel Lima
"""
import speech_recognition as sr
import pyttsx3
import requests
import random
import webbrowser
import os
import speedtest
import pyautogui
from time import sleep


def receber():
    # grava e salva a voz
    r = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("Diga algo: ")
        audio = r.listen(fonte)
        with open('fala.wav', 'wb') as f:
            f.write(audio.get_wav_data())
    path = 'fala.wav'
    return path


def convert(path):
    # converte a voz em texto
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio_data = r.record(source)
        text = (r.recognize_google(audio_data, language="pt-BR")).lower()
    return text


def convert_texto(texto):
    # converte texto em voz
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()


def previsao(path):
    token = ''
    convert_texto('Qual a sua cidade?')
    receber()
    city = convert(path)
    url = 'http://api.openweathermap.org/data/2.5/weather?&appid=' + token + '&q=' + city + '&units=metric&lang=pt_br'
    requisicao_clima = requests.get(url)
    clima = requisicao_clima.json()
    if clima["cod"] != "404":
        desc = clima["weather"]
        temp_atual = round((clima["main"]["temp"]))
        temp_min = round((clima["main"]["temp_min"]))
        temp_max = round((clima["main"]["temp_max"]))
        descricao = desc[0]["description"]
        convert_texto(f'A Temperatura atual em {city} é de {temp_atual} graus\n'
                      f'com Temperatura minima de {temp_min} graus\n'
                      f'e Temperatura máxima de {temp_max} graus\n'
                      f'com {descricao}')
    else:
        print("Cidade não encontrada")


def youtube(path):
    convert_texto('Qual a música ou cantor deseja ouvir?')
    receber()
    saida = convert(path)
    webbrowser.open('https://www.youtube.com/results?search_query=' + saida)
    sleep(5)
    pyautogui.press('tab')
    sleep(2)
    pyautogui.press('enter')


def google(path):
    convert_texto('O que deseja pesquisar no google?')
    receber()
    saida = convert(path).replace(' ', '+')
    webbrowser.open('https://www.google.com/search?q=' + saida)


def jarvis(text, path):
    if text == 'bom dia':
        words = ("Tenha um excelente dia", "Bom dia", "Tenha uma dia fantástico", "Tenha um dia maravilhoso",
                 "Tenha um dia significativo")
        bom_dia = random.choice(words)
        convert_texto(bom_dia)
    elif text == 'boa noite':
        words = ("Boa noite", "Boa noite, durma bem", "Bons sonhos", "Tenho um bom sono de beleza",
                 "Bom descanso")
        boa_noite = random.choice(words)
        convert_texto(boa_noite)
    elif text == 'boa tarde':
        words = ("Tenha uma excelente tarde", "Boa tarde", "Espero que seu dia esteja sendo maravilhoso")
        boa_tarde = random.choice(words)
        convert_texto(boa_tarde)
    elif text == 'qual o valor do dólar':
        convert_texto('Procurando o valor do Dolar')
        requisicao_dolar = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
        cotacao_dolar = requisicao_dolar.json()
        convert_texto('O valor atual do euro é de:' + cotacao_dolar['USD']['bid'] + 'reais')
    elif text == 'qual o valor do euro':
        convert_texto('Procurando o valor do Euro')
        requisicao_euro = requests.get('https://economia.awesomeapi.com.br/all/EUR-BRL')
        cotacao_euro = requisicao_euro.json()
        convert_texto('O valor atual do euro é de:' + cotacao_euro['EUR']['bid'] + 'reais')
    elif text == 'qual o valor da libra':
        convert_texto('Procurando o valor da Libra')
        requisicao_libra = requests.get('https://economia.awesomeapi.com.br/all/GBP-BRL')
        cotacao_libra = requisicao_libra.json()
        convert_texto('O valor atual do euro é de:' + cotacao_libra['GBP']['bid'] + 'reais')
    elif text == 'abrir o chrome' or text == 'abra o chrome':
        convert_texto('Abrindo o Chrome')
        os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
    elif text == 'abrir o player de vídeo' or text == 'abrir player de video':
        convert_texto('Abrindo o player de video')
        os.startfile("C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe")
    elif text == 'abrir o youtube' or text == 'abra o youtube':
        youtube(path)
    elif text == 'qual a velocidade da internet' or text == 'teste de internet':
        convert_texto('Realizando o teste de internet')
        test = speedtest.Speedtest()
        down = test.download()
        rs_down = round(down)
        f_down = int(rs_down / 1e+6)
        f_down = str(f_down)
        upload = test.upload()
        rs_up = round(upload)
        f_up = int(rs_up / 1e+6)
        f_up = str(f_up)
        convert_texto('Sua velocidade de download é de' + f_down + 'Mb/s')
        convert_texto('Sua velocidade de upload é de' + f_up + 'Mb/s')
    elif text == 'qual a previsão do tempo' or text == 'previsão do tempo':
        previsao(path)
    elif text == 'jéssica':
        convert_texto('Oi Gabriel, como posso ajudar?')
    elif text == 'google':
        google(path)
    elif text == 'parar':
        exit()
    else:
        convert_texto('Não sei nada sobre isso')


def inicio():
    while True:
        caminho = receber()
        voz_texto = convert(caminho)
        jarvis(voz_texto, caminho)
        continue


inicio()
