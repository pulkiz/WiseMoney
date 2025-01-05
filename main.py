class ExpenseTracker:
    def __init__(self):
        self.people = []
        self.transactions = []
        self.categories = ["eating outside", "delivery", "grocery", "rent", "cabs/car rentals", "stay", "other expenses"]

    def add_person(self, name):
        self.people.append(name)

    def list_people(self):
        for i, person in enumerate(self.people, 1):
            print(f"{i}. {person}")

    def add_transaction(self, amount, payer, participants, note, category):
        transaction = {
            'amount': amount,
            'payer': payer,
            'participants': participants,
            'note': note,
            'category': category  # Single category instead of multiple tags
        }
        self.transactions.append(transaction)

    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            self.transactions.pop(index)
        else:
            print("Invalid transaction index.")

    def modify_transaction(self, index, amount=None, payer=None, participants=None, note=None, category=None):
        if 0 <= index < len(self.transactions):
            if amount:
                self.transactions[index]['amount'] = amount
            if payer:
                self.transactions[index]['payer'] = payer
            if participants:
                self.transactions[index]['participants'] = participants
            if note:
                self.transactions[index]['note'] = note
            if category:
                self.transactions[index]['category'] = category  # Update single category
        else:
            print("Invalid transaction index.")

    def list_transactions(self):
        if not self.transactions:
            print("No transactions recorded.")
        for i, transaction in enumerate(self.transactions, 1):
            participants_str = ", ".join(transaction['participants'])  # Convert list to comma-separated string
            print(f"{i}. Amount: {transaction['amount']}, Payer: {transaction['payer']}, Participants: {participants_str}")
            print(f"   Note: {transaction['note']}")
            print(f"   Category: {transaction['category']}")  # Single category displayed

    def calculate_debts(self):
        debts = {}
        for transaction in self.transactions:
            amount = transaction['amount']
            payer = transaction['payer']
            participants = transaction['participants']
            split_amount = amount / len(participants)

            for participant in participants:
                if participant != payer:
                    debts[(participant, payer)] = debts.get((participant, payer), 0) + split_amount
        return debts

    def simplify_debts(self, debts):
        net_balances = {}
        for (payer, payee), amount in debts.items():
            net_balances[payer] = net_balances.get(payer, 0) - amount
            net_balances[payee] = net_balances.get(payee, 0) + amount

        debtors = []
        creditors = []
        for person, balance in net_balances.items():
            if balance < 0:
                debtors.append((person, balance))
            elif balance > 0:
                creditors.append((person, balance))

        simplified_transactions = []
        debtors.sort(key=lambda x: x[1])
        creditors.sort(key=lambda x: -x[1])

        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt_amount = debtors[i]
            creditor, credit_amount = creditors[j]

            settlement_amount = min(-debt_amount, credit_amount)
            simplified_transactions.append((debtor, creditor, settlement_amount))

            debtors[i] = (debtor, debt_amount + settlement_amount)
            creditors[j] = (creditor, credit_amount - settlement_amount)

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        return simplified_transactions


# Example usage
def main():
    tracker = ExpenseTracker()

    num_people = int(input("Enter the number of people: "))
    for i in range(num_people):
        name = input(f"Enter name of person {i + 1}: ")
        tracker.add_person(name)

    while True:
        print("\n1. Add transaction")
        print("2. Delete transaction")
        print("3. Modify transaction")
        print("4. List transactions")
        print("5. Calculate and simplify debts")
        print("6. Add new people to group")
        print("7. Exit")
        choice = input("Choose an option:")

        if choice == "1":
            amount = float(input("Enter the amount of the transaction: "))
            tracker.list_people()
            payer_index = int(input("Enter the number of the person who paid: ")) - 1
            num_participants = int(input("Enter number of participants in the transaction: "))
            participants = []
            tracker.list_people()
            for _ in range(num_participants):
                participant_index = int(input("Enter the number of a participant: ")) - 1
                participants.append(tracker.people[participant_index])

            note = input("Enter a note for the transaction: ")
            print("Available categories:")
            for i, category in enumerate(tracker.categories, 1):
                print(f"{i}. {category}")
            category_index = int(input("Choose a category number: ")) - 1
            category = tracker.categories[category_index]  # Select only one category

            tracker.add_transaction(amount, tracker.people[payer_index], participants, note, category)

        elif choice == "2":
            tracker.list_transactions()
            transaction_index = int(input("Enter the number of the transaction to delete: ")) - 1
            tracker.delete_transaction(transaction_index)

        elif choice == "3":
            tracker.list_transactions()
            transaction_index = int(input("Enter the number of the transaction to modify: ")) - 1
            amount = float(input("Enter the new amount (or leave blank to keep unchanged): ") or 0)
            tracker.list_people()
            payer_index = int(input("Enter the new payer (or leave blank to keep unchanged): ") or -1) - 1
            num_participants = int(input("Enter the new number of participants (or leave blank to keep unchanged): ") or 0)
            participants = []
            if num_participants:
                tracker.list_people()
                for _ in range(num_participants):
                    participant_index = int(input("Enter the number of a participant: ")) - 1
                    participants.append(tracker.people[participant_index])

            note = input("Enter a new note (or leave blank to keep unchanged): ") or None
            print("Available categories:")
            for i, category in enumerate(tracker.categories, 1):
                print(f"{i}. {category}")
            category_index = int(input("Choose a new category number (or leave blank to keep unchanged): ") or -1) - 1
            category = tracker.categories[category_index] if category_index != -1 else None

            tracker.modify_transaction(transaction_index, amount or None, tracker.people[payer_index] if payer_index != -1 else None, participants if participants else None, note, category)

        elif choice == "4":
            tracker.list_transactions()

        elif choice == "5":
            if len(tracker.transactions) == 0:
                print("\nNo transactions recorded yet")
                continue
            debts = tracker.calculate_debts()
            simplified_debts = tracker.simplify_debts(debts)
            print("Simplified Debts:")
            for debtor, creditor, amount in simplified_debts:
                print(f"{debtor} pays {creditor} {amount:.2f}")
            x = int(input("\nEnter 1 for main menu or 2 to exit:"))
            if x == 2:
                break

        elif choice == "6":
            for i in range(int(input("Enter number of people to add:"))):
                tracker.add_person(input("Enter name:"))

        elif choice == "7":
            break

if __name__ == '__main__':
    main()