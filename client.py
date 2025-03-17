import requests


URL = 'http://localhost:8005/api/v1/users/login'

USER = {
    'username':'Jose',
    'password':'passowrd'
    
}

response = requests.post(URL, json=USER)    

if response.status_code == 200:
    print('El usuario autenticado ')
    print(response.json())
    print(response.cookies)
    print(response.cookies.get_dict())
    

    
    




