import logging

def initilise_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('food-flex')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='data/foodflex.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger