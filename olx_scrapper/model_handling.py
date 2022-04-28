def apple_handling(title):
    path = 'py_playground/inputs/apple_models.txt' 
    models = open(path)
    fullLines = models.read().splitlines()
    models.close()
    title = title.upper()
    for model in fullLines:
        if model in title:
            return model

def samsung_handling(title):
    path = 'py_playground/inputs/samsung_models.txt' 
    models = open(path)
    fullLines = models.read().splitlines()
    models.close()
    title = title.upper()
    for model in fullLines:
        if model in title:
            return model

def lg_handling(title):
    path = 'py_playground/inputs/lg_models.txt' 
    models = open(path)
    fullLines = models.read().splitlines()
    models.close()
    title = title.upper()
    for model in fullLines:
        if model in title:
            return model

def motorola_lenovo_handling(title):
    path = 'py_playground/inputs/motorola_lenovo_models.txt' 
    models = open(path)
    fullLines = models.read().splitlines()
    models.close()
    title = title.upper()
    for model in fullLines:
        if model in title:
            return model