from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
import requests
import time
from deep_translator import GoogleTranslator

LAST_REQUEST_TIME = None
REQUEST_COOLDOWN = 2  # segundos


def get_advice():
    global LAST_REQUEST_TIME

    if LAST_REQUEST_TIME and time.time() - LAST_REQUEST_TIME < REQUEST_COOLDOWN:
        return "Por favor, aguarde antes de tentar novamente."

    try:
        advice = cache.get("advice")
        if not advice:
            response = requests.get("https://zenquotes.io/api/random")
            if response.status_code == 200:
                data = response.json()

                if isinstance(data, list) and data and "q" in data[0]:
                    quote = data[0]["q"]
                    author = data[0].get("a", "Autor desconhecido")
                    full_quote = f"{quote} — {author}"

                    # Tradução mais estável
                    try:
                        translation = GoogleTranslator(
                            source="auto", target="pt"
                        ).translate(full_quote)
                    except Exception as e:
                        translation = f"{full_quote} (tradução indisponível)"

                    cache.set("advice", translation, timeout=600)
                    LAST_REQUEST_TIME = time.time()
                    return translation
                else:
                    return "Não foi possível obter a citação válida da API."
            else:
                return "Desculpe, não foi possível obter a citação."

        return advice

    except requests.exceptions.RequestException as e:
        return f"Erro ao fazer requisição: {str(e)}"
    except Exception as e:
        return f"Erro ao processar a requisição: {str(e)}"


def conselho(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        advice = get_advice()
        return JsonResponse({"advice": advice})
    else:
        advice = get_advice()
        return render(request, "shared/conselho.html", {"advice": advice})
