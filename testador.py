import speedtest
import csv
from datetime import datetime

def testar_velocidade():
    st = speedtest.Speedtest()
    st.get_best_server()
    print("Testando a velocidade...")
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping

    return download, upload, ping

def salvar_resultado(download, upload, ping):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arquivo = "log_velocidade.csv"
    
    # isso salva em CSV
    with open(arquivo, mode="a", newline="") as file:
        escritor = csv.writer(file)
        if file.tell() == 0:
            escritor.writerow(["Data/Hora", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)"])
        escritor.writerow([data_hora, download, upload, ping])

    print(f"Resultado salvo em {arquivo}!")

def main():
    print("Teste de Velocidade de Internet")
    download, upload, ping = testar_velocidade()
    print(f"Download: {download:.2f} Mbps")
    print(f"Upload: {upload:.2f} Mbps")
    print(f"Ping: {ping:.2f} ms")

    salvar_resultado(download, upload, ping)

if __name__ == "__main__":
    main()
