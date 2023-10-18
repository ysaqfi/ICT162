class ERPException(Exception):
    pass

class DeliSet:
    def __init__(self, name, deli):
        self._name = name
        self._deliList = [deli]

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return sum(deli.price for deli in self._deliList)

    @property
    def consumeBy(self):
        return min(deli.expireHours for deli in self._deliList)

    @property
    def totalFat(self):
        return sum(deli.fatContent for deli in self._deliList)

    @property
    def totalCalories(self):
        return sum(deli.calories for deli in self._deliList)

    def setType(self):
        return type(self)._SET_TYPE

    def getDeliCodes(self):
        return ",".join(deli.deliCode for deli in self._deliList)

    def addDeli(self, deli):
        if deli.deliCode in [d.deliCode for d in self._deliList]:
            raise ERPException("Deli with the same code already exists in this DeliSet.")
        self._deliList.append(deli)

    def __str__(self):
        deli_names = ", ".join(deli.name for deli in self._deliList)
        return f"DeliSet: {self._name} Price: ${self.price:.2f} Consume in {self.consumeBy} hrs with {deli_names}"

class EconSet(DeliSet):
    _MAX_DELI = 5
    _MAX_PRICE = 20.0
    _SET_TYPE = "EconSet"

    def addDeli(self, deli):
        if len(self._deliList) >= self._MAX_DELI:
            raise ERPException("Exceeded maximum number of Delis for EconSet.")
        if self.price + deli.price > self._MAX_PRICE:
            raise ERPException("Exceeded maximum price for EconSet.")
        super().addDeli(deli)

class LowFatSet(DeliSet):
    _MAX_FAT_PERCENT = 0.1  # 10% of total calories
    _SET_TYPE = "LowFatSet"

    def addDeli(self, deli):
        if (self.totalFat + deli.fatContent) > (self.totalCalories * self._MAX_FAT_PERCENT):
            raise ERPException("Exceeded maximum fat content for LowFatSet.")
        super().addDeli(deli)

class LowCarbSet(DeliSet):
    _MAX_CALORIES = 600  # Maximum total calories
    _SET_TYPE = "LowCarbSet"

    def addDeli(self, deli):
        if (self.totalCalories + deli.calories) > self._MAX_CALORIES:
            raise ERPException("Exceeded maximum total calories for LowCarbSet.")
        super().addDeli(deli)

def main():
    # Create Delis (you would need to define Deli class separately)
    class Deli:
        def __init__(self, deliCode, name, price, expireHours, fatContent, calories):
            self.deliCode = deliCode
            self.name = name
            self.price = price
            self.expireHours = expireHours
            self.fatContent = fatContent
            self.calories = calories

    # Create DeliSet objects
    econ_set = EconSet("Econ Lunch", Deli("H006", "Deli1", 5.0, 2.0, 1.5, 300))
    low_fat_set = LowFatSet("Low Fat Lunch", Deli("H003", "Deli2", 4.0, 1.5, 0.5, 250))
    low_carb_set = LowCarbSet("Low Carb Lunch", Deli("C004", "Deli3", 6.0, 3.0, 0.8, 400))

    # Add Delis to the DeliSets
    try:
        econ_set.addDeli(Deli("C005", "Deli4", 3.0, 1.0, 0.2, 150))
        econ_set.addDeli(Deli("H010", "Deli5", 4.0, 2.0, 0.7, 200))
        
        low_fat_set.addDeli(Deli("H002", "Deli6", 3.5, 2.0, 0.4, 180))
        low_fat_set.addDeli(Deli("C003", "Deli7", 2.5, 1.5, 0.3, 120))
        low_fat_set.addDeli(Deli("C001", "Deli8", 2.0, 2.5, 0.1, 100))

        low_carb_set.addDeli(Deli("C007", "Deli9", 3.0, 2.0, 0.6, 350))
        low_carb_set.addDeli(Deli("H013", "Deli10", 4.0, 2.5, 0.8, 380))
        low_carb_set.addDeli(Deli("H012", "Deli11", 5.0, 3.0, 1.0, 420))
        low_carb_set.addDeli(Deli("H009", "Deli12", 6.0, 3.5, 1.2, 480))
    except ERPException as e:
        print(f"Exception: {e}")

    # Print the string representation of the created DeliSet objects
    print(econ_set)
    print(low_fat_set)
    print(low_carb_set)

if __name__ == "__main__":
    main()
