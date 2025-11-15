#!/usr/bin/env python3
"""
Pleo MCP Server

A Model Context Protocol server for interacting with the Pleo API.
Provides tools for managing expenses, receipts, and accounting data.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

import httpx
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("pleo-mcp")

# Pleo API configuration
PLEO_API_BASE_URL = "https://openapi.pleo.io/v1"
PLEO_API_KEY = os.getenv("PLEO_API_KEY")

if not PLEO_API_KEY:
    logger.warning("PLEO_API_KEY environment variable not set")


class PleoAPIClient:
    """Client for interacting with the Pleo API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = PLEO_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the Pleo API."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{endpoint}"
            response = await client.get(url, headers=self.headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    
    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a PUT request to the Pleo API."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{endpoint}"
            response = await client.put(url, headers=self.headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
    
    async def download_file(self, url: str) -> bytes:
        """Download a file from a URL."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0)
            response.raise_for_status()
            return response.content


def get_client() -> PleoAPIClient:
    """Get an instance of the Pleo API client."""
    if not PLEO_API_KEY:
        raise ValueError("PLEO_API_KEY environment variable is not set")
    return PleoAPIClient(PLEO_API_KEY)


@mcp.tool()
async def list_expenses(
    status: Optional[str] = None,
    expense_type: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    limit: int = 50
) -> str:
    """
    List all expenses for your company with optional filtering.
    
    Args:
        status: Filter by export status (NOT_EXPORTED, QUEUED, EXPORTING, EXPORTED)
        expense_type: Filter by type (CARD, PERSONAL_TRANSFER, BILL_INVOICE, LOAD, MANUAL, etc.)
        from_date: Filter expenses from this date (YYYY-MM-DD format)
        to_date: Filter expenses to this date (YYYY-MM-DD format)
        limit: Maximum number of results to return (default: 50, max: 100)
    
    Returns:
        JSON string containing the list of expenses
    """
    try:
        client = get_client()
        
        # Build query parameters
        params = {"limit": min(limit, 100)}
        
        if status:
            params["status"] = status
        if expense_type:
            params["type"] = expense_type
        if from_date:
            params["performedAtFrom"] = from_date
        if to_date:
            params["performedAtTo"] = to_date
        
        # Make API request
        result = await client.get("/expenses", params=params)
        
        # Format response
        expenses = result.get("data", [])
        
        if not expenses:
            return "No expenses found matching the criteria."
        
        # Create summary
        summary = f"Found {len(expenses)} expense(s):\n\n"
        
        for expense in expenses:
            expense_id = expense.get("id", "N/A")
            performed_at = expense.get("performedAt", "N/A")
            amount = expense.get("amountOriginal", {})
            value = amount.get("value", 0)
            currency = amount.get("currency", "N/A")
            note = expense.get("note", "No note")
            exp_type = expense.get("type", "N/A")
            exp_status = expense.get("status", "N/A")
            
            summary += f"- ID: {expense_id}\n"
            summary += f"  Date: {performed_at}\n"
            summary += f"  Amount: {value} {currency}\n"
            summary += f"  Type: {exp_type}\n"
            summary += f"  Status: {exp_status}\n"
            summary += f"  Note: {note}\n\n"
        
        return summary
        
    except Exception as e:
        logger.error(f"Error listing expenses: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def get_expense(expense_id: str) -> str:
    """
    Get detailed information about a specific expense.
    
    Args:
        expense_id: The UUID of the expense
    
    Returns:
        JSON string containing detailed expense information
    """
    try:
        client = get_client()
        expense = await client.get(f"/expenses/{expense_id}")
        
        # Format detailed response
        result = "Expense Details:\n\n"
        result += f"ID: {expense.get('id', 'N/A')}\n"
        result += f"Employee ID: {expense.get('employeeId', 'N/A')}\n"
        result += f"Employee Code: {expense.get('employeeCode', 'N/A')}\n"
        result += f"Department ID: {expense.get('departmentId', 'N/A')}\n"
        result += f"Performed At: {expense.get('performedAt', 'N/A')}\n"
        
        # Amount information
        amount_original = expense.get('amountOriginal', {})
        result += f"Original Amount: {amount_original.get('value', 0)} {amount_original.get('currency', 'N/A')}\n"
        
        amount_settled = expense.get('amountSettled', {})
        if amount_settled:
            result += f"Settled Amount: {amount_settled.get('value', 0)} {amount_settled.get('currency', 'N/A')}\n"
        
        result += f"Note: {expense.get('note', 'No note')}\n"
        result += f"Type: {expense.get('type', 'N/A')}\n"
        result += f"Status: {expense.get('status', 'N/A')}\n"
        
        # Accounting information
        result += f"Account ID: {expense.get('accountId', 'N/A')}\n"
        result += f"Tax Code ID: {expense.get('taxCodeId', 'N/A')}\n"
        
        # Receipt information
        receipt_ids = expense.get('receiptIds', [])
        result += f"Receipt IDs: {', '.join(receipt_ids) if receipt_ids else 'None'}\n"
        
        # Card transaction details
        card_transaction = expense.get('cardTransaction', {})
        if card_transaction:
            result += "\nCard Transaction:\n"
            result += f"  State: {card_transaction.get('state', 'N/A')}\n"
            result += f"  Authorized At: {card_transaction.get('authorizedAt', 'N/A')}\n"
            result += f"  Settled At: {card_transaction.get('settledAt', 'N/A')}\n"
            
            merchant = card_transaction.get('merchant', {})
            if merchant:
                result += f"  Merchant: {merchant.get('name', 'N/A')} (ID: {merchant.get('id', 'N/A')})\n"
        
        # Timestamps
        result += f"\nCreated At: {expense.get('createdAt', 'N/A')}\n"
        result += f"Updated At: {expense.get('updatedAt', 'N/A')}\n"
        
        return result
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Expense with ID {expense_id} not found"
        logger.error(f"HTTP error getting expense: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting expense: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def update_expense(
    expense_id: str,
    note: Optional[str] = None,
    account_id: Optional[str] = None,
    tax_code_id: Optional[str] = None
) -> str:
    """
    Update an expense with new information.
    
    Args:
        expense_id: The UUID of the expense to update
        note: Update the expense note/comment
        account_id: Update the accounting category UUID
        tax_code_id: Update the tax code UUID
    
    Returns:
        Success message or error
    """
    try:
        client = get_client()
        
        # Build update payload
        update_data = {}
        
        if note is not None:
            update_data["note"] = note
        if account_id is not None:
            update_data["accountId"] = account_id
        if tax_code_id is not None:
            update_data["taxCodeId"] = tax_code_id
        
        if not update_data:
            return "Error: No update fields provided. Please specify at least one field to update."
        
        # Make API request
        result = await client.put(f"/expenses/{expense_id}", update_data)
        
        return f"Successfully updated expense {expense_id}"
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Expense with ID {expense_id} not found"
        logger.error(f"HTTP error updating expense: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error updating expense: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def get_expense_receipts(expense_id: str) -> str:
    """
    Get all receipts attached to an expense.
    
    Args:
        expense_id: The UUID of the expense
    
    Returns:
        Information about all receipts attached to the expense
    """
    try:
        client = get_client()
        receipts = await client.get(f"/expenses/{expense_id}/receipts")
        
        if not receipts:
            return f"No receipts found for expense {expense_id}"
        
        result = f"Receipts for expense {expense_id}:\n\n"
        
        for receipt in receipts:
            receipt_id = receipt.get("id", "N/A")
            name = receipt.get("name", "N/A")
            mime_type = receipt.get("mimeType", "N/A")
            size = receipt.get("size", 0)
            url = receipt.get("url", "N/A")
            
            result += f"- Receipt ID: {receipt_id}\n"
            result += f"  Name: {name}\n"
            result += f"  Type: {mime_type}\n"
            result += f"  Size: {size} KB\n"
            result += f"  Download URL: {url}\n"
            result += f"  (URL valid for 15 hours)\n\n"
        
        return result
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Expense with ID {expense_id} not found"
        logger.error(f"HTTP error getting receipts: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting receipts: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def get_expense_receipt(expense_id: str, receipt_id: str) -> str:
    """
    Get information about a specific receipt attached to an expense.
    
    Args:
        expense_id: The UUID of the expense
        receipt_id: The UUID of the receipt
    
    Returns:
        Information about the specific receipt including download URL
    """
    try:
        client = get_client()
        receipt = await client.get(f"/expenses/{expense_id}/receipts/{receipt_id}")
        
        result = "Receipt Details:\n\n"
        result += f"ID: {receipt.get('id', 'N/A')}\n"
        result += f"Name: {receipt.get('name', 'N/A')}\n"
        result += f"MIME Type: {receipt.get('mimeType', 'N/A')}\n"
        result += f"Size: {receipt.get('size', 0)} KB\n"
        result += f"Download URL: {receipt.get('url', 'N/A')}\n"
        result += f"(URL valid for 15 hours)\n"
        
        return result
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Receipt with ID {receipt_id} not found for expense {expense_id}"
        logger.error(f"HTTP error getting receipt: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error getting receipt: {e}")
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
