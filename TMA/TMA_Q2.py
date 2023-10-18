from abc import ABC, abstractmethod

class Deli(ABC):
    standard_expiry_hours = 2

    def __init__(self, deliCode, name, price, fat, carbohydrates, protein):
        self._deliCode = deliCode
        self._name = name
        self._price = price
        self._fat = fat
        self._carbohydrates = carbohydrates
        self._protein = protein

    @property
    def deliCode(self):
        return self._deliCode

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def fat(self):
        return self._fat

    @property
    def calories(self):
        return (self._fat * 9) + (self._carbohydrates * 4) + (self._protein * 4)

    @abstractmethod
    def expiryHours(self):
        pass

    def __str__(self):
        return f"{self._deliCode} - {self._name}     Price: ${self._price:.2f}   Fat: {self._fat}"

class ColdDeli(Deli):
    def __init__(self, deliCode, name, price, fat, carbohydrates, protein, storageTemperature):
        super().__init__(deliCode, name, price, fat, carbohydrates, protein)
        self._storageTemperature = storageTemperature

    def expiryHours(self):
        if self._storageTemperature <= 10:
            return 0.5
        elif self._storageTemperature <= 15:
            return 1.0
        elif self._storageTemperature <= 20:
            return 1.5
        else:
            return self.standard_expiry_hours

class HotDeli(Deli):
    _COOKING_STYLE_EXPIRY = {
        "Baking": 2.3,
        "Grilling": 2.5,
        "Frying": 2.0
    }

    def __init__(self, deliCode, name, price, fat, carbohydrates, protein, cookingStyle):
        super().__init__(deliCode, name, price, fat, carbohydrates, protein)
        self._cookingStyle = cookingStyle

    def expiryHours(self):
        if self._cookingStyle in self._COOKING_STYLE_EXPIRY:
            return self._COOKING_STYLE_EXPIRY[self._cookingStyle]
        else:
            return self.standard_expiry_hours

# Create Deli objects
deli1 = ColdDeli("C001", "Smoked Duck Salad", 3.00, 12.5, 23, 0, 16)
deli2 = HotDeli("H001", "Croissant", 2.00, 7.5, 13.4, 0, "Baking")

# Print Deli object details
print(deli1)
print(deli2)
