import json

def criar_pagamento(user_id, valor):
    # Gera link de pagamento simulado
    return f"https://mpago.la/22w162C?ref_user={user_id}&v={valor}"

def verificar_pagamento(user_id):
    # Aqui você colocaria a verificação via API do Mercado Pago
    # Exemplo fictício
    return True

def salvar_dados(user_id, dados):
    with open("dados.json", "w") as f:
        json.dump({str(user_id): dados}, f, indent=2)

def carregar_dados():
    try:
        with open("dados.json") as f:
            return json.load(f)
    except:
        return {}

def dias_disponiveis():
    return ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

def horarios_disponiveis():
    return ["08:00", "10:00", "12:00", "15:00", "18:00", "20:00"]