# Uniswap Pools MCP

An MCP server for querying Uniswap pools/pairs by token address, delivering clean, structured results for easy integration and analysis.

<a href="https://glama.ai/mcp/servers/@kukapay/uniswap-pools-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@kukapay/uniswap-pools-mcp/badge" alt="uniswap-pools-mcp MCP server" />
</a>

![GitHub License](https://img.shields.io/github/license/kukapay/uniswap-pools-mcp) 
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Query Uniswap Pools/Pairs**:
  - Fetch V2, V3, and V4 pools/pairs for a given token address.
  - Retrieve specific pool/pair details by version (`v2`, `v3`, `v4`) and ID.
- **Formatted Output**:
  - Returns data in markdown tables for combined pool queries.
  - Provides markdown text summaries for specific pool/pair queries, including token addresses.

## Installation

### Prerequisites

- **Python**: Version 3.10 or higher.
- **uv**: A Python package manager (recommended for dependency management).
- **The Graph API Key**: Required for querying Subgraphs. Obtain one from [The Graph](https://thegraph.com).

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/uniswap-pools-mcp.git
   cd uniswap-pools-mcp
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```

3. **Installing to Claude Desktop**:

    Install the server as a Claude Desktop application:
    ```bash
    uv run mcp install main.py --name "Uniswap Pools"
    ```

    Configuration file as a reference:

    ```json
    {
       "mcpServers": {
           "Uniswap Pools": {
               "command": "uv",
               "args": [ "--directory", "/path/to/uniswap-pools-mcp", "run", "main.py" ],
               "env": { "THEGRAPH_API_KEY": "thegraph-api-key"}               
           }
       }
    }
    ```
    Replace `/path/to/uniswap-pools-mcp` with your actual installation path, and `thegraph-api-key` with your API key from The Graph.
        
## Usage

The server provides several tools to query Uniswap pool/pair data. 

### Tools

1. **Get All Pools/Pairs for a Token**:
   ```python
   def get_token_pools(token_address: str) -> str:
   ```
   - **Description**: Queries all Uniswap V2, V3, and V4 pools/pairs for a given token address.
   - **Parameters**:
     - `token_address` (str): Ethereum address of the token (e.g., `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` for USDC).
   - **Output**: Markdown table with columns: Version, ID, Pair, Fee Tier, Volume USD, Liquidity/ReserveUSD, Fees USD.
   - **Example**:
   
     Prompt:
     ```
     Get Uniswap pools for token at address 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
     ```
     Output:
     ```
     | Version | ID                                         | Pair      | Fee Tier | Volume USD | Liquidity/ReserveUSD | Fees USD |
     |---------|--------------------------------------------|-----------|----------|------------|---------------------|----------|
     | v2      | 0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc | USDC/WETH | 3000     | 2000000.0  | 500000.0            | N/A      |
     | v3      | 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 | USDC/WETH | 500      | 1000000.0  | 123456789           | 5000.0   |
     | v4      | 0x1234567890abcdef1234567890abcdef12345678 | USDC/WETH | 1000     | 500000.0   | 987654321           | 2500.0   |
     ```


2. **Get Specific Pool/Pair by Version and ID**:
   ```python
   def get_pool_data(version: str, pool_id: str) -> str:
   ```
   - **Description**: Queries a specific Uniswap pool/pair by version (`v2`, `v3`, or `v4`) and ID.
   - **Parameters**:
     - `version` (str): Uniswap version (`v2`, `v3`, or `v4`).
     - `pool_id` (str): Ethereum address of the pool or pair (e.g., `0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc`).
   - **Output**: Markdown text with details: Version, ID, Pair, Token0 Address, Token1 Address, Fee Tier, Volume USD, Liquidity/ReserveUSD, Fees USD.
   - **Example**:

     Prompt:
     ```
     Get Uniswap V2 pool data by ID 0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc
     ```
     Output:
     ```
     **Uniswap V2 Pair Details**
     - **Version**: v2
     - **ID**: 0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc
     - **Pair**: USDC/WETH
     - **Token0 Address**: 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
     - **Token1 Address**: 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
     - **Fee Tier**: 3000 (0.3%)
     - **Volume USD**: 2000000.0
     - **Liquidity/ReserveUSD**: 500000.0
     - **Fees USD**: N/A
     ```


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.