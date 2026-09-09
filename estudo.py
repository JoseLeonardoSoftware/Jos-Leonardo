import psutil
print("Processos ativos:\n")
for proc in psutil.process_iter(['pid', 'name', 'status']):
    try:
        print(proc.info)
    except:
        pass
