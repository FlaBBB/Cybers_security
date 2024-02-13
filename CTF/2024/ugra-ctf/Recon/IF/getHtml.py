import requests

data = requests.get('https://if.q.2024.ugractf.ru/j361boy9zihi7ocv/').content
with open("chall.html", "wb") as file:
    file.write(data)