import os
import qrcode
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
import webbrowser


class QRSurpresa:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QR Code - Surpresa Especial")
        self.root.geometry("600x600")
        self.root.config(bg="#1e1e2f")

        self.imagens = []

        titulo = Label(root, text="QR Code Surpresa 🎉",
                       font=("Arial", 20, "bold"),
                       bg="#1e1e2f", fg="white")
        titulo.pack(pady=10)

        self.texto_label = Label(root, text="Digite sua mensagem:",
                                 bg="#1e1e2f", fg="white")
        self.texto_label.pack()

        self.texto_entry = Text(root, height=5, width=50)
        self.texto_entry.pack(pady=10)

        btn_imagens = Button(root, text="Selecionar Imagens",
                             command=self.selecionar_imagens,
                             bg="#4CAF50", fg="white")
        btn_imagens.pack(pady=5)

        btn_gerar = Button(root, text="Gerar QR Code",
                           command=self.gerar_qr,
                           bg="#2196F3", fg="white")
        btn_gerar.pack(pady=10)

        self.qr_label = Label(root, bg="#1e1e2f")
        self.qr_label.pack(pady=10)

        btn_salvar = Button(root, text="Salvar QR Code",
                            command=self.salvar_qr,
                            bg="#FF9800", fg="white")
        btn_salvar.pack(pady=5)

    def selecionar_imagens(self):
        arquivos = filedialog.askopenfilenames(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        self.imagens = arquivos
        messagebox.showinfo(
            "Imagens", f"{len(self.imagens)} imagens selecionadas!")

    def gerar_qr(self):
        if not self.imagens:
            messagebox.showerror("Erro", "Selecione pelo menos uma imagem!")
            return

        mensagem = self.texto_entry.get("1.0", END).strip()
        if not mensagem:
            messagebox.showerror("Erro", "Digite uma mensagem!")
            return

        # Criar pasta do projeto
        pasta = "surpresa"
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
        os.makedirs(pasta)

        # Copiar imagens
        nomes_imagens = []
        for img in self.imagens:
            nome = os.path.basename(img)
            shutil.copy(img, os.path.join(pasta, nome))
            nomes_imagens.append(nome)

        # Criar HTML
        html = f"""
        <html>
        <head>
        <title>Surpresa Especial</title>
        <style>
            body {{
                background: linear-gradient(to right, #ff758c, #ff7eb3);
                text-align: center;
                font-family: Arial;
                color: white;
            }}
            img {{
                width: 300px;
                margin: 10px;
                border-radius: 15px;
                box-shadow: 0 0 10px black;
            }}
            h1 {{
                margin-top: 30px;
            }}
        </style>
        </head>
        <body>
        <h1>{mensagem}</h1>
        """

        for nome in nomes_imagens:
            html += f'<img src="{nome}"><br>'

        html += "</body></html>"

        with open(os.path.join(pasta, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

        caminho_absoluto = os.path.abspath(os.path.join(pasta, "index.html"))

        # Criar QR Code apontando para o arquivo
        qr = qrcode.make(caminho_absoluto)
        qr.save("qrcode.png")

        self.qr_img = Image.open("qrcode.png")
        self.qr_img = self.qr_img.resize((200, 200))
        self.qr_tk = ImageTk.PhotoImage(self.qr_img)

        self.qr_label.config(image=self.qr_tk)
        messagebox.showinfo("Sucesso", "QR Code gerado com sucesso!")

    def salvar_qr(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".png")
        if arquivo:
            self.qr_img.save(arquivo)
            messagebox.showinfo("Salvo", "QR Code salvo com sucesso!")


root = Tk()
app = QRSurpresa(root)
root.mainloop()
