from dataclasses import dataclass, asdict, field

@dataclass
class Entity:
    name: str
    id: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, d):
        return Entity(**d)
    def to_dict(self):
        return asdict(self)