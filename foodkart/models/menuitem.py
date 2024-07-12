from dataclasses import dataclass, asdict, field

@dataclass
class MenuItem:
    name: str
    price: int
    id: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, d):
        return MenuItem(**d)
    def to_dict(self):
        return asdict(self)