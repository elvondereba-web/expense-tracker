import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
DATA_FILE = "expenses.json"
# Load data from JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        # Save data to JSON
        def save_data(expenses):
            with open(DATA_FILE, "w") as f:
                json.dump(expenses, f, indent=4)
                # Streamlit App UI & Layout
                st.title("Expense Tracker Dashboard")
                # Load current expenses
                expenses = load_data()
                st.sidebar.header("Add New Expense")
                with st.sidebar.form("expense_form"):
                    amount = st.number_input("Amount", min_value=0.0, format="%.2F")
                    category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
                    date = st.date_input("date", datetime.today())
                    description = st.text_input("Description")
                    submitted = st.form_submit_button("Add Expense")
                    if submitted:
                        new_expense = {
                            "amount": amount,
                            "categorey": category,
                            "date": str(date),
                            "description": description,
                        }
                        expenses.append(new_expense)
                        save_data(expenses)
                        st.success("Expense added successfully!")
                        st.rerun()
                        st.title("Expense Tracker Dashboard")
                        if not expenses:
                            st.info("No expenses recorded yet. Use the sidebar to add your first expense!")
                        else:
                            df = pd.DataFrame(expenses)
                            df['date'] = pd.to_datetime(df['date'])
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Total Spent", f"${df['amount'].sum():,.2f}")
                            col2.metric("Total Transactions", len(df))
                            col3.metric("Average Expense", f"${df['amount'].mean():,.2f}")
                            st.divider()
                            st.subheader("Transaction History")
                            st.dateframe(df, use_container_width=True)
                            st.subheader("Spending by Category")
                            category_df = df.groupby("category")["amount"].sum()
                            st.bar_chart(category_df)
                            st.subheader("Spending Over Time")
                            timeline_df = df.groupby(df['date'].dt.date)["amount"].sum()
                            st.line_chart(timeline_df)
                        