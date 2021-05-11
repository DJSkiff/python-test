import math
from collections import OrderedDict


class NotEnaughValues(Exception):
    value = 'Give area or perimeter!'


class FieldMetaSingeltone (type):
    _field_instances = {}

    def __call__(cls, *args, **kwargs):
        if not cls in cls._field_instances:
            instance = type.__call__(cls, *args, **kwargs)
            cls._field_instances[cls] = instance
            return instance
        else:
            return cls._field_instances[cls]


class Field(metaclass=FieldMetaSingeltone):

    fig_number = 0

    def __init__(self):
        self._figs = OrderedDict()

    def add(self, fig, x=0, y=0, rot=0):
        if isinstance(fig, Group):
            for shape in fig:
                if shape in self._figs.keys():
                    self._figs.pop(shape)
        self._figs[fig] = [x, y, rot]
        self.fig_number = len(self._figs)

    def num(self, fig):
        num = 0
        for shape in self._figs.keys():
            if isinstance(shape, fig):
                num += 1
        return num

    def _moove(self, fig, x, y, rot):
        for shape, coord in self._figs.items():
            if shape == fig:
                coord[0] += x
                coord[1] += y
                coord[2] += rot

    def __getitem__(self, key):
        return list(self._figs[key])

    @property
    def figs(self):
        return list(self._figs.keys())

    @figs.setter
    def figs(self, value):
        pass

    def coord(self, fig):
        for key, item in self._figs.items():
            if key == fig:
                return tuple(item)


class Shape:
    _field = Field()

    def __init__(self, *args, **kwargs):
        self.area = None
        self.perimeter = None
        if len(kwargs) < 1:
            raise NotEnaughValues()
        for param in kwargs:
            if param == 'area':
                self.area = kwargs[param]
            if param == 'perimeter':
                self.perimeter = kwargs[param]

    def move(self, x, y, rot):
        self._field._moove(self, x, y, rot)


class Triangle(Shape):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.perimeter:
            self.perimeter = self.area * 2 + math.sqrt(8)


class Rectangle(Shape):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.area:
            self.area = self.perimeter/2


class Circle(Shape):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.perimeter:
            self.perimeter = math.sqrt(self.area * 4 * math.pi)


class Group(Shape):

    _current = -1

    def __init__(self, *args):
        self._figs = []
        _area = 0
        for shape in args:
            self._figs.append(shape)
            _area += shape.area
        self.area = _area

    def __iter__(self):
        return self

    def __next__(self):
        self._current += 1
        if self._current < len(self._figs):
            return self._figs[self._current]
        raise StopIteration

    @property
    def figs(self):
        return self._figs


def testing():
    field = Field()
    field2 = Field()

    assert field == field2

    triangle = Triangle(area=2)
    square = Rectangle(perimeter=8)
    circle = Circle(area=1)

    try:
        e = Circle()
    except NotEnaughValues:
        pass

    assert circle.area == 1
    assert square.area == 4
    assert triangle.area == 2

    r = math.sqrt(1/math.pi)
    assert circle.perimeter == 2 * math.pi * r
    assert square.perimeter == 8
    assert triangle.perimeter == 4 + math.sqrt(8)

    field.add(triangle, x=1, y=3)
    field.add(square, y=8, rot=45)
    field.add(circle, x=7, y=5)

    assert field.fig_number == 3
    assert field.num(Triangle) == 1
    assert field.num(Rectangle) == 1
    assert field.num(Circle) == 1
    assert field.figs == [triangle, square, circle]

    assert field.coord(triangle) == (1, 3, 0)
    assert field.coord(square) == (0, 8, 45)
    assert field.coord(circle) == (7, 5, 0)

    triangle.move(x=3, y=1, rot=15)

    assert field.coord(triangle) == (4, 4, 15)

    group = Group(circle, square)
    field.add(group)

    field.coord(group) == (0, 0, 0)
    assert field.figs == [triangle, group]
    assert group.figs == [circle, square]

    group.move(x=10, y=10, rot=45)

    assert field.coord(group) == (10, 10, 45)
    assert field.coord(circle) == None
    assert field.coord(square) == None
    assert field.fig_number == 2

    assert group.area == 5


if __name__ == "__main__":

    testing()
