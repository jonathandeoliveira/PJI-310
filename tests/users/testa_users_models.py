import pytest
from apps.users.models import UserProfile

@pytest.mark.django_db
#Testa a criação de um usuário
def test_create_user():
  #arrange
    user = UserProfile.objects.create_user(
        username= "testuser@example.com",
        email="testuser@example.com",
        password="password123",
        document = '98765432109',
        full_address = 'Avenida dos Testes, 456, Rio de Janeiro - RJ',
        birth_date =  '1995-03-15',
        phone = '21987654321'
    )
    #act
    # clica em criar conta
    # preenche o formulario
    # clica em enviar 
    
    #assert
    assert user.username == "testuser@example.com"
    assert user.email == "testuser@example.com"
    assert user.check_password("password123")


# # Usuário: usuario_especial
# email: usuario_especial2@xpto.com
# document = '98765432109',
# postal_code: 22041001 (Rio de Janeiro)
# phone: '21987654321'
# birth_date: 15/03/1995
# full_address: Avenida dos Testes, 456, Rio de Janeiro - RJ
# senha: Teste@123!
