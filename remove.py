import telepot
from telepot.loop import MessageLoop
import requests
from io import BytesIO
from PIL import Image

TOKEN = '6322507780:AAEkT2WXKo9KVZ3krPXORlGh1VYlNys165s'
bot = telepot.Bot(TOKEN)


API_KEY_REMOVE_BG = 'XrEHE73aUTiB9qcEFf2EZDAx'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    try:
        if content_type == 'text':
            
            if msg['text'] == '/start':
                bot.sendMessage(chat_id, 'Bem-vindo ao ChatBot removedor de fundo! Envie uma foto para remover o fundo.')
        elif content_type == 'photo':
            
            file_id = msg['photo'][-1]['file_id']
            file_path = bot.getFile(file_id)['file_path']
            photo_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'

            
            response = requests.get(photo_url)
            img = Image.open(BytesIO(response.content))

            
            remove_bg_url = 'https://api.remove.bg/v1.0/removebg'
            headers = {'X-Api-Key': API_KEY_REMOVE_BG}
            files = {'image_file': response.content}
            response_bg = requests.post(remove_bg_url, headers=headers, files=files)

            print(response_bg.status_code)  

            
            if response_bg.status_code == 200:
                img_bg_removed = Image.open(BytesIO(response_bg.content))
                img_bg_removed.save('output.png')  
                bot.sendPhoto(chat_id, open('output.png', 'rb'))
            else:
                bot.sendMessage(chat_id, 'Erro ao remover o fundo da imagem.')

    except telepot.exception.TelegramError as e:
        
        print(f'Erro do Telegram: {e}')

    except Exception as e:
        
        print(f'Erro: {e}')


MessageLoop(bot, handle).run_as_thread()

print('Aguardando mensagens...')


while True:
    pass
