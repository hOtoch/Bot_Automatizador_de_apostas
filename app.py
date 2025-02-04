import pyautogui as pg
import pyperclip
from time import sleep
import random

bot_ativo = True

def escrever_frase(frase):
    pyperclip.copy(frase)
    pg.hotkey('ctrl','a')
    sleep(0.7)
    pg.hotkey('ctrl','v')
    

def verificar_resultado(regiao):
    tr_variations = [
        'icons/tr.PNG',
        'icons/tr_2.png',
        'icons/tr_3.png',
        'icons/tr_4.png',
    ]
    
    for tr_variation in tr_variations:
        try:
            tr_pos = pg.locateOnScreen(tr_variation, region=regiao, confidence=0.7)
            if tr_pos:
                return "tr"
        except pg.ImageNotFoundException:
            pass
   
    ct_variations = [
        'icons/ct.PNG',
        'icons/ct_2.png',
        'icons/ct_3.png',
        'icons/ct_4.png',
    ]
    
    for ct_variation in ct_variations:
        try:
            ct_pos = pg.locateOnScreen(ct_variation, region=regiao, confidence=0.7)
            if ct_pos:
                return "ct"
        except pg.ImageNotFoundException:
            pass
    
    try:
        dado_pos = pg.locateOnScreen('icons/dados.PNG', region=regiao, confidence=0.7)
        if dado_pos:
            return "dados"
    except pg.ImageNotFoundException:
        pass
    
def colocar_valor(valor):
    pg.click(x=random.randint(630,800), y=438, duration=1)
    sleep(0.5)
    escrever_frase(str(valor))
    
def verificar_saldo():
    try:
        if pg.locateOnScreen("icons/sem_saldo.PNG", region=(1640,121,100,40), confidence=0.7):
            return False
        else:
            return True
    except:
        return True
    
def verificar_rolando():
    # pg.screenshot("resultados/rolando.png",region=(912,273,80,20))
    try:
        if pg.locateOnScreen("icons/rolando.PNG", confidence=0.7):
            return True
        else:
            return False
    except:
        return False
    
def parar_bot():
    global bot_ativo
    bot_ativo = False

def iniciar_bot(valor_inicial_string, escrever_log_callback=None):

    # Função auxiliar para logar (callback ou print)
    def log(mensagem):
        if escrever_log_callback:
            escrever_log_callback(mensagem)
        else:
            print(mensagem)

    log(" ---------------------------- Iniciando bot ------------------------\n")
    
    global bot_ativo
    
    regioes = {
        'ultimo_resultado': (1021, 367, 33, 33),
        'penultimo_resultado': (992, 367, 33, 33),
        'antepenultimo_resultado': (962, 367, 33, 33)
    }
    valor_inicial = float(valor_inicial_string)
    valor_atual = valor_inicial
    
    while True:
        if not bot_ativo:
            log("Bot desativado.")
            break
       
        if not verificar_saldo():
            log("⚠️ Usuário sem saldo, faça o depósito e reinicie o bot!")
            break
        
        while not verificar_rolando():
            log("Aguardando início da rodada...\n")
            sleep(2)
            
        pg.screenshot("resultados/ultimo_resultado.png", region=regioes['ultimo_resultado'])
        pg.screenshot("resultados/penultimo_resultado.png", region=regioes['penultimo_resultado'])
        pg.screenshot("resultados/antepenultimo_resultado.png", region=regioes['antepenultimo_resultado'])

        ultimo_resultado = verificar_resultado(regioes['ultimo_resultado'])
        penultimo_resultado = verificar_resultado(regioes['penultimo_resultado'])
        antepenultimo_resultado = verificar_resultado(regioes['antepenultimo_resultado'])
        
        if (ultimo_resultado is None or
            penultimo_resultado is None or
            antepenultimo_resultado is None):
            log("Erro ao encontrar resultados, reiniciando a busca.\n")
        
        log(f"Ultimo Resultado: {ultimo_resultado}\n"
            f"Penúltimo Resultado: {penultimo_resultado}\n"
            f"Antepenultimo Resultado: {antepenultimo_resultado}\n")
        log("-------------------------------------------------------------------")
        
        if (ultimo_resultado == penultimo_resultado == antepenultimo_resultado == "ct"):
            log(f"Encontrado 3 resultados para CT, iniciando aposta em TR com {valor_inicial} moedas.\n")
            log("-------------------------------------------------------------------")
            # Apostar TR
            colocar_valor(valor_inicial)
            pg.click(x=random.randint(1300,1500), y=529, duration=0.7)  # Apostar no TR
            
            # Aguardar o final da rodada atual
            while verificar_rolando():
                sleep(1)
                
            # Aguardar o inicio da próxima rodada
            while not verificar_rolando():
                sleep(1)
                
            ultimo_resultado = verificar_resultado(regioes['ultimo_resultado'])
            
            while ultimo_resultado != "tr":
                valor_atual = valor_atual * 2
                log(f"Falha ao apostar em TR, dobrando a aposta para {valor_atual} moedas.\n")
                log("-------------------------------------------------------------------")
                colocar_valor(valor_atual)
                pg.click(x=random.randint(1300,1500), y=529, duration=0.7)
                
                # Aguardar o final da rodada atual
                while verificar_rolando():
                    sleep(1)
                    
                # Aguardar o inicio da próxima rodada
                while not verificar_rolando():
                    sleep(1)
                    
                ultimo_resultado = verificar_resultado(regioes['ultimo_resultado'])
                
            log("Resultado TR encontrado, reiniciando a aposta.\n")
            log("-------------------------------------------------------------------")
            valor_atual = valor_inicial
            
        elif (ultimo_resultado == penultimo_resultado == antepenultimo_resultado == "tr"):
            log(f"Encontrado 3 resultados para TR, iniciando aposta em CT com {valor_inicial} moedas.\n")
            log("-------------------------------------------------------------------")
            # Apostar CT
            colocar_valor(valor_inicial)
            pg.click(x=random.randint(500,700), y=526, duration=0.5)
            
            # Aguardar o final da rodada atual
            while verificar_rolando():
                sleep(1)
                
            # Aguardar o inicio da próxima rodada
            while not verificar_rolando():
                sleep(1)
                
            ultimo_resultado = verificar_resultado(regioes['ultimo_resultado'])
            
            while ultimo_resultado != "ct":
                valor_atual = valor_atual * 2
                log(f"Falha ao apostar em CT, dobrando a aposta para {valor_atual} moedas.\n")
                log("-------------------------------------------------------------------")
                colocar_valor(valor_atual)
                pg.click(x=random.randint(388,710), y=527, duration=0.7)
                
                # Aguardar o final da rodada atual
                while verificar_rolando():
                    sleep(1)
                    
                # Aguardar o inicio da próxima rodada
                while not verificar_rolando():
                    sleep(1)
                    
                ultimo_resultado = verificar_resultado(regioes['ultimo_resultado'])
                
            log("Resultado CT encontrado, reiniciando a aposta.\n")
            log("-------------------------------------------------------------------")
            valor_atual = valor_inicial
        else:
            # Se não houve repetição de 3 resultados iguais
            continue

        
# if __name__ == "__main__":
#     iniciar_bot(valor_aposta_inicial)
        
    
    
    
        
    
    

    
    
    
    
