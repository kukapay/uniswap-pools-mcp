import os
from mcp.server.fastmcp import FastMCP, Context
from typing import List, Dict
import httpx
import json
from dataclasses import dataclass
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Initialize MCP server
mcp = FastMCP("Uniswap Pools", dependencies=["httpx", "python-dotenv", "pandas"])

# Retrieve API key from .env
API_KEY = os.getenv("THEGRAPH_API_KEY")
if not API_KEY:
    raise ValueError("THEGRAPH_API_KEY not found in .env file")

BASE_URL = "https://gateway.thegraph.com/api/subgraphs/id"

# Uniswap V2 Subgraph endpoint
UNISWAP_V2_SUBGRAPH = f"{BASE_URL}/A3Np3RQbaBA6oKJgiwDJeo5T3zrYfGHPWFYayMwtNDum"

# Uniswap V3 Subgraph endpoint
UNISWAP_V3_SUBGRAPH = f"{BASE_URL}/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"

# Uniswap V4 Subgraph endpoint
UNISWAP_V4_SUBGRAPH = f"{BASE_URL}/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G"

# Define data structure for V2 pair
@dataclass
class Pair:
    id: str
    token0: str
    token1: str
    reserveUSD: str
    volumeUSD: str
    pair: str  # Format: token0.symbol/token1.symbol

# Define data structure for V3 pool
@dataclass
class Pool:
    id: str
    token0: str
    token1: str
    feeTier: int
    liquidity: str
    volumeUSD: str
    feesUSD: str
    pair: str  # Format: token0.symbol/token1.symbol

# Define data structure for V4 pool
@dataclass
class PoolV4:
    id: str
    token0: str
    token1: str
    feeTier: str
    liquidity: str
    volumeUSD: str
    feesUSD: str
    pair: str  # Format: token0.symbol/token1.symbol

# Query Subgraph to fetch V2 pairs for a given token
async def query_pairs_v2(token_address: str) -> List[Pair]:
    query = """
    query($token: ID!) {
        pairs(
            where: { 
                or: [
                    {token0: $token},
                    {token1: $token}
                ]
            }
            orderBy: volumeUSD
            orderDirection: desc
        ) {
            id
            token0 {
                id
                symbol
            }
            token1 {
                id
                symbol
            }
            reserveUSD
            volumeUSD
        }
    }
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            UNISWAP_V2_SUBGRAPH,
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "query": query,
                "variables": {"token": token_address.lower()}
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise ValueError(f"GraphQL errors: {data['errors']}")
            
        return [
            Pair(
                id=pair["id"],
                token0=pair["token0"]["id"],
                token1=pair["token1"]["id"],
                reserveUSD=pair["reserveUSD"],
                volumeUSD=pair["volumeUSD"],
                pair=f"{pair['token0']['symbol']}/{pair['token1']['symbol']}"
            )
            for pair in data["data"]["pairs"]
        ]

# Query Subgraph to fetch a specific V2 pair by ID
async def query_pair_v2_by_id(pair_id: str) -> Pair:
    query = """
    query($id: ID!) {
        pairs(where: { id: $id }) {
            id
            token0 {
                id
                symbol
            }
            token1 {
                id
                symbol
            }
            reserveUSD
            volumeUSD
        }
    }
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            UNISWAP_V2_SUBGRAPH,
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "query": query,
                "variables": {"id": pair_id.lower()}
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise ValueError(f"GraphQL errors: {data['errors']}")
        
        pairs = data["data"]["pairs"]
        if not pairs:
            raise ValueError(f"No V2 pair found with ID: {pair_id}")
            
        pair = pairs[0]
        return Pair(
            id=pair["id"],
            token0=pair["token0"]["id"],
            token1=pair["token1"]["id"],
            reserveUSD=pair["reserveUSD"],
            volumeUSD=pair["volumeUSD"],
            pair=f"{pair['token0']['symbol']}/{pair['token1']['symbol']}"
        )

# Query Subgraph to fetch V3 pools for a given token
async def query_pools_v3(token_address: str) -> List[Pool]:
    query = """
    query($token: Bytes!) {
        pools(
            where: { 
                or: [
                    {token0: $token},
                    {token1: $token}
                ]
            }
            orderBy: volumeUSD
            orderDirection: desc
        ) {
            id
            token0 {
                id
                symbol
            }
            token1 {
                id
                symbol
            }
            feeTier
            liquidity
            volumeUSD
            feesUSD
        }
    }
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            UNISWAP_V3_SUBGRAPH,
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "query": query,
                "variables": {"token": token_address.lower()}
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise ValueError(f"GraphQL errors: {data['errors']}")
            
        return [
            Pool(
                id=pool["id"],
                token0=pool["token0"]["id"],
                token1=pool["token1"]["id"],
                feeTier=pool["feeTier"],
                liquidity=pool["liquidity"],
                volumeUSD=pool["volumeUSD"],
                feesUSD=pool["feesUSD"],
                pair=f"{pool['token0']['symbol']}/{pool['token1']['symbol']}"
            )
            for pool in data["data"]["pools"]
        ]

# Query Subgraph to fetch a specific V3 pool by ID
async def query_pool_v3_by_id(pool_id: str) -> Pool:
    query = """
    query($id: ID!) {
        pools(where: { id: $id }) {
            id
            token0 {
                id
                symbol
            }
            token1 {
                id
                symbol
            }
            feeTier
            liquidity
            volumeUSD
            feesUSD
        }
    }
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            UNISWAP_V3_SUBGRAPH,
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "query": query,
                "variables": {"id": pool_id.lower()}
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise ValueError(f"GraphQL errors: {data['errors']}")
        
        pools = data["data"]["pools"]
        if not pools:
            raise ValueError(f"No V3 pool found with ID: {pool_id}")
            
        pool = pools[0]
        return Pool(
            id=pool["id"],
            token0=pool["token0"]["id"],
            token1=pool["token1"]["id"],
            feeTier=pool["feeTier"],
            liquidity=pool["liquidity"],
            volumeUSD=pool["volumeUSD"],
            feesUSD=pool["feesUSD"],
            pair=f"{pool['token0']['symbol']}/{pool['token1']['symbol']}"
        )

# Query Subgraph to fetch V4 pools for a given token
async def query_pools_v4(token_address: str) -> List[PoolV4]:
    query = """
    query($token: ID!) {
        pools(
            where: { 
                or: [
                    {token0: $token},
                    {token1: $token}
                ]
            }
            orderBy: volumeUSD
            orderDirection: desc
        ) {
            id
            token0: token0 {
                id
                symbol
            }
            token1: token1 {
                id
                symbol
            }
            feeTier
            liquidity
            volumeUSD
            feesUSD
        }
    }
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            UNISWAP_V4_SUBGRAPH,
            headers={
                'Authorization': f'Bearer {API_KEY}',
            },
            json={
                'query': query,
                'variables': {'token': token_address.lower()}
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if 'errors' in data:
            raise ValueError(f"GraphQL errors: {data['errors']}")
        
        return [
            PoolV4(
                id=pool['id'],
                token0=pool['token0']['id'],
                token1=pool['token1']['id'],
                feeTier=str(pool['feeTier']),
                liquidity=str(pool['liquidity']),
                volumeUSD=pool['volumeUSD'],
                feesUSD=pool['feesUSD'],
                pair=f"{pool['token0']['symbol']}/{pool['token1']['symbol']}"
            )
            for pool in data['data']['pools']
        ]

# Query Subgraph to fetch a specific V4 pool by ID
async def query_pool_v4_by_id(pool_id: str) -> PoolV4:
    query = """
    query($id: ID!) {
        pools(where: { id: $id }) {
            id
            token0 {
                id
                symbol
            }
            token1 {
                id
                symbol
            }
            feeTier
            liquidity
            volumeUSD
            feesUSD
        }
    }
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            UNISWAP_V4_SUBGRAPH,
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "query": query,
                "variables": {"id": pool_id.lower()}
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise ValueError(f"GraphQL errors: {data['errors']}")
        
        pools = data["data"]["pools"]
        if not pools:
            raise ValueError(f"No V4 pool found with ID: {pool_id}")
            
        pool = pools[0]
        return PoolV4(
            id=pool["id"],
            token0=pool["token0"]["id"],
            token1=pool["token1"]["id"],
            feeTier=str(pool["feeTier"]),
            liquidity=str(pool["liquidity"]),
            volumeUSD=pool["volumeUSD"],
            feesUSD=pool["feesUSD"],
            pair=f"{pool['token0']['symbol']}/{pool['token1']['symbol']}"
        )

# Tool: Query all Uniswap V2, V3, and V4 pools/pairs for a specific token and return as a formatted table
@mcp.tool()
async def get_token_pools(token_address: str, ctx: Context) -> str:
    """
    Query all Uniswap V2, V3, and V4 pools/pairs for a specific token and return as a formatted markdown table.

    Parameters:
        token_address (str): The Ethereum address of the token to query (e.g., '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48').
        ctx (Context): The API context for logging and error handling.

    Returns:
        A markdown-formatted string containing a table with columns: Version, ID, Pair, Fee Tier, Volume USD, Liquidity/ReserveUSD, Fees USD, sorted by Volume USD in descending order.
    """
    ctx.info(f"Querying V2, V3, and V4 pools/pairs for token: {token_address}")
    
    try:
        # Query V2 pairs
        v2_pairs = await query_pairs_v2(token_address)
        ctx.info(f"Found {len(v2_pairs)} V2 pairs")
        
        # Query V3 pools
        v3_pools = await query_pools_v3(token_address)
        ctx.info(f"Found {len(v3_pools)} V3 pools")
        
        # Query V4 pools
        v4_pools = await query_pools_v4(token_address)
        ctx.info(f"Found {len(v4_pools)} V4 pools")
        
        # Combine V2, V3, and V4 data into a single DataFrame
        df = pd.DataFrame([
            {
                "Version": "v2",
                "ID": pair.id,
                "Pair": pair.pair,
                "Fee Tier": "3000",  # V2 fixed 0.3% fee (3000 basis points)
                "Volume USD": pair.volumeUSD,
                "Liquidity/ReserveUSD": pair.reserveUSD,
                "Fees USD": "N/A"  # V2 schema doesn't provide feesUSD
            }
            for pair in v2_pairs
        ] + [
            {
                "Version": "v3",
                "ID": pool.id,
                "Pair": pool.pair,
                "Fee Tier": str(pool.feeTier),
                "Volume USD": pool.volumeUSD,
                "Liquidity/ReserveUSD": pool.liquidity,
                "Fees USD": pool.feesUSD
            }
            for pool in v3_pools
        ] + [
            {
                "Version": "v4",
                "ID": pool.id,
                "Pair": pool.pair,
                "Fee Tier": pool.feeTier,
                "Volume USD": pool.volumeUSD,
                "Liquidity/ReserveUSD": pool.liquidity,
                "Fees USD": pool.feesUSD
            }
            for pool in v4_pools
        ])
        
        # Sort by Volume USD (descending) and select columns
        df = df.sort_values(by="Volume USD", ascending=False)
        return df.to_markdown(index=False)
    except Exception as e:
        ctx.error(f"Failed to query V2/V3/V4 pools: {str(e)}")
        raise

# Tool: Query all Uniswap V2 pairs for a specific token and return as a formatted table
@mcp.tool()
async def get_token_pools_v2(token_address: str, ctx: Context) -> str:
    """
    Query all Uniswap V2 pairs for a specific token and return as a formatted markdown table.

    Parameters:
        token_address (str): The Ethereum address of the token to query (e.g., '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48').
        ctx (Context): The API context for logging and error handling.

    Returns:
        A markdown-formatted string containing a table with columns: Version, ID, Pair, Volume USD, ReserveUSD.
    """
    ctx.info(f"Querying V2 pairs for token: {token_address}")
    
    try:
        pairs = await query_pairs_v2(token_address)
        ctx.info(f"Found {len(pairs)} V2 pairs")
        
        # Create DataFrame directly from pairs list
        df = pd.DataFrame([
            {
                "Version": "v2",
                "ID": pair.id,
                "Pair": pair.pair,
                "Volume USD": pair.volumeUSD,
                "ReserveUSD": pair.reserveUSD
            }
            for pair in pairs
        ])
        return df.to_markdown(index=False)
    except Exception as e:
        ctx.error(f"Failed to query V2 pairs: {str(e)}")
        raise

# Tool: Query all Uniswap V3 pools for a specific token and return as a formatted table
@mcp.tool()
async def get_token_pools_v3(token_address: str, ctx: Context) -> str:
    """
    Query all Uniswap V3 pools for a specific token and return as a formatted markdown table.

    Parameters:
        token_address (str): The Ethereum address of the token to query (e.g., '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48').
        ctx (Context): The API context for logging and error handling.

    Returns:
        A markdown-formatted string containing a table with columns: Version, ID, Pair, Fee Tier, Volume USD, Liquidity.
    """
    ctx.info(f"Querying V3 pools for token: {token_address}")
    
    try:
        pools = await query_pools_v3(token_address)
        ctx.info(f"Found {len(pools)} V3 pools")
        
        # Create DataFrame directly from pools list
        df = pd.DataFrame([
            {
                "Version": "v3",
                "ID": pool.id,
                "Pair": pool.pair,
                "Fee Tier": pool.feeTier,
                "Volume USD": pool.volumeUSD,
                "Liquidity": pool.liquidity
            }
            for pool in pools
        ])
        return df.to_markdown(index=False)
    except Exception as e:
        ctx.error(f"Failed to query V3 pools: {str(e)}")
        raise

# Tool: Query all Uniswap V4 pools for a specific token and return as a formatted table
@mcp.tool()
async def get_token_pools_v4(token_address: str, ctx: Context) -> str:
    """
    Query all Uniswap V4 pools for a specific token and return as a formatted markdown table.

    Parameters:
        token_address (str): The Ethereum address of the token to query (e.g., '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48').
        ctx (Context): The API context for logging and error handling.

    Returns:
        A markdown-formatted string containing a table with columns: Version, ID, Pair, Fee Tier, Volume USD, Liquidity.
    """
    ctx.info(f"Querying V4 pools for token: {token_address}")
    
    try:
        pools = await query_pools_v4(token_address)
        ctx.info(f"Found {len(pools)} V4 pools")
        
        # Create DataFrame directly from pools list
        df = pd.DataFrame([
            {
                "Version": "v4",
                "ID": pool.id,
                "Pair": pool.pair,
                "Fee Tier": pool.feeTier,
                "Volume USD": pool.volumeUSD,
                "Liquidity": pool.liquidity
            }
            for pool in pools
        ])
        return df.to_markdown(index=False)
    except Exception as e:
        ctx.error(f"Failed to query V4 pools: {str(e)}")
        raise

# Tool: Query a specific Uniswap pool/pair by version and ID and return as markdown text
@mcp.tool()
async def get_pool_data(version: str, pool_id: str, ctx: Context) -> str:
    """
    Query a specific Uniswap pool/pair by version (v2, v3, v4) and ID and return as markdown text.

    Parameters:
        version (str): The Uniswap version to query ('v2', 'v3', or 'v4').
        pool_id (str): The Ethereum address of the pool or pair to query (e.g., '0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc').
        ctx (Context): The API context for logging and error handling.

    Returns:
        A markdown-formatted string containing details of the pool/pair, including Version, ID, Pair, Token0 Address,
        Token1 Address, Fee Tier, Volume USD, Liquidity/ReserveUSD, and Fees USD.
    """
    ctx.info(f"Querying {version} pool/pair with ID: {pool_id}")
    
    try:
        if version.lower() == "v2":
            pair = await query_pair_v2_by_id(pool_id)
            result = f"""
**Uniswap V2 Pair Details**
- **Version**: v2
- **ID**: {pair.id}
- **Pair**: {pair.pair}
- **Token0 Address**: {pair.token0}
- **Token1 Address**: {pair.token1}
- **Fee Tier**: 3000 (0.3%)
- **Volume USD**: {pair.volumeUSD}
- **Liquidity/ReserveUSD**: {pair.reserveUSD}
- **Fees USD**: N/A
"""
        elif version.lower() == "v3":
            pool = await query_pool_v3_by_id(pool_id)
            result = f"""
**Uniswap V3 Pool Details**
- **Version**: v3
- **ID**: {pool.id}
- **Pair**: {pool.pair}
- **Token0 Address**: {pool.token0}
- **Token1 Address**: {pool.token1}
- **Fee Tier**: {pool.feeTier}
- **Volume USD**: {pool.volumeUSD}
- **Liquidity/ReserveUSD**: {pool.liquidity}
- **Fees USD**: {pool.feesUSD}
"""
        elif version.lower() == "v4":
            pool = await query_pool_v4_by_id(pool_id)
            result = f"""
**Uniswap V4 Pool Details**
- **Version**: v4
- **ID**: {pool.id}
- **Pair**: {pool.pair}
- **Token0 Address**: {pool.token0}
- **Token1 Address**: {pool.token1}
- **Fee Tier**: {pool.feeTier}
- **Volume USD**: {pool.volumeUSD}
- **Liquidity/ReserveUSD**: {pool.liquidity}
- **Fees USD**: {pool.feesUSD}
"""
        else:
            raise ValueError(f"Invalid version: {version}. Must be 'v2', 'v3', or 'v4'")
        
        return result.strip()
    except Exception as e:
        ctx.error(f"Failed to query {version} pool/pair: {str(e)}")
        raise


# Main entry point
if __name__ == "__main__":
    mcp.run()
