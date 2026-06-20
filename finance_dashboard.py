import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("finance_data.json")

DEFAULT_DATA = {
    "cash_accounts": {
        "Wells Fargo Checking": 867.76,
        "Wells Fargo Savings": 67.57,
        "Capital One Savings": 1091.66
    },
    "credit_cards": {
        "Wells Fargo Active Cash": {
            "balance": 801.59,
            "limit": 4000.00
        },
        "Capital One Savor": {
            "balance": 1091.66,
            "limit": 3968.04
        }
    },
    "investments": {
        "Acorns Invest": 403.49,
        "Acorns Roth IRA": 39.09
    },
    "credit_scores": [
        {"date": "2026-04-01", "score": 573},
        {"date": "2026-05-28", "score": 597},
        {"date": "2026-06-01", "score": 600},
        {"date": "2026-06-12", "score": 604}
    ]
}


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    save_data(DEFAULT_DATA)
    return DEFAULT_DATA


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def money(amount):
    return f"${amount:,.2f}"


def total_cash(data):
    return sum(data["cash_accounts"].values())


def total_investments(data):
    return sum(data["investments"].values())


def total_debt(data):
    return sum(card["balance"] for card in data["credit_cards"].values())


def total_credit_limit(data):
    return sum(card["limit"] for card in data["credit_cards"].values())


def utilization(data):
    limit = total_credit_limit(data)
    if limit == 0:
        return 0
    return (total_debt(data) / limit) * 100


def net_worth(data):
    return total_cash(data) + total_investments(data) - total_debt(data)


def show_dashboard(data):
    print("\n" + "=" * 55)
    print("PERSONAL FINANCE DASHBOARD")
    print("=" * 55)

    print("\nCASH ACCOUNTS")
    for name, balance in data["cash_accounts"].items():
        print(f"- {name}: {money(balance)}")

    print("\nCREDIT CARDS")
    for name, card in data["credit_cards"].items():
        card_util = (card["balance"] / card["limit"]) * 100 if card["limit"] else 0
        print(f"- {name}: {money(card['balance'])} / {money(card['limit'])} ({card_util:.2f}% used)")

    print("\nINVESTMENTS")
    for name, balance in data["investments"].items():
        print(f"- {name}: {money(balance)}")

    print("\nSUMMARY")
    print(f"Total Cash: {money(total_cash(data))}")
    print(f"Total Investments: {money(total_investments(data))}")
    print(f"Total Credit Card Debt: {money(total_debt(data))}")
    print(f"Overall Credit Utilization: {utilization(data):.2f}%")
    print(f"Estimated Net Worth: {money(net_worth(data))}")

    if data["credit_scores"]:
        latest = data["credit_scores"][-1]
        print(f"Latest Credit Score: {latest['score']} on {latest['date']}")

    print("=" * 55 + "\n")


def update_cash(data):
    name = input("Cash account name: ").strip()
    balance = float(input("Current balance: $"))
    data["cash_accounts"][name] = balance
    save_data(data)
    print("Cash account updated.\n")


def update_credit_card(data):
    name = input("Credit card name: ").strip()
    balance = float(input("Current balance: $"))
    limit = float(input("Credit limit: $"))
    data["credit_cards"][name] = {"balance": balance, "limit": limit}
    save_data(data)
    print("Credit card updated.\n")


def update_investment(data):
    name = input("Investment account name: ").strip()
    balance = float(input("Current balance: $"))
    data["investments"][name] = balance
    save_data(data)
    print("Investment updated.\n")


def add_credit_score(data):
    score = int(input("Credit score: "))
    date = input("Date YYYY-MM-DD or press Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    data["credit_scores"].append({"date": date, "score": score})
    save_data(data)
    print("Credit score added.\n")


def payoff_simulator(data):
    cards = list(data["credit_cards"].keys())
    print("\nChoose a card:")
    for i, card in enumerate(cards, start=1):
        print(f"{i}. {card}")

    choice = int(input("Card number: ")) - 1
    if choice < 0 or choice >= len(cards):
        print("Invalid choice.\n")
        return

    card_name = cards[choice]
    payment = float(input("Payment amount: $"))

    current_balance = data["credit_cards"][card_name]["balance"]
    new_balance = max(current_balance - payment, 0)

    old_util = utilization(data)

    data_copy = json.loads(json.dumps(data))
    data_copy["credit_cards"][card_name]["balance"] = new_balance

    print("\nPAYOFF SIMULATION")
    print(f"{card_name} current balance: {money(current_balance)}")
    print(f"After payment: {money(new_balance)}")
    print(f"Utilization before: {old_util:.2f}%")
    print(f"Utilization after: {utilization(data_copy):.2f}%\n")


def credit_score_history(data):
    print("\nCREDIT SCORE HISTORY")
    for entry in data["credit_scores"]:
        print(f"- {entry['date']}: {entry['score']}")
    print()


def main():
    data = load_data()

    while True:
        print("1. View dashboard")
        print("2. Update cash account")
        print("3. Update credit card")
        print("4. Update investment")
        print("5. Add credit score")
        print("6. Payoff simulator")
        print("7. View credit score history")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_dashboard(data)
        elif choice == "2":
            update_cash(data)
        elif choice == "3":
            update_credit_card(data)
        elif choice == "4":
            update_investment(data)
        elif choice == "5":
            add_credit_score(data)
        elif choice == "6":
            payoff_simulator(data)
        elif choice == "7":
            credit_score_history(data)
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.\n")

        data = load_data()


if __name__ == "__main__":
    main()
