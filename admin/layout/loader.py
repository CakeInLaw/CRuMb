from flet import Container, Text


class Loader(Container):
    def __init__(self):
        super().__init__()
        self.content = Text('Загрузка...')
