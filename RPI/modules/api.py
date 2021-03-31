import requests
r = requests.get('https://www.python.org')
print(r.content)


class Api:
    def __init__(self):
        print("api created")
        self.testvalue = "first value"

    def test(self):
        print("test")