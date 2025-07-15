import unittest
from unittest.mock import patch, MagicMock
import math
from personalfinancecalculator import (
    get_positive_number,
    get_number,
    loan_payment_calculator,
    compound_interest_calculator,
    simple_interest_calculator,
    budget_tracker,
    savings_goal_calculator
)


class TestPersonalFinanceCalculator(unittest.TestCase):
    def test_get_positive_number(self):
        """Test get_positive_number function with valid and invalid inputs."""
        with patch('builtins.input', side_effect=['10', '-5', 'abc', '20']) as mocked_input:
            # First call should return 10.0 after one valid input
            result1 = get_positive_number("Enter number: ")
            self.assertEqual(result1, 10.0)

            # Second call should return 20.0 after skipping invalid inputs
            result2 = get_positive_number("Enter number: ")
            self.assertEqual(result2, 20.0)

            # Verify all inputs were consumed
            self.assertEqual(mocked_input.call_count, 4, "Expected 4 input calls for valid and invalid inputs")

    def test_get_number(self):
        """Test get_number function with valid and invalid inputs."""
        with patch('builtins.input', side_effect=['10.5', 'abc', '-5']) as mocked_input:
            # First call should return 10.5 after one valid input
            result1 = get_number("Enter number: ")
            self.assertEqual(result1, 10.5)

            # Second call should return -5.0 after skipping invalid input
            result2 = get_number("Enter number: ")
            self.assertEqual(result2, -5.0)

            # Verify all inputs were consumed
            self.assertEqual(mocked_input.call_count, 3, "Expected 3 input calls for valid and invalid inputs")

    def test_loan_payment_calculator(self):
        """Test loan payment calculator for interest and zero-interest cases."""
        # Test with interest
        with patch('personalfinancecalculator.get_positive_number', side_effect=[10000, 5, 2]) as mocked_input:
            with patch('builtins.print') as mocked_print:
                loan_payment_calculator()
                monthly_rate = 0.05 / 12
                num_payments = 2 * 12
                # Ensure float division for accurate calculation
                denominator = ((1 + monthly_rate) ** num_payments - 1)
                monthly_payment = 10000 * (monthly_rate * (1 + monthly_rate) ** num_payments) / denominator
                total_payment = monthly_payment * num_payments
                total_interest = total_payment - 10000

                # Check if the key results are printed
                mocked_print.assert_any_call(f"Monthly Payment: ${monthly_payment:,.2f}")
                mocked_print.assert_any_call(f"Total Interest: ${total_interest:,.2f}")
                mocked_print.assert_any_call(f"Total Payment: ${total_payment:,.2f}")
                self.assertEqual(mocked_input.call_count, 3, f"Expected 3 input calls, got {mocked_input.call_count}")

        # Test zero interest
        with patch('personalfinancecalculator.get_positive_number', side_effect=[10000, 0, 2]) as mocked_input:
            with patch('builtins.print') as mocked_print:
                loan_payment_calculator()
                monthly_payment = 10000 / 24
                total_payment = monthly_payment * 24
                total_interest = 0

                mocked_print.assert_any_call(f"Monthly Payment: ${monthly_payment:,.2f}")
                mocked_print.assert_any_call(f"Total Interest: ${total_interest:,.2f}")
                mocked_print.assert_any_call(f"Total Payment: ${total_payment:,.2f}")
                self.assertEqual(mocked_input.call_count, 3, f"Expected 3 input calls, got {mocked_input.call_count}")

    def test_compound_interest_calculator(self):
        """Test compound interest calculator with monthly compounding."""
        # Mock both get_positive_number and the menu choice input
        with patch('personalfinancecalculator.get_positive_number', side_effect=[1000, 5, 2]) as mocked_get_positive:
            with patch('builtins.input', return_value='4') as mocked_input:  # Monthly compounding
                with patch('builtins.print') as mocked_print:
                    compound_interest_calculator()
                    final_amount = 1000 * (1 + 0.05 / 12) ** (12 * 2)
                    interest_earned = final_amount - 1000

                    mocked_print.assert_any_call(f"Final Amount: ${final_amount:,.2f}")
                    mocked_print.assert_any_call(f"Interest Earned: ${interest_earned:,.2f}")
                    self.assertEqual(mocked_get_positive.call_count, 3,
                                     f"Expected 3 get_positive_number calls, got {mocked_get_positive.call_count}")

    def test_simple_interest_calculator(self):
        """Test simple interest calculator."""
        with patch('personalfinancecalculator.get_positive_number', side_effect=[1000, 5, 2]) as mocked_input:
            with patch('builtins.print') as mocked_print:
                simple_interest_calculator()
                interest = 1000 * 0.05 * 2
                final_amount = 1000 + interest

                mocked_print.assert_any_call(f"Simple Interest: ${interest:,.2f}")
                mocked_print.assert_any_call(f"Final Amount: ${final_amount:,.2f}")
                self.assertEqual(mocked_input.call_count, 3, f"Expected 3 input calls, got {mocked_input.call_count}")

    def test_budget_tracker(self):
        """Test budget tracker with income and expenses."""
        # Income: Salary=2000, Expense: Rent=1000
        input_names_sequence = [
            'Salary', 'done',  # Income source and 'done' signal
            'Rent', 'done'    # Expense category and 'done' signal
        ]
        amounts_sequence = [2000, 1000] # Amounts corresponding to Salary and Rent

        with patch('builtins.input', side_effect=input_names_sequence) as mocked_input:
            with patch('personalfinancecalculator.get_positive_number',
                       side_effect=amounts_sequence) as mocked_get_positive:
                with patch('builtins.print') as mocked_print:
                    budget_tracker()
                    total_income = 2000
                    total_expenses = 1000
                    net_income = total_income - total_expenses
                    savings_rate = (net_income / total_income) * 100

                    mocked_print.assert_any_call(f"Net Income: ${net_income:,.2f}")
                    mocked_print.assert_any_call(f"Savings Rate: {savings_rate:,.2f}%")

                    # Verify correct number of calls
                    # For input: 'Salary', 'done', 'Rent', 'done' = 4 calls
                    self.assertEqual(mocked_input.call_count, 4)
                    # For get_positive_number: Salary amount, Rent amount = 2 calls
                    self.assertEqual(mocked_get_positive.call_count, 2)


    def test_savings_goal_calculator_no_growth(self):
        """Test savings goal calculator with no growth."""
        with patch('personalfinancecalculator.get_positive_number', side_effect=[10000, 2]) as mocked_get_positive:
            with patch('personalfinancecalculator.get_number', side_effect=[0, 0]) as mocked_get_number: # Current savings 0, Annual return 0
                with patch('builtins.print') as mocked_print:
                    savings_goal_calculator()
                    monthly_savings = 10000 / 24
                    total_contributions = monthly_savings * 24

                    mocked_print.assert_any_call(f"Required Monthly Savings: ${monthly_savings:,.2f}")
                    mocked_print.assert_any_call(f"Total Contributions: ${total_contributions:,.2f}")
                    self.assertEqual(mocked_get_positive.call_count, 2,
                                     f"Expected 2 get_positive_number calls, got {mocked_get_positive.call_count}")
                    self.assertEqual(mocked_get_number.call_count, 2,
                                     f"Expected 2 get_number calls, got {mocked_get_number.call_count}")

    def test_savings_goal_calculator_with_growth(self):
        """Test savings goal calculator with growth rate."""
        with patch('personalfinancecalculator.get_positive_number', side_effect=[10000, 2]) as mocked_get_positive:
            with patch('personalfinancecalculator.get_number', side_effect=[1000, 5]) as mocked_get_number: # Current savings 1000, Annual return 5%
                with patch('builtins.print') as mocked_print:
                    savings_goal_calculator()
                    # This test primarily ensures the function runs without error with these inputs.
                    # Detailed assertion for calculated values can be added if needed,
                    # but for now, checking call counts confirms input processing.
                    self.assertEqual(mocked_get_positive.call_count, 2,
                                     f"Expected 2 get_positive_number calls, got {mocked_get_positive.call_count}")
                    self.assertEqual(mocked_get_number.call_count, 2,
                                     f"Expected 2 get_number calls, got {mocked_get_number.call_count}")

    def test_savings_goal_already_met(self):
        """Test savings goal calculator when goal is already met."""
        # Goal: 5000, Current Savings: 10000 (already met)
        with patch('personalfinancecalculator.get_positive_number', side_effect=[5000, 2]) as mocked_get_positive:
            with patch('personalfinancecalculator.get_number', side_effect=[10000, 5]) as mocked_get_number:
                with patch('builtins.print') as mocked_print:
                    savings_goal_calculator()
                    # Assert that the exact congratulatory message (including the leading newline) is printed.
                    mocked_print.assert_any_call("\n🎉 Congratulations! You've already reached your goal!")

    def test_budget_tracker_multiple_items(self):
        """Test budget tracker with multiple income and expense items."""
        input_names_sequence = [
            'Salary', 'Freelance', 'done',  # Income sources and 'done'
            'Rent', 'Food', 'Transport', 'done'  # Expense categories and 'done'
        ]
        # Amounts for: Salary, Freelance, Rent, Food, Transport
        amounts_sequence = [3000, 500, 1200, 400, 200]

        with patch('builtins.input', side_effect=input_names_sequence) as mocked_input:
            with patch('personalfinancecalculator.get_positive_number',
                       side_effect=amounts_sequence) as mocked_get_positive:
                with patch('builtins.print') as mocked_print:
                    budget_tracker()
                    total_income = 3000 + 500  # 3500
                    total_expenses = 1200 + 400 + 200  # 1800
                    net_income = total_income - total_expenses  # 1700
                    savings_rate = (net_income / total_income) * 100  # 48.57%

                    mocked_print.assert_any_call(f"Net Income: ${net_income:,.2f}")
                    mocked_print.assert_any_call(f"Savings Rate: {savings_rate:,.2f}%")

                    # Verify call counts:
                    # input: 'Salary', 'Freelance', 'done', 'Rent', 'Food', 'Transport', 'done' = 7 calls
                    self.assertEqual(mocked_input.call_count, 7)
                    # get_positive_number: 2 income amounts + 3 expense amounts = 5 calls
                    self.assertEqual(mocked_get_positive.call_count, 5)

    def test_compound_interest_calculator_different_frequencies(self):
        """Test compound interest calculator with different compounding frequencies."""
        # Test annually (choice 1)
        with patch('personalfinancecalculator.get_positive_number', side_effect=[1000, 5, 2]) as mocked_get_positive:
            with patch('builtins.input', return_value='1') as mocked_input:  # Annual compounding choice
                with patch('builtins.print') as mocked_print:
                    compound_interest_calculator()
                    final_amount = 1000 * (1 + 0.05 / 1) ** (1 * 2)
                    interest_earned = final_amount - 1000

                    mocked_print.assert_any_call(f"Final Amount: ${final_amount:,.2f}")
                    mocked_print.assert_any_call(f"Interest Earned: ${interest_earned:,.2f}")

        # Test daily (choice 5)
        with patch('personalfinancecalculator.get_positive_number', side_effect=[1000, 5, 2]) as mocked_get_positive:
            with patch('builtins.input', return_value='5') as mocked_input:  # Daily compounding choice
                with patch('builtins.print') as mocked_print:
                    compound_interest_calculator()
                    final_amount = 1000 * (1 + 0.05 / 365) ** (365 * 2)
                    interest_earned = final_amount - 1000

                    mocked_print.assert_any_call(f"Final Amount: ${final_amount:,.2f}")
                    mocked_print.assert_any_call(f"Interest Earned: ${interest_earned:,.2f}")


if __name__ == '__main__':
    unittest.main()