import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# from ttkbootstrap.style import Style
from ttkbootstrap import Style
import tkinter as tk
from app import *
from time import sleep
import app
import threading
from tkinter.scrolledtext import ScrolledText

        
bot_thread = None

def iniciar_thread_bot(valor_aposta_inicial):
    
    if not valor_aposta_inicial:
        escrever_log("Valor da aposta inicial está vazio! Usando 1.0")
        valor_aposta_inicial = "1.0"
    global bot_thread
    app.bot_ativo = True

    print("Iniciando a thread do bot!!!!!!!!!!!!!!!!!!!!!!")
    # Cria uma thread separada que executa iniciar_bot
    bot_thread = threading.Thread(
        target=app.iniciar_bot,
        args=(valor_aposta_inicial,),         # argumentos "normais"
        kwargs={"escrever_log_callback": escrever_log},
        daemon=True  # daemon=True encerra a thread quando a main acabar
    )
    bot_thread.start()

def parar_thread_bot():
    escrever_log("--- Finalizando bot ---")
    global bot_thread
    app.bot_ativo = False  
    if bot_thread is not None:
        bot_thread.join()
        bot_thread = None
        
def toggle_iniciar_parar(valor_aposta_inicial):

    if iniciar_parar_btn.cget('text') == 'Iniciar':
        iniciar_parar_btn.config(text='Parar',bootstyle="danger")
        iniciar_thread_bot(valor_aposta_inicial)
          
    else:
        iniciar_parar_btn.config(text='Iniciar',bootstyle="success")
        parar_thread_bot()
        
def escrever_log(mensagem):
    log_text.insert(tk.END, mensagem + "\n")
    log_text.see(tk.END)
        
       

window = ttk.Window("Bot Empire")
window.geometry("550x500")
style = Style(theme="darkly")


label = ttk.Label(window, text="Configurações do BOT Empire")
label.pack(pady=35)
label.config(font=("Arial",20,"bold"))

aposta_inicial = ttk.Frame(window)
aposta_inicial.pack(pady=18,padx=10)
ttk.Label(aposta_inicial,text="Valor da Aposta Inicial").pack(padx=5,pady=5)
aposta_inicial_entry = ttk.Entry(aposta_inicial)
aposta_inicial_entry.pack(padx=5)


valor_aposta_inicial = aposta_inicial_entry.get()

log_frame = ttk.Frame(window)
log_frame.pack(pady=18,padx=10,fill="both",expand=True)

log_text = ScrolledText(master=log_frame,wrap = "word", width=60, height=10)

log_text.pack(fill="both",expand=True)


iniciar = ttk.Frame(window)
iniciar.pack(pady=18,padx=10,fill="x")
iniciar_parar_btn = ttk.Button(
    iniciar,
    text="Iniciar",
    style="success",
    command=lambda: toggle_iniciar_parar(
        aposta_inicial_entry.get(),
    )
)
iniciar_parar_btn.pack(padx=5, pady=5)
    


window.mainloop()

