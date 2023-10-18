from datetime import datetime

class Participant:
    def __init__(self, id, name, dob, handicapped=False):
        self._id = id
        self._name = name
        self._dob = dob
        self._handicapped = handicapped

    @property
    def id(self):
        return self._id

    @property
    def dob(self):
        return self._dob

    @property
    def handicapped(self):
        return self._handicapped

    def getAge(self):
        current_year = datetime.now().year
        participant_year = self._dob.year
        age = current_year - participant_year
        return age

    def __str__(self):
        return f"ID: {self._id}\nName: {self._name}\nAge: {self.getAge()}"

