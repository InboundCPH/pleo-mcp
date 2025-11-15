# Pleo MCP Server

A Model Context Protocol (MCP) server for interacting with the Pleo API. This server enables automated management of expenses, receipts, and accounting data through the Pleo platform.

## Features

- **List Expenses**: Retrieve all expenses for your company with filtering options
- **Get Expense Details**: Fetch detailed information about specific expenses
- **Update Expenses**: Modify expense details including accounting information and tags
- **Manage Receipts**: Retrieve and download receipts attached to expenses
- **Filter by Status**: Query expenses by export status, date range, and more

## Prerequisites

- Python 3.11 or higher
- A Pleo account with API access
- Pleo API key (Bearer token)

## Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/InboundCPH/pleo-mcp.git
cd pleo-mcp

# Install dependencies
pip install -r requirements.txt

# Set your Pleo API key
export PLEO_API_KEY="your_api_key_here"

# Run the server
python server.py
```

### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/pleo-mcp)

1. Click the "Deploy on Railway" button above
2. Set the `PLEO_API_KEY` environment variable in Railway
3. Deploy and get your server URL

## Configuration

The server requires the following environment variable:

- `PLEO_API_KEY`: Your Pleo API key (Bearer token)

## Usage

Once deployed, you can connect to this MCP server from any MCP-compatible client. The server provides the following tools:

### `list_expenses`

List all expenses for your company with optional filtering.

**Parameters:**
- `status` (optional): Filter by export status (NOT_EXPORTED, QUEUED, EXPORTING, EXPORTED)
- `type` (optional): Filter by expense type (CARD, PERSONAL_TRANSFER, BILL_INVOICE, etc.)
- `from_date` (optional): Filter expenses from this date (YYYY-MM-DD)
- `to_date` (optional): Filter expenses to this date (YYYY-MM-DD)
- `limit` (optional): Maximum number of results (default: 50)

### `get_expense`

Get detailed information about a specific expense.

**Parameters:**
- `expense_id` (required): The UUID of the expense

### `update_expense`

Update an expense with new information.

**Parameters:**
- `expense_id` (required): The UUID of the expense
- `note` (optional): Update the expense note
- `account_id` (optional): Update the accounting category
- `tax_code_id` (optional): Update the tax code

### `get_expense_receipts`

Get all receipts attached to an expense.

**Parameters:**
- `expense_id` (required): The UUID of the expense

### `download_receipt`

Download a specific receipt file.

**Parameters:**
- `expense_id` (required): The UUID of the expense
- `receipt_id` (required): The UUID of the receipt

## API Documentation

For more information about the Pleo API, visit the [official documentation](https://developers.pleo.io/).

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
