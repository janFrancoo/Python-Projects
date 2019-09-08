import requests

url = "http://data.fixer.io/api/latest?access_key=02bd1b7b5f441668e9463d2dc40d7503"

first_currency = input(First currency: ")
second_currency = input("Second currency: ")
amount = int(input("Amount: "))

response = requests.get(url)

infos = response.json()

firstValue = infos["rates"][first_currency]
secondValue = infos["rates"][second_currency]

print((secondValue / firstValue) * amount)
