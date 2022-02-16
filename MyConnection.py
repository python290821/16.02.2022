class MyConnection():
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return f'Connection number: {self.number}'