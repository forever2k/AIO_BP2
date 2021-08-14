from random import randint

def generate_number(id):
    id_generate = str(id) + "_"
    for i in range(0, 6):
        id_generate = id_generate + str(randint(1, 10))
    return id_generate

