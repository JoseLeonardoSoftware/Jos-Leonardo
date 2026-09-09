import qrcode
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

imagem_qr_global = None  # Guarda a imagem gerada


def gerar_qrcode():
    global imagem_qr_global

    link = entrada.get().strip()

    if not link:
        messagebox.showerror("Erro", "Digite um link!")
        return

    # Gera o QR Code
    imagem_qr_global = qrcode.make(link)

    # Redimensiona para exibição
    imagem_exibicao = imagem_qr_global.resize((220, 220))
    imagem_tk = ImageTk.PhotoImage(imagem_exibicao)

    # Exibe na interface
    label_qr.config(image=imagem_tk)
    label_qr.image = imagem_tk

    # Ativa botão de download
    botao_baixar.config(state=tk.NORMAL)

    messagebox.showinfo("Sucesso", "QR Code gerado com sucesso!")


def baixar_qrcode():
    if imagem_qr_global is None:
        messagebox.showerror("Erro", "Gere um QR Code primeiro!")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagem PNG", "*.png")],
        title="Salvar QR Code"
    )

    if caminho:
        imagem_qr_global.save(caminho)
        messagebox.showinfo("Salvo", f"QR Code salvo em:\n{caminho}")


# ===== INTERFACE =====
janela = tk.Tk()
janela.title("Gerador de QR Code Universal")
janela.geometry("480x520")
janela.resizable(False, False)

tk.Label(
    janela,
    text="Cole o link da rede social ou site:",
    font=("Arial", 12)
).pack(pady=10)

entrada = tk.Entry(janela, width=55)
entrada.pack(pady=5)

tk.Button(
    janela,
    text="Gerar QR Code",
    command=gerar_qrcode,
    width=20
).pack(pady=15)

label_qr = tk.Label(janela)
label_qr.pack(pady=20)

botao_baixar = tk.Button(
    janela,
    text="Baixar QR Code",
    command=baixar_qrcode,
    width=20,
    state=tk.DISABLED
)
botao_baixar.pack(pady=10)

janela.mainloop()
