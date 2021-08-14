from random import randint


async def generate_number(id):
    id_generate = id + "_"
    for i in range(0, 10):
        id_generate = id_generate + str(randint(1, 10))
    return id_generate

