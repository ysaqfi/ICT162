class Order:
    _NEXT_ID = 1
    _DELIVERY_FEE = 1.99

    @classmethod
    def getApplicableDiscounts(cls, dob):
        discounts = []
        birth_year = int(dob.split("-")[2])
        current_year = 2023  # You may need to update the current year as necessary

        # PioneerDiscount
        if current_year - birth_year >= 16 and birth_year <= 1965:
            discounts.append(PioneerDiscount())

        # MerdekaDiscount
        if current_year - birth_year >= 64 and not discounts:
            if PriceDiscount not in discounts:
                discounts.append(MerdekaDiscount())

        # PriceDiscount
        if PriceDiscount not in discounts:
            discounts.append(PriceDiscount())

        # NationalDayDiscount
        if dob.endswith("-08-09") or dob == "09-Aug-1965":
            discounts.append(NationalDayDiscount())

        return discounts

    @classmethod
    def setNextID(cls, order_date):
        order_id = f"{order_date}{cls._NEXT_ID:03d}"
        cls._NEXT_ID += 1
        return order_id

    def __init__(self, participant, deliSet, orderID=None):
        self._participant = participant
        self._deliSet = deliSet

        if orderID is None:
            order_date = "20230911"  # You may need to update this date as necessary
            self._orderID = self.setNextID(order_date)
        else:
            self._orderID = orderID

        self._discounts = self.getApplicableDiscounts(self._participant.getDOB())

    def getDeliveryFee(self):
        if self._participant.isHandicapped():
            return 0
        else:
            return self._DELIVERY_FEE

    @property
    def price(self):
        deliSet_price = self._deliSet.getPrice()
        total_discount = sum(discount.getDiscount(deliSet_price) for discount in self._discounts)
        final_price = max(deliSet_price - total_discount + self.getDeliveryFee(), 0)
        return final_price

    def getDetails(self):
        deliCodes = ",".join(self._deliSet.getDeliCodes())
        return f"{self._orderID},{self._participant.getID()},{self._deliSet.getType()},{self._deliSet.getName()},{deliCodes}"

    def __str__(self):
        participant_info = f"ID: {self._participant.getID()} Name: {self._participant.getName()} Age: {self._participant.getAge()}"
        deliSet_info = f"DeliSet: {self._deliSet.getName()} Price: ${self._deliSet.getPrice():.2f}\n\twith {', '.join(self._deliSet.getDeliCodes())}"
        discounts_info = "Discounts: " + "   ".join(f"${discount.getDiscount(self._deliSet.getPrice()):.2f}" for discount in self._discounts)
        delivery_fee_info = f"Delivery Fee: ${self.getDeliveryFee():.2f}"
        final_price_info = f"Final Price: ${self.price:.2f}"

        return f"Order ID: {self._orderID}\n{participant_info}\n{deliSet_info}\n{discounts_info}\n{delivery_fee_info}\n{final_price_info}\nConsume in {self._deliSet.getConsumptionTime()} hrs"
