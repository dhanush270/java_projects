import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date,get_amount,get_category,get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_File="finance_data.csv"
    COLUMNS=["date","amount","category","description"]
    FORMAT="%d-%m-%Y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_File)
        except FileNotFoundError:
            df=pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_File,index=False)

    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry={
            "date":date,
            "amount":amount,
            "category":category,
            "description":description,
        }
        with open(cls.CSV_File,"a",newline="")as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added sucessfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        cls.initialize_csv()  
        df = pd.read_csv(cls.CSV_File)
    
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, errors="coerce")
    
        df = df.dropna(subset=["date"])

        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            filtered_df["date"] = filtered_df["date"].dt.strftime(cls.FORMAT)
        
        print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}:")
        print(filtered_df.to_string(index=False))

        filtered_df["amount"] = pd.to_numeric(filtered_df["amount"], errors="coerce").fillna(0)
        
        
        total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
        total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
        
        print("\nSummary:")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
        CSV.initialize_csv()
        date=get_date(
        "enter the date of transaction (dd--mm--yyyy) or today's date: ",allow_default=True,
        )
        amount=get_amount()
        category=get_category()
        description=get_description()
        CSV.add_entry(date,amount,category,description)

import pandas as pd
import matplotlib.pyplot as plt

def plot_transactions(df):
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df = df.dropna(subset=["date"])  
    df.set_index("date", inplace=True)

    
    income_df = df[df["category"] == "Income"].resample("D")["amount"].sum()
    expense_df = df[df["category"] == "Expense"].resample("D")["amount"].sum()

    all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")
    income_df = income_df.reindex(all_dates, fill_value=0)
    expense_df = expense_df.reindex(all_dates, fill_value=0)

    
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df, label="Income", color="g")
    plt.plot(expense_df.index, expense_df, label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid()
    plt.show()


def main():
        while True:
            print("\n1. Add a new Transaction")
            print("2. View transactions and summary within a date range")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")

            if choice == "1":
                add()
            elif choice == "2":
                start_date = get_date("Enter the start date (dd-mm-yyyy): ")
                end_date = get_date("Enter the end date (dd-mm-yyyy): ")
                df=CSV.get_transactions(start_date, end_date)
                if input("Do you want to see a plot? (y/n) ").lower()=="y":
                    plot_transactions(df)
            elif choice == "3":
                 print("Exiting...")
                 break
            else:
                 print("Invalid choice, please try again.")

if __name__ == "__main__":
        main()







