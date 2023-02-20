from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
from talib.abstract import *
import pandas as pd
import numpy as np
import time
import talib

#LOGIN E SENHA
my_user = input("Login: ")
my_pass = input("Senha: ")

#CONFIGURAÇÃO SE ESTÁ LOGADO OU NÃO
Iq=IQ_Option(my_user,my_pass)
iqch1,iqch2=Iq.connect()
if iqch1==True:
  print("logado ( ͡ ° ͜ʖ ͡ °)")
else:
  print("login failed ┌( ಠ_ಠ)-💣")
  
#BANCA TOTAL
my_blc=Iq.get_balance()
print(f"BANCA TOTAL: {my_blc} ")

#QUER O MODO PRATICO OU REAL
changeB = input("Pratica ou Real? 1- Pratica 2- Real:") 
if changeB == '1':
    changeBs = 'PRACTICE'
elif changeB == '2':
    changeBs = 'REAL'

# Vai usar dinheiro FICTICIO OU REAL = PRACTICE / REAL
Iq.change_balance(changeBs) 

#ESCOLHA O VALOR DE ENTRADA
valorPR = input("Escolha o valor de entrada :")

total_ganho = 0
vitoria = 0
vitoriaV = 0
perdaV = 0
perda = 0

# valor de aposta inicial
valor_aposta = float(valorPR)

# número máximo de perdas consecutivas permitidas
max_perdas_consecutivas = 3

# número atual de perdas consecutivas
perdas_consecutivas = 0


#ESCOLHA QUAL MOEDA
def BinDig(): 
    OptionBD = "1"
    global par 
    if OptionBD == '1': 
        OptionBx = input("Escolha a opção Digital: 1-USD/CAD 2-EUR/USD 3-AUD/CAD 4-AUD/JPY 5-EUR/AUD 6-EUR/GBP 7-GBP/USD 8-GBP/JPY 9-EUR/USD-OTC 10-EUR/JPY-OTC 11-AUD/CAD-OTC: ")
        if OptionBx == '1':
            parX = 'USDCAD'
        elif OptionBx == '2':
            parX = 'EURUSD'
        elif OptionBx == '3':
            parX = 'AUDCAD'
        elif OptionBx == '4':
            parX = 'AUDJPY'
        elif OptionBx == '5':
            parX = 'EURAUD'
        elif OptionBx == '6':
            parX = 'EURGBP'
        elif OptionBx == '7':
            parX = 'GBPUSD' 
        elif OptionBx == '8':
            parX = 'GBPJPY' 
        elif OptionBx == '9':
            parX = 'EURUSD-OTC'
        elif OptionBx == '10':
            parX = 'EURJPY-OTC' 
        elif OptionBx == '11':
            parX = 'AUDCAD-OTC'
        
        par = parX
        print('Voce selecinou a opção:'+OptionBx+'-'+par)
        print('...Aguarde.')
BinDig()



# AQUI É AONDE A FUNÇÃO FAZ APOSTAR PRA SUBIR - OPÇÃO DIGITAL!
def apostarSubirD():
    #par="AUDUSD"
    duration=1#minute 1 or 5
    amount=valorPR
    action="call"#put
    
    global vitoria
    global vitoriaV
    global perda
    global perdaV
    global total_ganho
    
    liquidoD = vitoria - perda
    liquidoVD = vitoriaV - perdaV
    
    if liquidoD <= (-3):
        PerdaD = input("Vc ja ta perdendo R$ "+str(liquidoVD)+", deseja continuar? 1-Não   2-Sim: ")
        if PerdaD == '1':
            pausar()
        elif PerdaD == '2': 
            perda = 0
            BinDig()
            
    _,id=(Iq.buy_digital_spot(par,amount,action,duration))
    if 'expiration_out_of_schedule' in str(id):
        print('Expirado para aposta, redirecionando...')
    print(id)
    print("__DIGITAL_APOSTOU_LONG__")
    if id !="error":
        while True:
            check,win=Iq.check_win_digital_v2(id)
            if check==True:
                break
        if win<0:
            perda += 1
            perdaV += win
            print("Você perdeu "+str(win)+"$")
            total_ganho += win
            print("Ganho atual: R$", total_ganho)
            time.sleep(10)
        else:
            vitoria += 1
            vitoriaV += win
            print("Você ganhou "+str(win)+"$")
            total_ganho += win
            print("Ganho atual: R$", total_ganho)
            time.sleep(10)
    
    else:
        print('EMPATE - Robô parado')
        pausar()

# AQUI É AONDE A FUNÇÃO FAZ APOSTAR PRA DESCER - OPÇÃO DIGITAL!
def apostarDescerD():
    #par="AUDUSD"
    duration=1#minute 1 or 5
    amount=valorPR
    action="put"#call 
    global vitoria
    global vitoriaV
    global perda
    global perdaV
    global total_ganho
    
    liquidoD = vitoria - perda
    liquidoVD = vitoriaV - perdaV
    
    if liquidoD <= (-3):#SE VC PERDER 3 SEGUIDAS O ROBO DA UMA PARADA E PERGUNTA SE DESEJA CONTINUAR
        PerdaD = input("Vc ja ta perdendo R$ "+str(liquidoVD)+", deseja continuar? 1-Não   2-Sim: ")
        if PerdaD == '1':
            pausar()
        elif PerdaD == '2': 
            perda = 0
            BinDig()    
    
    _,id=(Iq.buy_digital_spot(par,amount,action,duration))
    if 'expiration_out_of_schedule' in str(id):
        print('Expirado para aposta, redirecionando...')
    print(id)
    print("__DIGITAL_APOSTOU_SHORT__")
    if id !="error":
        while True:
            check,win=Iq.check_win_digital_v2(id)
            if check==True:
                break
        if win<0:
            perda += 1
            perdaV += win
            print("Você perdeu "+str(win)+"$")
            total_ganho += win
            print("Ganho atual: R$", total_ganho)
            time.sleep(10) #TIME DE 180 SEGUNDOS
        else:
            vitoria += 1
            vitoriaV += win
            print("Você ganhou "+str(win)+"$")
            total_ganho += win
            print("Ganho atual: R$", total_ganho)
            time.sleep(10)
    else:
        print('EMPATE - Robô parado')


size = 60 #periodo da vela
timeperiod = 9 #periodo do rsi

print("Starting stream...")
Iq.start_candles_stream(par, size, maxdict=60)

def pausar():
    pausado = input("Programa pausado, deseja continuar? 1- Sim 2- Não:")
    if pausado == '1':
        BinDig()
    elif pausado == '2':
        print('Obrigado pelo uso do robô, pode fechar o programa :-)')


while True:
    candles = Iq.get_realtime_candles(par, size)
    inputs = {
        'close': np.array([]),
        'high': np.array([]),
        'low': np.array([]),
        'volume': np.array([])
    }
    for timestamp, candle in candles.items():
        inputs["close"] = np.append(inputs["close"], candle["close"])
        inputs["high"] = np.append(inputs["high"], candle["max"])
        inputs["low"] = np.append(inputs["low"], candle["min"])
        inputs["volume"] = np.append(inputs["volume"], candle["volume"])

    rsi = talib.RSI(inputs["close"], timeperiod=timeperiod)
    print("RSI:", rsi[-1], end='\r')
    time.sleep(2)

    if rsi[-1] > 70:
        apostarDescerD()
    elif rsi[-1] < 30:
        apostarSubirD()
        


