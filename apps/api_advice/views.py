from django.shortcuts import render
from django.core.cache import cache
import requests
from googletrans import Translator
import time

# Configuração de controle de requisições (limitação)
LAST_REQUEST_TIME = None
REQUEST_COOLDOWN = 2  # Em segundos, define o tempo entre as requisições


def get_advice():
    global LAST_REQUEST_TIME

    # Verifica se é necessário esperar antes de fazer uma nova requisição
    if LAST_REQUEST_TIME and time.time() - LAST_REQUEST_TIME < REQUEST_COOLDOWN:
        return "Por favor, aguarde antes de tentar novamente."

    try:
        # Tenta obter o conselho do cache primeiro
        advice = cache.get('advice')

        # Se o conselho não estiver no cache, faz a requisição à API
        if not advice:
            # Faz a requisição para a API Advice Slip
            response = requests.get("https://api.adviceslip.com/advice")

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                advice_json = response.json()

                # Verifica se a chave 'slip' e 'advice' estão presentes na resposta
                if 'slip' in advice_json and 'advice' in advice_json['slip']:
                    advice_text = advice_json['slip']['advice']

                    # Traduz o conselho para português
                    translator = Translator()
                    translation = translator.translate(
                        advice_text, src='en', dest='pt').text

                    # Armazena o conselho no cache por 10 minutos
                    cache.set('advice', translation, timeout=600)

                    # Atualiza o tempo da última requisição
                    LAST_REQUEST_TIME = time.time()

                    return translation
                else:
                    return "Não foi possível obter o conselho válido da API."
            else:
                return "Desculpe, não foi possível obter o conselho."

        # Se o conselho estiver no cache, retorna-o diretamente
        return advice

    except Exception as e:
        return f"Erro ao processar a requisição: {str(e)}"


def conselho(request):
    advice = get_advice()  # Obtemos o conselho aqui
    # Passamos o conselho como contexto
    return render(request, 'shared/conselho.html', {'advice': advice})
