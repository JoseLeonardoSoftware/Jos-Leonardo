import tkinter as tk
from tkinter import messagebox
import sqlite3
import qrcode
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime

# -------------------------
# Banco de dados
# -------------------------

conn = sqlite3.connect("presenca.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS presenca(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT,
data TEXT
)
""")

conn.commit()


# -------------------------
# Cadastrar aluno
# -------------------------

def cadastrar():

    nome = entrada_nome.get()

    if nome == "":
        messagebox.showerror("Erro", "Digite o nome")
        return

    cursor.execute("INSERT INTO alunos (nome) VALUES (?)", (nome,))
    conn.commit()

    messagebox.showinfo("Sucesso", "Aluno cadastrado")

    entrada_nome.delete(0, tk.END)


# -------------------------
# Gerar QR code da aula
# -------------------------

def gerar_qr():

    agora = datetime.now().strftime("%d-%m-%Y %H:%M")

    img = qrcode.make(agora)

    img.save("aula_qr.png")

    messagebox.showinfo("QR Code", "QR Code da aula gerado")


# -------------------------
# Ler QR code e marcar presença
# -------------------------

def ler_qr():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        for codigo in decode(frame):

            data = codigo.data.decode('utf-8')

            nome = entrada_nome.get()

            cursor.execute(
                "INSERT INTO presenca (nome,data) VALUES (?,?)",
                (nome, data))

            conn.commit()

            messagebox.showinfo("Presença", "Presença registrada")

            cap.release()
            cv2.destroyAllWindows()

            return

        cv2.imshow("Leitor QR", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# -------------------------
# Mostrar presenças
# -------------------------

def mostrar():

    cursor.execute("SELECT * FROM presenca")

    dados = cursor.fetchall()

    texto.delete("1.0", tk.END)

    for linha in dados:

        texto.insert(tk.END, f"{linha[1]} - {linha[2]}\n")


# -------------------------
# Interface
# -------------------------

janela = tk.Tk()
janela.title("Sistema de Presença")

tk.Label(janela, text="Nome do aluno").pack()

entrada_nome = tk.Entry(janela)
entrada_nome.pack()

tk.Button(janela, text="Cadastrar aluno", command=cadastrar).pack(pady=5)

tk.Button(janela, text="Gerar QR da aula", command=gerar_qr).pack(pady=5)

tk.Button(janela, text="Ler QR e marcar presença", command=ler_qr).pack(pady=5)

tk.Button(janela, text="Mostrar presenças", command=mostrar).pack(pady=5)

texto = tk.Text(janela, height=10, width=40)
texto.pack()

janela.mainloop()
