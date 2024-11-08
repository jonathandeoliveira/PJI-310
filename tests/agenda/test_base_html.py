from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest
from apps.users.models import UserProfile
from django.urls import reverse


  # Configura o driver do Chrome em modo headless, necessário para fazer o teste sem abrir o navegador. É o setup do selenium.
def setup_driver():
    """Configura o driver do Chrome em modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)

  # Função que obtém o tamanho da fonte de um elemento, usada em todos os nossos testes de tamanho de fonte.
def get_font_size(element):
    """Obtém o tamanho da fonte de um elemento."""
    return float(element.value_of_css_property("font-size").replace('px', ''))
  
#arrange
def test_increase_font_size():
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000/")
        wait = WebDriverWait(driver, 4)

        #act
        # Procura o botão A+
        increase_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'A+')]")))
        text_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#font-controls")))

        # Captura o tamanho de fonte inicial
        initial_font_size = get_font_size(text_element)
        print(f"Tamanho de fonte inicial: {initial_font_size}px")

        # Clica duas vezes para aumentar a fonte
        for _ in range(2):
            increase_button.click()
            time.sleep(0.2)
        increased_font_size = get_font_size(text_element)
        print(f"Tamanho de fonte após aumento: {increased_font_size}px")
        
        #assert
        assert increased_font_size > initial_font_size, "Erro: Aumento de fonte falhou."
        print("Teste de aumento de fonte bem-sucedido.")

    finally:
        driver.quit()

#arrange
def test_decrease_font_size():
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000/")

        wait = WebDriverWait(driver, 4)

        #act  
        # Procura o botão A-
        decrease_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'A-')]")))
        text_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#font-controls")))


        # Captura o tamanho de fonte inicial antes de aumentar
        initial_font_size = get_font_size(text_element)
        for _ in range(2):
            decrease_button.click()
            time.sleep(0.2)

        decreased_font_size = get_font_size(text_element)
        print(f"Tamanho de fonte após diminuição: {decreased_font_size}px")
        
        #assert
        assert decreased_font_size < initial_font_size, "Erro: Diminuição de fonte falhou."
        print("Teste de diminuição de fonte bem-sucedido.")

    finally:
        driver.quit()


#arrange
def test_reset_font_size():
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000/")
        wait = WebDriverWait(driver, 4)

        #act
        # Procura o botão de A+ e o reset
        reset_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Reset')]")))
        increase_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'A+')]")))
        text_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#font-controls")))


        # Captura o tamanho de fonte inicial
        initial_font_size = get_font_size(text_element)

        # Aumenta a fonte para garantir que o reset funcione
        for _ in range(2):
            increase_button.click()
            time.sleep(0.2)

        # Reseta o tamanho da fonte
        reset_button.click()
        time.sleep(0.2)

        reset_font_size = get_font_size(text_element)
        print(f"Tamanho de fonte após reset: {reset_font_size}px")
        assert reset_font_size == initial_font_size, "Erro: Reset de fonte falhou."

        print("Teste de reset de fonte bem-sucedido.")

    finally:
        driver.quit()
        

@pytest.fixture
@pytest.mark.django_db
def create_user():
    # Arrange: Criação do usuário fictício
    user = UserProfile.objects.create_user(
        username="testuser@example.com",
        email="testuser@example.com",
        password="password123",
        document='98765432109',
        full_address='Avenida dos Testes, 456, Rio de Janeiro - RJ',
        birth_date='1995-03-15',
        phone='21987654321',
        is_professor='True'
    )
    return user


@pytest.mark.django_db
def test_user_login(client, create_user):
    # Parte 1: Teste com o client (sem interface gráfica)
    login_url = reverse("login")
    username = create_user.email
    password = "password123"  # A senha correta

    # Fazendo login usando o client
    response = client.post(login_url, {
        "email": username,
        "password": password
    })

    # Verifica se o redirecionamento foi bem-sucedido
    assert response.status_code == 302, "O login não redirecionou como esperado."
    
    # Verifica se o usuário foi autenticado
    user = client.login(email=username, password=password)
    assert user, "Erro: Usuário não autenticado."

    # Você pode verificar para onde o usuário foi redirecionado
    redirect_url = response.get('Location')
    assert redirect_url == reverse("index"), f"Redirecionamento esperado para 'index', mas obteve {redirect_url}."

    # Parte 2: Teste com Selenium (interface gráfica)
    # Função setup_driver() deve estar definida para configurar o WebDriver
    driver = setup_driver()
    # Cria uma instância do WebDriverWait para Selenium
    wait = WebDriverWait(driver, 10)

    try:
        # Navegar para a página de login
        driver.get("http://localhost:8000/login/")

        # Encontrar campos de entrada e fazer login
        username_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#email")))
        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#password")))

        username_input.send_keys(username)
        password_input.send_keys(password)

        # Submeter o formulário de login
        login_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[@type='submit']")))
        login_button.click()

        # Esperar até que o elemento de saudação esteja presente (indicando login bem-sucedido)
        text_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#logado")))

        # Verificar se o texto contém "Bem-vindo"
        expected_text = f"Bem-vindo, {create_user.username}!"
        assert expected_text in text_element.text, f"Texto esperado '{
            expected_text}' não encontrado. Texto atual: '{text_element.text}'"

    finally:
        driver.quit()

# Executa os testes
if __name__ == "__main__":
    test_increase_font_size()
    test_decrease_font_size()
    test_reset_font_size()
    test_user_login()

