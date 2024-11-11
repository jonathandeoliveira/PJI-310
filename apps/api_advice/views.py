from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
import requests
from googletrans import Translator
import time

# Configuração de controle de requisições
LAST_REQUEST_TIME = None
REQUEST_COOLDOWN = 2  # 2 segundos


def get_advice():
    global LAST_REQUEST_TIME

    if LAST_REQUEST_TIME and time.time() - LAST_REQUEST_TIME < REQUEST_COOLDOWN:
        return "Por favor, aguarde antes de tentar novamente."

    try:
        # Tenta obter o conselho do cache primeiro
        advice = cache.get("advice")

        if not advice:
            response = requests.get("https://api.adviceslip.com/advice")

            if response.status_code == 200:
                advice_json = response.json()

                if "slip" in advice_json and "advice" in advice_json["slip"]:
                    advice_text = advice_json["slip"]["advice"]

                    translator = Translator()
                    translation = translator.translate(
                        advice_text, src="en", dest="pt"
                    ).text

                    cache.set("advice", translation, timeout=600)

                    LAST_REQUEST_TIME = time.time()

                    return translation
                else:
                    return "Não foi possível obter o conselho válido da API."
            else:
                return "Desculpe, não foi possível obter o conselho."

        return advice

    except requests.exceptions.RequestException as e:
        return f"Erro ao fazer requisição: {str(e)}"
    except Exception as e:
        return f"Erro ao processar a requisição: {str(e)}"


def conselho(request):
    advice = get_advice()  # Obtemos o conselho aqui, via AJAX e pelo navegador

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"advice": advice})
    return render(request, "shared/conselho.html", {"advice": advice})
