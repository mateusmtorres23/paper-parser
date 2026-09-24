from dataclasses import dataclass

@dataclass
class Section:
    header: str
    content: str

    def __repr__(self) -> str:
        return self.header