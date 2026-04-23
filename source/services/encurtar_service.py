from source.models import encurtar_model
import random, string

def generate_new_code(tamanho=10):
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(tamanho))
    print("CODE GERADO:", code, type(code))
    return code
     
def create_shortlink(url):
    while True:
        code = generate_new_code(10)
        if encurtar_model.verify_code_exists(code) == None:
            break

    encurtar_model.save_new_url(url, code)
    