import qrcode
import re


# ==============================
# CRC16 (OBRIGATÓRIO)
# ==============================
def crc16_ccitt(payload: str) -> str:
    crc = 0xFFFF
    polinomio = 0x1021

    for byte in payload.encode("utf-8"):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ polinomio) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF

    return f"{crc:04X}"


# ==============================
# FORMATA TELEFONE (CRÍTICO)
# ==============================
def formatar_telefone(chave: str) -> str:
    numeros = re.sub(r"\D", "", chave)

    if len(numeros) != 11:
        raise ValueError("Telefone inválido! Use DDD + número (11 dígitos)")

    return f"+55{numeros}"


# ==============================
# GERAR PAYLOAD PIX CORRETO
# ==============================
def gerar_payload_pix(telefone: str) -> str:
    chave_pix = formatar_telefone(telefone)

    nome = "PAGADOR"
    cidade = "SAO PAULO"

    payload = ""

    # Payload Format Indicator
    payload += "000201"

    # Static QR
    payload += "010211"

    # Merchant Account Information (PIX)
    gui = "BR.GOV.BCB.PIX"

    campo_gui = f"00{len(gui):02d}{gui}"
    campo_chave = f"01{len(chave_pix):02d}{chave_pix}"

    merchant = campo_gui + campo_chave

    payload += f"26{len(merchant):02d}{merchant}"

    # Merchant Category Code
    payload += "52040000"

    # Currency (BRL)
    payload += "5303986"

    # Country
    payload += "5802BR"

    # Nome (OBRIGATÓRIO)
    payload += f"59{len(nome):02d}{nome}"

    # Cidade (OBRIGATÓRIO)
    payload += f"60{len(cidade):02d}{cidade}"

    # CRC
    payload_crc = payload + "6304"
    crc = crc16_ccitt(payload_crc)

    payload_final = payload_crc + crc

    return payload_final


# ==============================
# GERAR QR CODE
# ==============================
def gerar_qr(telefone: str):
    payload = gerar_payload_pix(telefone)

    print("\nPayload gerado:")
    print(payload)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("pix_qrcode.png")

    print("\nQR Code gerado com sucesso: pix_qrcode.png")


# ==============================
# EXECUÇÃO
# ==============================
if __name__ == "__main__":
    telefone = input("Digite o telefone (DDD + número): ")

    try:
        gerar_qr(telefone)
    except Exception as e:
        print("Erro:", e)
