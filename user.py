class User:
    def __init__(self, id) -> None:
        self.id = id
        self.prove = None

    def __str__(self) -> str:
        return f"{self.name}\n{self.bday}\n{self.group}\n{self.learn}\n{self.addr}\n{self.number}"

    def set_name(self, name: str) -> None:
        self.name = name

    def set_birthday(self, bday: str) -> None:
        self.bday = bday

    def set_group(self, group: str) -> None:
        self.group = group

    def set_learn(self, learn: str) -> None:
        self.learn = learn

    def set_addres(self, addres) -> None:
        self.addr = addres

    def set_number(self, number) -> None:
        self.number = number

    def set_prove(self, prove) -> None:
        self.prove = prove
