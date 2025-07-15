
"""Personal Finance Calculator

A comprehensive Python-based calculator for personal finance management and planning.
This module provides various financial calculations including loan payments,
compound interest, simple interest, budget tracking, and savings goal planning.

Author: Biraj M
Repository: https://github.com/birajm/personalfinancecalculator
License: MIT
Version: 1.0.0
"""

import math
from typing import List, Tuple, Optional


def display_menu() -> None:
    """
    Display the main menu options for the Personal Finance Calculator.

    Prints a formatted menu with all available calculator options.
    """
    print("\n" + "=" * 50)
    print("         PERSONAL FINANCE CALCULATOR")
    print("=" * 50)
    print("1. Loan Payment Calculator")
    print("2. Compound Interest Calculator")
    print("3. Simple Interest Calculator")
    print("4. Budget Tracker")
    print("5. Saving Goal Calculator")
    print("6. Exit")
    print("=" * 50)


def get_positive_number(prompt: str) -> float:
    """
    Get a positive number from user with validation.

    Args:
        prompt (str): The prompt message to display to the user

    Returns:
        float: A positive number entered by the user

    Raises:
        Continues to prompt until a valid positive number is entered
    """
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a positive number.")


def get_number(prompt: str) -> float:
    """
    Get any number from user with validation.

    Args:
        prompt (str): The prompt message to display to the user

    Returns:
        float: A number entered by the user

    Raises:
        Continues to prompt until a valid number is entered
    """
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def loan_payment_calculator() -> None:
    """
    Calculate monthly loan payment using the standard loan payment formula.

    Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
    Where:
        M = Monthly payment
        P = Principal (loan amount)
        r = Monthly interest rate (annual rate / 12)
        n = Number of payments (years * 12)

    For zero interest rate, uses simple division: M = P / n

    Displays:
        - Monthly payment amount
        - Total interest paid
        - Total amount paid over loan term
    """
    print("\n--- LOAN PAYMENT CALCULATOR ---")

    # Get input values
    principal = get_positive_number("Enter loan amount ($): ")
    annual_rate = get_positive_number("Enter annual interest rate (%): ")
    years = get_positive_number("Enter loan term (years): ")

    # Convert to monthly values
    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12

    # Calculate monthly payment
    if monthly_rate == 0:
        if num_payments == 0:
            print("Error: Loan term cannot be zero with a 0% interest rate.")
            return
        monthly_payment = principal / num_payments
    else:
        # Standard loan payment formula
        denominator = ((1 + monthly_rate) ** num_payments - 1)
        if denominator == 0:
            print("Error: Cannot calculate monthly payment with given parameters.")
            return
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / denominator

    # Calculate total amounts
    total_payment = monthly_payment * num_payments
    total_interest = total_payment - principal

    # Display results
    print(f"\n--- LOAN PAYMENT RESULTS ---")
    print(f"Loan Amount: ${principal:,.2f}")
    print(f"Interest Rate: {annual_rate:.2f}% annually")
    print(f"Loan Term: {years:.0f} years ({num_payments:.0f} months)")
    print(f"Monthly Payment: ${monthly_payment:,.2f}")
    print(f"Total Interest: ${total_interest:,.2f}")
    print(f"Total Payment: ${total_payment:,.2f}")


def compound_interest_calculator() -> None:
    """
    Calculate compound interest using the compound interest formula.

    Formula: A = P(1 + r/n)^(nt)
    Where:
        A = Final amount
        P = Principal amount
        r = Annual interest rate (decimal)
        n = Number of times interest is compounded per year
        t = Time in years

    Supports various compounding frequencies:
        - Annually (1 time per year)
        - Semi-annually (2 times per year)
        - Quarterly (4 times per year)
        - Monthly (12 times per year)
        - Daily (365 times per year)

    Displays:
        - Final amount after compound interest
        - Total interest earned
        - Growth factor (multiplier)
    """
    print("\n--- COMPOUND INTEREST CALCULATOR ---")

    # Get input values
    principal = get_positive_number("Enter principal amount ($): ")
    annual_rate = get_positive_number("Enter annual interest rate (%): ")
    years = get_positive_number("Enter time period (years): ")

    # Compounding frequency options
    print("\nCompounding frequency:")
    print("1. Annually (1)")
    print("2. Semi-annually (2)")
    print("3. Quarterly (4)")
    print("4. Monthly (12)")
    print("5. Daily (365)")

    frequency_options = {1: 1, 2: 2, 3: 4, 4: 12, 5: 365}
    compound_frequency = 0

    while True:
        try:
            choice = int(input("Select compounding frequency (1-5): "))
            if choice in frequency_options:
                compound_frequency = frequency_options[choice]
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Convert percentage to decimal
    rate = annual_rate / 100

    # Calculate compound interest
    final_amount = principal * (1 + rate / compound_frequency) ** (compound_frequency * years)
    interest_earned = final_amount - principal

    # Display results
    print(f"\n--- COMPOUND INTEREST RESULTS ---")
    print(f"Principal: ${principal:,.2f}")
    print(f"Interest Rate: {annual_rate:.2f}% annually")
    print(f"Time Period: {years:.2f} years")
    print(f"Compounding: {compound_frequency} times per year")
    print(f"Final Amount: ${final_amount:,.2f}")
    print(f"Interest Earned: ${interest_earned:,.2f}")
    if principal > 0:
        print(f"Growth Factor: {final_amount / principal:.2f}x")


def simple_interest_calculator() -> None:
    """
    Calculate simple interest using the simple interest formula.

    Formula: I = P * r * t
    Where:
        I = Interest earned
        P = Principal amount
        r = Annual interest rate (decimal)
        t = Time in years

    Final Amount = Principal + Interest

    Displays:
        - Simple interest earned
        - Final amount (principal + interest)
    """
    print("\n--- SIMPLE INTEREST CALCULATOR ---")

    # Get input values
    principal = get_positive_number("Enter principal amount ($): ")
    annual_rate = get_positive_number("Enter annual interest rate (%): ")
    years = get_positive_number("Enter time period (years): ")

    # Convert percentage to decimal
    rate = annual_rate / 100

    # Calculate simple interest
    interest = principal * rate * years
    final_amount = principal + interest

    # Display results
    print(f"\n--- SIMPLE INTEREST RESULTS ---")
    print(f"Principal: ${principal:,.2f}")
    print(f"Interest Rate: {annual_rate:.2f}% annually")
    print(f"Time Period: {years:.2f} years")
    print(f"Simple Interest: ${interest:,.2f}")
    print(f"Final Amount: ${final_amount:,.2f}")


def budget_tracker() -> None:
    """
    Track income and expenses to calculate budget balance and savings rate.

    Allows users to:
        - Enter multiple income sources
        - Enter multiple expense categories
        - Calculate net income (income - expenses)
        - Calculate savings rate ((net income / total income) * 100)
        - Provide budget analysis and recommendations

    Displays:
        - Detailed income breakdown
        - Detailed expense breakdown
        - Net income calculation
        - Savings rate percentage
        - Budget recommendations
    """
    print("\n--- BUDGET TRACKER ---")

    # Initialize variables
    total_income = 0
    total_expenses = 0
    income_items: List[Tuple[str, float]] = []
    expense_items: List[Tuple[str, float]] = []

    # Get income information
    print("\n--- INCOME TRACKING ---")
    while True:
        income_source = input("Enter income source (or 'done' to finish): ").strip()
        if income_source.lower() == 'done':
            break

        amount = get_positive_number(f"Enter amount for {income_source}: $")
        income_items.append((income_source, amount))
        total_income += amount

    # Get expense information
    print("\n--- EXPENSE TRACKING ---")
    while True:
        expense_category = input("Enter expense category (or 'done' to finish): ").strip()
        if expense_category.lower() == 'done':
            break

        amount = get_positive_number(f"Enter amount for {expense_category}: $")
        expense_items.append((expense_category, amount))
        total_expenses += amount

    # Calculate budget balance
    net_income = total_income - total_expenses
    saving_rate = (net_income / total_income * 100) if total_income > 0 else 0

    # Display results
    print(f"\n--- BUDGET SUMMARY ---")
    print(f"\nINCOME:")
    for source, amount in income_items:
        print(f"  {source}: ${amount:,.2f}")
    print(f"Total Income: ${total_income:,.2f}")

    print(f"\nEXPENSES:")
    for category, amount in expense_items:
        print(f"  {category}: ${amount:,.2f}")
    print(f"Total Expenses: ${total_expenses:,.2f}")

    print(f"\nBUDGET ANALYSIS:")
    print(f"Net Income: ${net_income:,.2f}")
    print(f"Savings Rate: {saving_rate:.2f}%")

    # Provide recommendations
    if net_income > 0:
        print("✅ You have a budget surplus! Consider saving or investing.")
    elif net_income == 0:
        print("⚠️ You're breaking even. Consider increasing income or reducing expenses.")
    else:
        print("❌ You have a budget deficit. You need to reduce expenses or increase income.")


def savings_goal_calculator() -> None:
    """
    Calculate required monthly savings to reach a financial goal.

    Takes into account:
        - Target savings goal
        - Current savings amount
        - Time frame to reach goal
        - Expected annual return rate
        - Growth of current savings over time

    Uses future value of annuity formula for calculating required monthly payments:
    PMT = FV / [((1 + r)^n - 1) / r]

    Where:
        PMT = Required monthly payment
        FV = Future value needed (goal - future value of current savings)
        r = Monthly interest rate
        n = Number of months

    Displays:
        - Required monthly savings amount
        - Total contributions needed
        - Expected growth from returns
        - Weekly and daily savings equivalents
        - Personalized recommendations
    """
    print("\n--- SAVINGS GOAL CALCULATOR ---")

    # Get input values
    goal_amount = get_positive_number("Enter your savings goal amount ($): ")
    current_savings = get_number("Enter current savings amount ($): ")
    time_years = get_positive_number("Enter time to reach goal (years): ")
    annual_return = get_number("Enter expected annual return rate (%, 0 for no growth): ")

    # Check if goal is already met
    if current_savings >= goal_amount:
        print(f"\n🎉 Congratulations! You've already reached your goal!")
        print(f"You have ${current_savings:,.2f} and your goal is ${goal_amount:,.2f}")
        return

    # Calculate required additional savings
    amount_needed = goal_amount - current_savings

    # Convert to monthly values
    monthly_return = annual_return / 100 / 12
    months = time_years * 12

    # Calculate monthly savings needed
    if monthly_return == 0:
        if months == 0:
            print("Error: Time to reach goal cannot be zero with 0% return.")
            return
        monthly_savings = amount_needed / months
    else:
        # Calculate future value of current savings
        future_value_current_savings = current_savings * (1 + monthly_return) ** months

        # Remaining amount needed after current savings grow
        remaining_needed_after_growth = goal_amount - future_value_current_savings

        if remaining_needed_after_growth <= 0:
            monthly_savings = 0
        else:
            # Using future value of annuity formula
            annuity_factor = ((1 + monthly_return) ** months - 1) / monthly_return
            if annuity_factor == 0:
                print("Error: Cannot calculate monthly savings with given parameters.")
                return
            monthly_savings = remaining_needed_after_growth / annuity_factor

    # Calculate total contributions and growth
    total_contributions = monthly_savings * months
    total_growth = goal_amount - current_savings - total_contributions

    # Display results
    print(f"\n--- SAVINGS GOAL RESULTS ---")
    print(f"Savings Goal: ${goal_amount:,.2f}")
    print(f"Current Savings: ${current_savings:,.2f}")
    print(f"Amount Needed: ${amount_needed:,.2f}")
    print(f"Time Frame: {time_years:.0f} years ({months:.0f} months)")
    print(f"Expected Annual Return: {annual_return:.2f}%")
    print(f"Required Monthly Savings: ${monthly_savings:,.2f}")
    print(f"Total Contributions: ${total_contributions:,.2f}")
    print(f"Expected Growth: ${total_growth:,.2f}")

    # Provide recommendations
    if monthly_savings > 0:
        print(f"\n💡 RECOMMENDATION:")
        print(f"Save ${monthly_savings:,.2f} per month for {time_years:.0f} years to reach your goal.")

        weekly_savings = monthly_savings / 4.33  # Approximate weeks in a month
        daily_savings = monthly_savings / 30.44  # Approximate days in a month

        print(f"That's about ${weekly_savings:,.2f} per week or ${daily_savings:,.2f} per day.")
    elif monthly_savings == 0 and current_savings < goal_amount:
        print(f"\n🚀 GREAT NEWS:")
        print("Your current savings will grow to meet your goal with the expected returns!")
    elif monthly_savings == 0 and current_savings >= goal_amount:
        print("\n🎯 GOAL ACHIEVED:")
        print("You have already reached or exceeded your savings goal!")


def main() -> None:
    """
    Main program loop that displays the menu and handles user selections.

    Provides a continuous loop for users to access different calculators
    until they choose to exit. Includes error handling for invalid inputs.
    """
    print("🏦 Welcome to the Personal Finance Calculator!")
    print("This program helps you with various financial calculations.")

    while True:
        display_menu()

        try:
            choice = int(input("Enter your choice (1-6): "))

            if choice == 1:
                loan_payment_calculator()
            elif choice == 2:
                compound_interest_calculator()
            elif choice == 3:
                simple_interest_calculator()
            elif choice == 4:
                budget_tracker()
            elif choice == 5:
                savings_goal_calculator()
            elif choice == 6:
                print("💰 Thank you for using the Personal Finance Calculator!")
                print("Remember: Smart financial planning leads to financial freedom!")
                break
            else:
                print("❌ Please enter a number between 1 and 6.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

        # Ask if user wants to continue
        if choice in [1, 2, 3, 4, 5]:
            input("\n⏸️ Press Enter to continue...")


if __name__ == "__main__":
    main()