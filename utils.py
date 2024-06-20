import requests


def random_duck() -> str:
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

random_duck()

def random_fox() -> str:
    url = 'https://randomfox.ca/floof'
    res = requests.get(url)
    data = res.json()
    return data['image']

random_fox()

def random_dog() -> str:
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

random_dog()