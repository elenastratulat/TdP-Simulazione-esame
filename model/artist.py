from dataclasses import dataclass


@dataclass

class Artist:
    ArtistId: int
    Name: str

    def __hash__(self):
        return hash(self.ArtistId)


    def __str__(self):
        return f"{self.Name}"