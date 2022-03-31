"""Task: Сделать класс определяющий прямоугольный земельный
участок. Реализовать операции сравнения участков по
площади. Определить метод, проверяющий, можно ли
сложить/вычесть 2 участка (одна из сторон совпадает по
длине). Реализовать методы сложения/вычитания
участков."""


class AddLandPlotsException(Exception):
    pass


class SubstractLandPlotsException(Exception):
    pass


class LandPlot:
    def __init__(self, height=10, width=10):
        self.height = height
        self.width = width
        self.square = self.height * self.width

    def __eq__(self, other):
        return self.square == other.square

    def __ne__(self, other):
        return self.square != other.square

    def __lt__(self, other):
        return self.square < other.square

    def __gt__(self, other):
        return self.square > other.square

    def __le__(self, other):
        return self.square <= other.square

    def __ge__(self, other):
        return self.square >= other.square

    def __add__(self, other):
        if self.width == other.width:
            self.height += other.height
        elif self.height == other.height:
            self.width += other.width
        else:
            raise AddLandPlotsException("Can't add one plot to another")
        return self.height, self.width

    def __sub__(self, other):
        if self.width == other.width:
            self.height -= other.height
        elif self.height == other.height:
            self.width -= other.width
        else:
            raise SubstractLandPlotsException("Can't substract one plot from another")
        return self.height, self.width


land1 = LandPlot(height=10, width=20)
land2 = LandPlot(height=10, width=30)

print(land1 + land2)
land2.width += 20  # чтобы произвести вычитание прямоугольников
print(land1 - land2)

# сравнение по пллощади
print(land1 == land2)
print(land1 != land2)
print(land1 > land2)
print(land1 < land2)
print(land1 >= land2)
print(land1 <= land2)
