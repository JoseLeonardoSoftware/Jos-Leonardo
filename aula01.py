def calcular_salario_por_hora():
    print("=== Cálculo de Salário por Hora ===")

    # Entrada de dados
    salario_mensal = float(input("Digite seu salário mensal (R$): "))
    dias_por_semana = float(input("Quantos dias você trabalha por semana? "))
    horas_por_dia = float(input("Quantas horas você trabalha por dia? "))

    # Constante: média de semanas no mês
    semanas_por_mes = 4.33

    # Cálculo de horas mensais
    horas_por_semana = dias_por_semana * horas_por_dia
    horas_por_mes = horas_por_semana * semanas_por_mes

    # Cálculo do valor por hora
    salario_por_hora = salario_mensal / horas_por_mes

    # Saída
    print("\n=== Resultado ===")
    print(f"Horas trabalhadas no mês: {horas_por_mes:.2f}h")
    print(f"Salário por hora: R$ {salario_por_hora:.2f}")


# Executar função
calcular_salario_por_hora()
