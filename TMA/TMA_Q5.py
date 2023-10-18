class Participant:
    def __init__(self, nric, name):
        self.nric = nric
        self.name = name
        self.discounts = []

    def addDiscount(self, discount):
        self.discounts.append(discount)

    # Define other methods for managing participant details as needed.
class DeliSet:
    def __init__(self, set_name):
        self.set_name = set_name
        self.selected_delis = []

    def addDeli(self, deli):
        self.selected_delis.append(deli)

    def calculateTotalPrice(self):
        total_price = sum(deli.price for deli in self.selected_delis)
        return total_price

    # Define other methods for managing the DeliSet as needed.
class Order:
    _next_id = 1

    def __init__(self, participant, deli_set):
        self.order_id = Order._next_id
        self.participant = participant
        self.deli_set = deli_set
        Order._next_id += 1

    @staticmethod
    def setNextID(next_id):
        Order._next_id = next_id

    def getDetails(self):
        details = f"Order ID: {self.order_id}\n"
        details += f"Participant: {self.participant.name}\n"
        details += f"DeliSet: {self.deli_set.set_name}\n"
        details += f"Total Price: ${self.deli_set.calculateTotalPrice():.2f}"
        return details

    # Define other methods for managing order details as needed.
class Discount:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    # Define other methods for managing discount details as needed.



class EatRightAdmin:
    _DAILY_QUOTA = 2

    def __init__(self):
        self._participants = {}  # Dictionary to store participants
        self._delis = {}         # Dictionary to store Delis
        self._orders = []        # List to store Order objects
        Order.setNextID(self.readOrders())  # Set the next order ID based on existing orders

    def setupParticipants(self):
        # Read and populate participants from "Participants.txt" (Appendix A)
        pass

    def setupDelis(self):
        # Read and populate delis from "Delis.txt" (Appendix B)
        pass

    def readOrders(self):
        # Read orders for the next day and return the last order ID if any (Appendix C)
        pass

    def searchParticipant(self, id):
        # Search and return a Participant object by ID or return None if not found
        pass

    def searchDeli(self, code):
        # Search and return a Deli object by code or return None if not found
        pass

    def listDeliInventory(self):
        # Format and return a string representation of all Deli objects
        pass

    def countOrders(self, id):
        # Count the number of orders for a participant by ID
        pass

    def listOrders(self, id):
        # List all orders for a participant by ID
        pass

    def addOrder(self, participant, deli_set):
        # Add a new order and return the Order object if successful, raise an exception if not
        pass

    def saveOrders(self):
        # Save the order details to a file for the next day (Appendix C)
        pass

# Application for ERP participants to submit and enquire their orders
def main():
    erp_admin = EatRightAdmin()

    while True:
        print("Healthier SG: Eat-Right Programme")
        print("===================================")
        print("1. Order DeliSet")
        print("2. List Orders")
        print("3. Quit")

        choice = input("Enter choice: ")

        if choice == "1":
            # Order DeliSet
            nric = input("Enter NRIC to start your order(s): ")
            participant = erp_admin.searchParticipant(nric)

            if participant is None:
                print("You did not sign up for this program.")
                continue

            print("You are entitled to the following discount(s):")
            for discount in participant.discounts:
                print(f"{discount.name}: {discount.amount} discount")

            set_name = input("Enter your customised set name: ")
            print("Available Deli:")
            print("===============")
            print(erp_admin.listDeliInventory())
            print("Enter Deli codes to assemble your DeliSet (Press Enter to complete):")

            deli_set = DeliSet(set_name)  # Create an empty DeliSet

            while True:
                deli_code = input("Select Deli by entering the code (Press Enter to stop Deli): ")
                if not deli_code:
                    break

                deli = erp_admin.searchDeli(deli_code)
                if deli is None:
                    print("Invalid Deli code. Please re-enter.")
                    continue

                try:
                    deli_set.addDeli(deli)
                except DeliSetException as e:
                    print(e)

            try:
                order = erp_admin.addOrder(participant, deli_set)
                print("Order submitted successfully:")
                print(order.getDetails())
            except ERPException as e:
                print(e)

        elif choice == "2":
            # List Orders
            nric = input("Enter NRIC to list your orders: ")
            participant = erp_admin.searchParticipant(nric)

            if participant is None:
                print("Participant not found.")
                continue

            orders = erp_admin.listOrders(participant.id)
            if not orders:
                print("You did not order any DeliSet.")
            else:
                print("Your order(s) for the next day:")
                print("=============================")
                for order in orders:
                    print(order.getDetails())

        elif choice == "3":
            # Quit
            erp_admin.saveOrders()
            print("Thank you for using the Eat-Right Programme. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
