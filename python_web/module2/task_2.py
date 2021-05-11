from typing import List
import inspect


class Story(List):

    def __repr__(self):
        return self

    def add(self, diagnose):
        print(inspect.stack())
        self.append(diagnose)


class Person:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class Doctor(Person):

    def __init__(self, name, surname, post):
        super().__init__(name, surname)
        self.post = post


class Pacient(Person):

    def __init__(self, name, surname, mip):
        super().__init__(name, surname)
        self.mip = mip
        self.story = Story()


doctor_surg = Doctor('Bill', 'Klinton', 'Head of surgery dep.')
doctor_tera = Doctor('Monika', 'Levinsky', 'Therapist')

pac1 = Pacient('Geoge', 'Bush', 128712678213)
pac2 = Pacient('Barak', 'Obama', 598624093862)

assert pac1.story == []
assert pac2.story == []

pac1.story.add('flue')
