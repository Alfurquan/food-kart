from dataclasses import dataclass, asdict, field

@dataclass
class Customer:
    name: str = None
    phone: str = None
    id: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, d):
        return Customer(**d)
    
    def to_dict(self):
        return asdict(self)