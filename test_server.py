'''
Test script for the Pleo MCP server.

This script directly invokes the tool functions to test their functionality
without needing to run the full MCP server and client.
'''

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the tool functions from the server file
from server import list_expenses, get_expense, update_expense, get_expense_receipts, get_expense_receipt

async def main():
    '''Main function to run the tests.'''
    print("--- Running Pleo MCP Tests ---")

    # Test 1: List recent expenses
    print("\n[Test 1: Listing recent expenses...]")
    try:
        recent_expenses = await list_expenses.fn(limit=5)
        print("Result:\n", recent_expenses)
        # Extract an expense ID for further tests
        first_expense_id = None
        if "ID:" in recent_expenses:
            try:
                first_expense_id = recent_expenses.split("ID: ")[1].split("\n")[0]
                print(f"Extracted expense ID for next tests: {first_expense_id}")
            except IndexError:
                print("Could not extract an expense ID.")

    except Exception as e:
        print(f"Error during list_expenses test: {e}")
        first_expense_id = None # Ensure it's None if the test fails

    # Subsequent tests depend on having a valid expense ID
    if first_expense_id:
        # Test 2: Get details for a specific expense
        print(f"\n[Test 2: Getting details for expense {first_expense_id}...]")
        try:
            expense_details = await get_expense.fn(expense_id=first_expense_id)
            print("Result:\n", expense_details)
            # Extract a receipt ID if available
            first_receipt_id = None
            if "Receipt IDs:" in expense_details:
                try:
                    receipt_ids_str = expense_details.split("Receipt IDs: ")[1].split("\n")[0]
                    if receipt_ids_str and receipt_ids_str != "None":
                        first_receipt_id = receipt_ids_str.split(", ")[0]
                        print(f"Extracted receipt ID for next test: {first_receipt_id}")
                except (IndexError, ValueError):
                    print("Could not extract a receipt ID.")

        except Exception as e:
            print(f"Error during get_expense test: {e}")
            first_receipt_id = None

        # Test 3: Update the expense note
        print(f"\n[Test 3: Updating note for expense {first_expense_id}...]")
        try:
            update_result = await update_expense.fn(expense_id=first_expense_id, note=f"Test update from Manus AI at {asyncio.get_event_loop().time()}")
            print("Result:", update_result)
            # Verify the update
            updated_details = await get_expense.fn(expense_id=first_expense_id)
            print("Verified Update:\n", updated_details)
        except Exception as e:
            print(f"Error during update_expense test: {e}")

        # Test 4: Get receipts for the expense
        print(f"\n[Test 4: Getting receipts for expense {first_expense_id}...]")
        try:
            receipts_info = await get_expense_receipts.fn(expense_id=first_expense_id)
            print("Result:\n", receipts_info)
        except Exception as e:
            print(f"Error during get_expense_receipts test: {e}")

        # Test 5: Get a specific receipt if an ID was found
        if first_receipt_id:
            print(f"\n[Test 5: Getting specific receipt {first_receipt_id}...]")
            try:
                receipt_detail = await get_expense_receipt.fn(expense_id=first_expense_id, receipt_id=first_receipt_id)
                print("Result:\n", receipt_detail)
            except Exception as e:
                print(f"Error during get_expense_receipt test: {e}")
        else:
            print("\n[Test 5: Skipped] No receipt ID found to get a specific receipt.")

    else:
        print("\n[Tests 2-5: Skipped] No expense ID available to proceed with detailed tests.")

    print("\n--- Tests Finished ---")

if __name__ == "__main__":
    # Check for API key before running
    if not os.getenv("PLEO_API_KEY"):
        print("Error: PLEO_API_KEY environment variable is not set. Please create a .env file or export it.")
    else:
        asyncio.run(main())
