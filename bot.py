import logging
from aiogram import Bot, Dispatcher, executor, types
from utils import criar_pagamento, verificar_pagamento, salvar_dados, carregar_dados, dias_disponiveis, horarios_disponiveis

API_TOKEN = '7882021305:AAGoM7RLUdZRqGtGDK5aLRlsALcR6a5gWoM'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

usuarios = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Bem-vindo ao PropulsoAI Bot!\n\nVamos criar sua propaganda profissional.\n\nMe diga: qual a descrição do seu anúncio?")
    usuarios[message.from_user.id] = {'etapa': 'descricao'}

@dp.message_handler(content_types=types.ContentType.TEXT)
async def coletar_info(message: types.Message):
    uid = message.from_user.id
    if uid not in usuarios:
        return await message.answer("Use /start para começar.")

    dados = usuarios[uid]

    if dados['etapa'] == 'descricao':
        dados['descricao'] = message.text
        dados['etapa'] = 'imagem'
        await message.answer("Envie uma imagem da sua propaganda.")
    elif dados['etapa'] == 'link':
        dados['link'] = message.text
        salvar_dados(uid, dados)
        link_pagamento = criar_pagamento(uid, valor=3)
        await message.answer(f"Perfeito! Agora clique no link abaixo para pagar R$3 e ativar:\n{link_pagamento}")
        dados['etapa'] = 'aguardando_pagamento'
    elif dados['etapa'] == 'dias':
        dados['dias'] = message.text.split(",")
        dados['etapa'] = 'horarios'
        await message.answer("Agora envie 4 horários diferentes (ex: 09:00, 12:00, 15:00, 20:00):")
    elif dados['etapa'] == 'horarios':
        dados['horarios'] = message.text.split(",")
        dados['etapa'] = 'link'
        await message.answer("Por fim, envie o link do botão de ação (ex: https://loja.com/produto123):")
    elif dados['etapa'] == 'aguardando_pagamento' and message.text.lower() == 'pago':
        if verificar_pagamento(uid):
            await message.answer("Pagamento confirmado! Sua propaganda será postada nos dias e horários escolhidos.")
        else:
            await message.answer("Ainda não identificamos seu pagamento. Tente novamente em alguns minutos.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def coletar_imagem(message: types.Message):
    uid = message.from_user.id
    if uid not in usuarios or usuarios[uid]['etapa'] != 'imagem':
        return await message.answer("Envie uma imagem apenas no momento certo do cadastro.")

    file_id = message.photo[-1].file_id
    usuarios[uid]['imagem'] = file_id
    usuarios[uid]['etapa'] = 'dias'
    await message.answer("Quais 4 dias deseja para publicar a propaganda? (ex: segunda, quarta, sexta, domingo):")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)