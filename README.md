# PropulsoAI Bot

Bot avançado de propaganda no Telegram com pagamento automático, agendamento inteligente, edição premium e muito mais.

## Comandos para rodar no Termux

```bash
pkg update -y && pkg upgrade -y
pkg install python git unzip -y
pip install --upgrade pip wheel setuptools
git clone https://github.com/douglasdias1918/bot-propaganda-telegram-premium.git
cd bot-propaganda-telegram-premium
pip install -r requirements.txt
python bot.py
```

Bot 100% funcional com sistema de pagamento via Mercado Pago, anti-horário duplicado e sistema de renovação inteligente.