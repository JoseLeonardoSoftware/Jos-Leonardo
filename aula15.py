import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

# =========================
# FUNÇÕES
# =========================


def potencia(V, R):
    return (V**2) / R


def simular(V, R, ks):
    resultados = []

    for i, k in enumerate(ks):
        eta = k**2
        P_in = potencia(V, R)
        P_out = P_in * eta
        V_out = np.sqrt(P_out * R)
        perda = (1 - eta) * 100

        resultados.append({
            "nome": f"Config {i+1}",
            "k": k,
            "P_in": P_in,
            "P_out": P_out,
            "V_out": V_out,
            "ef": eta * 100,
            "perda": perda
        })

    return resultados

# =========================
# BOTÃO EXECUTAR
# =========================


def executar():
    try:
        V = float(entry_tensao.get())
        R = float(entry_resistencia.get())

        ks = [
            float(entry_k1.get()),
            float(entry_k2.get()),
            float(entry_k3.get()),
            float(entry_k4.get())
        ]

        resultados = simular(V, R, ks)

        mostrar_resultados(resultados)
        gerar_graficos(resultados)

    except:
        messagebox.showerror("Erro", "Verifique os valores digitados")

# =========================
# MOSTRAR RESULTADOS
# =========================


def mostrar_resultados(resultados):
    texto = ""

    for r in resultados:
        texto += f"{r['nome']} (k={r['k']})\n"
        texto += f"Potência Entrada: {r['P_in']:.2f} W\n"
        texto += f"Potência Saída: {r['P_out']:.2f} W\n"
        texto += f"Tensão Saída: {r['V_out']:.2f} V\n"
        texto += f"Eficiência: {r['ef']:.2f}%\n"
        texto += f"Perda: {r['perda']:.2f}%\n"
        texto += "----------------------\n"

    label_resultado.config(text=texto)

# =========================
# GRÁFICOS
# =========================


def gerar_graficos(resultados):

    nomes = [r["nome"] for r in resultados]
    ef = [r["ef"] for r in resultados]
    perdas = [r["perda"] for r in resultados]
    p_in = [r["P_in"] for r in resultados]
    p_out = [r["P_out"] for r in resultados]

    # Eficiência
    plt.figure()
    plt.bar(nomes, ef)
    plt.title("Eficiência (%)")
    plt.xlabel("Configuração")
    plt.ylabel("Eficiência")
    plt.grid()
    plt.show()

    # Perdas
    plt.figure()
    plt.bar(nomes, perdas)
    plt.title("Perdas (%)")
    plt.xlabel("Configuração")
    plt.ylabel("Perda")
    plt.grid()
    plt.show()

    # Potência
    plt.figure()
    plt.plot(nomes, p_in, marker='o', label="Entrada")
    plt.plot(nomes, p_out, marker='o', label="Saída")
    plt.title("Potência")
    plt.xlabel("Configuração")
    plt.ylabel("W")
    plt.legend()
    plt.grid()
    plt.show()

    # Curva k
    ks = np.linspace(0.1, 1.0, 20)
    ef_k = [(k**2)*100 for k in ks]

    plt.figure()
    plt.plot(ks, ef_k, marker='o')
    plt.title("Eficiência vs k")
    plt.xlabel("k")
    plt.ylabel("%")
    plt.grid()
    plt.show()

# =========================
# INTERFACE
# =========================


janela = tk.Tk()
janela.title("Simulador de Transmissão por Indução")
janela.geometry("500x600")

tk.Label(janela, text="Tensão de Entrada (V)").pack()
entry_tensao = tk.Entry(janela)
entry_tensao.pack()

tk.Label(janela, text="Resistência (Ohms)").pack()
entry_resistencia = tk.Entry(janela)
entry_resistencia.pack()

tk.Label(janela, text="Coeficientes k (0 a 1)").pack()

entry_k1 = tk.Entry(janela)
entry_k1.pack()
entry_k1.insert(0, "0.3")

entry_k2 = tk.Entry(janela)
entry_k2.pack()
entry_k2.insert(0, "0.5")

entry_k3 = tk.Entry(janela)
entry_k3.pack()
entry_k3.insert(0, "0.7")

entry_k4 = tk.Entry(janela)
entry_k4.pack()
entry_k4.insert(0, "0.9")

tk.Button(janela, text="Calcular", command=executar).pack(pady=10)

label_resultado = tk.Label(janela, text="", justify="left")
label_resultado.pack()

janela.mainloop()
