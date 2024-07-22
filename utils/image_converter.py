import base64

file = "static/profile_images/p0.png"

def encode(image_file: str):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read())
        
        print(encoded)
        decode(encoded, 'p0.png')

        
def decode(image_file: bytes, file_name: str = 'sem_nome.png'):
    decoded = base64.b64decode(image_file)
    with open(file_name, "wb") as result:
            result.write(decoded)
    
# encode(file)
