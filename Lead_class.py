class Lead:
    def __init__(self, name: str):
        self.name = name


def change_name(lead: Lead, new_name: str) -> None:
    lead.name = new_name


lead = Lead("Иван")
print(lead.name)

change_name(lead, "Илья")
print(lead.name)
