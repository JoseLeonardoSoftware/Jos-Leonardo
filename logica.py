import calendar
import matplotlib.pyplot as plt

# Configurar idioma (português manual)
meses = [
    "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL",
    "MAIO", "JUNHO", "JULHO", "AGOSTO",
    "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
]

dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

# Configurar calendário
calendar.setfirstweekday(calendar.MONDAY)

ano = 2026

# Criar figura grande (alta resolução)
fig, axes = plt.subplots(4, 3, figsize=(16, 20))
fig.suptitle(f"CALENDÁRIO {ano}", fontsize=28, fontweight='bold')

# Ajuste de layout
plt.subplots_adjust(hspace=0.5, wspace=0.3)

# Loop pelos meses
for i, ax in enumerate(axes.flat):
    mes = i + 1
    ax.set_title(meses[i], fontsize=14, fontweight='bold')

    # Obter matriz do mês
    cal = calendar.monthcalendar(ano, mes)

    # Converter zeros em vazio
    cal_formatado = []
    for semana in cal:
        linha = []
        for dia in semana:
            linha.append("" if dia == 0 else str(dia))
        cal_formatado.append(linha)

    # Criar tabela
    tabela = ax.table(
        cellText=cal_formatado,
        colLabels=dias_semana,
        loc='center',
        cellLoc='center'
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1, 1.5)

    # Remover eixos
    ax.axis('off')

# Salvar imagem
plt.savefig("calendario_2026.png", dpi=300, bbox_inches='tight')

print("Calendário 2026 gerado com sucesso!")
