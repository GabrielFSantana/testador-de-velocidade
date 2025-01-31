# -*- coding: utf-8 -*-
"""
Teste de Velocidade da Internet com Múltiplas Funcionalidades
Autor: GABRIEL FELIPE SANTANA BELARMINO
"""

import speedtest
import csv
import argparse
import logging
import sqlite3
import smtplib
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import threading
import time
import configparser
import gettext
from datetime import datetime
from email.mime.text import MIMEText

# CONFIGURAÇÕES INICIAIS 
# Carregar configurações de arquivo externo
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

logging.basicConfig(
    filename='internet_speed.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

gettext.install('messages', localedir='locales')

# FUNÇÕES PRINCIPAIS 

def testar_velocidade():
    """Testa a velocidade da internet com tratamento de erros (Melhoria 1)"""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        logging.info(_("Testando velocidade..."))
        
        download = st.download() / 1_000_000  # Converte para Mbps
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        
        return download, upload, ping
    except Exception as e:
        logging.error(_(f"Erro no teste: {e}"))
        return None, None, None

def salvar_resultado(download, upload, ping, arquivo_csv='velocidade.csv'):
    """Salva resultados em CSV e banco de dados (Melhoria 2, 6)"""
    if None in (download, upload, ping):
        return

    # Salvar em CSV
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(arquivo_csv, 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Data/Hora", "Download", "Upload", "Ping"])
        writer.writerow([data_hora, download, upload, ping])

    # Salvar no banco de dados SQLite 
    conn = sqlite3.connect('velocidade.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS testes
                 (data_hora TEXT, download REAL, upload REAL, ping REAL)''')
    c.execute("INSERT INTO testes VALUES (?,?,?,?)", 
              (data_hora, download, upload, ping))
    conn.commit()
    conn.close()

# FUNÇÕES ADICIONAIS 

def enviar_alerta(download, upload):
    """Envia notificação por e-mail (Melhoria 5)"""
    try:
        # Ler limites corretamente
        limite_download = float(config['ALERTAS']['limite_download'].split(';')[0].strip())
        limite_upload = float(config['ALERTAS']['limite_upload'].split(';')[0].strip())

        if download < limite_download or upload < limite_upload:
            msg = MIMEText(_(f"""
                ALERTA: Velocidade abaixo do esperado!
                Download: {download:.2f} Mbps (Mínimo: {limite_download} Mbps)
                Upload: {upload:.2f} Mbps (Mínimo: {limite_upload} Mbps)
            """))
            
            msg['Subject'] = _('Alerta de Velocidade')
            msg['From'] = config['EMAIL']['remetente']
            msg['To'] = config['EMAIL']['destinatario']

            with smtplib.SMTP(config['EMAIL']['servidor'], int(config['EMAIL']['porta'])) as server:
                server.starttls()
                server.login(config['EMAIL']['usuario'], config['EMAIL']['senha'])
                server.send_message(msg)
            logging.info(_("Alerta enviado por e-mail"))
            
    except Exception as e:
        logging.error(_(f"Erro no envio do alerta: {e}"))

def gerar_grafico():
    """Gera gráfico com dados históricos (Melhoria 4)"""
    try:
        df = pd.read_csv('velocidade.csv')
        plt.style.use('ggplot')
        df.plot(x='Data/Hora', y=['Download', 'Upload', 'Ping'])
        plt.title(_('Histórico de Velocidade'))
        plt.ylabel(_('Mbps / ms'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('historico.png')
        plt.close()
    except Exception as e:
        logging.error(_(f"Erro no gráfico: {e}"))

# INTERFACE GRÁFICA 

class Aplicativo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(_("Teste de Velocidade"))
        self.geometry("300x200")
        
        # Elementos da UI
        self.btn_teste = tk.Button(
            self, 
            text=_("Iniciar Teste"), 
            command=self.iniciar_teste
        )
        self.btn_grafico = tk.Button(
            self,
            text=_("Gerar Gráfico"),
            command=gerar_grafico
        )
        self.lbl_resultado = tk.Label(self, text="", justify=tk.LEFT)
        
        # Layout
        self.btn_teste.pack(pady=10)
        self.btn_grafico.pack(pady=5)
        self.lbl_resultado.pack(pady=10)

    def iniciar_teste(self):

        def thread_teste():
            download, upload, ping = testar_velocidade()
            if download:
                self.lbl_resultado.config(text=_(
                    f"Download: {download:.2f} Mbps\n"
                    f"Upload: {upload:.2f} Mbps\n"
                    f"Ping: {ping:.2f} ms"
                ))
                salvar_resultado(download, upload, ping)
                enviar_alerta(download, upload)
                messagebox.showinfo(_("Sucesso"), _("Teste concluído!"))

        threading.Thread(target=thread_testar, daemon=True).start()

# EXECUÇÃO PRINCIPAL 

def main():

    parser = argparse.ArgumentParser(description=_("Teste de Velocidade"))
    parser.add_argument(
        '--gui', 
        action='store_true', 
        help=_("Abrir interface gráfica")
    )
    parser.add_argument(
        '--intervalo', 
        type=int, 
        default=int(config['GERAL']['intervalo'].split(';')[0].strip()),  # Pega apenas o número
        help=_("Intervalo entre testes em segundos")
    )
    args = parser.parse_args()

    if args.gui:
        app = Aplicativo()
        app.mainloop()
    else:
        while True:
            download, upload, ping = testar_velocidade()
            if download:
                print(_(f"Download: {download:.2f} Mbps"))
                print(_(f"Upload: {upload:.2f} Mbps"))
                print(_(f"Ping: {ping:.2f} ms"))
                salvar_resultado(download, upload, ping)
                enviar_alerta(download, upload)
            
            if args.intervalo <= 0:
                break
            time.sleep(args.intervalo)

if __name__ == "__main__":
    main()