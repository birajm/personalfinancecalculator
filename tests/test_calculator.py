import unittest
import math
from personalfinancecalculator import (
    get_positive_number,
    loan_payment_calculator,
    compound_interest_calculator,
    simple_interest_calculator,
    budget_tracker,
    savings_goal_calculator
)

class TestPersonalFinanceCalculator(unittest.TestCase):
    def test_get_positive_number(self):
        # Mock input to simulate user entering valid and invalid numbers
        with unittest.mock.patch('builtins.input', side_effect=['10', '-5', 'abc', '20']):
            self.assertEqual(get_positive_number("Enter number: "), 10.0)
            self.assertEqual(get_positive_number("Enter number: "), 20.0)

    def test_loan_payment_calculator(self):
        # Test loan payment with interest
        with unittest.mock.patch('builtins.input', side_effect=['10000', '5', '2']):
            with unittest.mock.patch('builtins.print') as mocked_print:
                loan_payment_calculator()
                monthly_payment = 10000 * (0.05/12 * (1 + 0.05/12)**(2*12)) / ((1 + 0.05/12)**(2*12) - 1)
                total_payment = monthly_payment * 24
                total_interest = total_payment - 10000
                mocked_print.assert_any_call(f"Monthly Payment: ${monthly_payment:,.2f}")
                mocked_print.assert_any_call(f"Total Interest: ${total_interest:,.2f}")
                mocked_print.assert_any_call(f"Total Payment: ${total_payment:,.2f}")

        # Test zero interest loan
        with unittest.mock.patch('builtins.input', side_effect=['10000', '0', '2']):
            with unittest.mock.patch('builtins.print') as mocked_print:
                loan_payment_calculator()
                monthly_payment = 10000 / 24
                total_payment = monthly_payment * 24
                total_interest = 0
                mocked_print.assert_any_call(f"Monthly Payment: ${monthly_payment:,.2f}")
                mocked_print.assert_any_call(f"Total Interest: ${total_interest:,.2f}")
                mocked_print.assert_any_call(f"Total Payment: ${total_payment:,.2f}")

    def test_compound_interest_calculator(self):
        # Test monthly compounding
        with unittest.mock.patch('builtins.input', side_effect=['1000', '5', '2', '4']):
            with unittest.mock.patch('builtins.print') as mocked_print:
                compound_interest_calculator()
                final_amount = 1000 * (1 + 0.05/12)**(12*2)
                interest_earned = final_amount - 1000
                mocked_print.assert_any_call(f"Final Amount: ${final_amount:,.2f}")
                mocked_print.assert_any_call(f"Interest Earned: ${interest_earned:,.2f}")

    def test_simple_interest_calculator(self):
        # Test simple interest
        with unittest.mock.patch('builtins.input', side_effect=['1000', '5', '2']):
            with unittest.mock.patch('builtins.print') as mocked_print:
                simple_interest_calculator()
                interest = 1000 * 0.05 * 2
                final_amount = 1000 + interest
                mocked_print.assert_any_call(f"Simple Interest: ${interest:,.2f}")
                mocked_print.assert_any_call(f"Final Amount: ${final_amount:,.2f}")

    def test_budget_tracker(self):
        # Test budget with income and expenses
        with unittest.mock.patch('builtins.input', side_effect=['Salary', '2000', 'done', 'Rent', '1000', 'done']):
            with unittest.mock.patch('builtins.print') as mocked_print:
                budget_tracker()
                net_income = 2000 - 1000
                savings_rate = (net_income / 2000) * 100
                mocked_print.assert_any_call(f"Net Income: ${net_income:,.2f}")
                mocked_print.assert_any_call(f"Savings Rate: {savings_rate:.2f}%")

    def test_savings_goal_calculator(self):
        # Test savings goal with no growth
        with unittest.mock.patch('builtins.input', side_effect=['10000', '0', '2', '0']):
            with unittest.mock.patch('builtins.print') as mocked_print:
                savings_goal_calculator()
                monthly_savings = 10000 / 24
                total_contributions = monthly_savings * 24
                mocked_print.assert_any_call(f"Required Monthly Savings: ${monthly_savings:,.2f}")
                mocked_print.assert_any_call(f"Total Contributions: ${total_contributions:,.2f}")

if __name__ == '__main__':
    unittest.main()