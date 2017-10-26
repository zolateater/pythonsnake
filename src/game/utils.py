class Position():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    @property 
    def x(self) -> int:
        return self.x

    def withX(self, x: int) -> 'Position':
        return Position(x, self.y)
    
    @property
    def y(self) -> int:
        return self.y

    def withY(self, y: int) -> 'Position':
        return Position(self.x, y)
        
    
