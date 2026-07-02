from stellar_sdk import SorobanServer, Keypair, Network
from stellar_sdk.contract import ContractClient
import os, json
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("STELLAR_RPC_URL", "https://rpc-testnet.stellar.org:443")
NETWORK_PASSPHRASE = os.getenv("STELLAR_NETWORK_PASSPHRASE", "Testnet SDF Future Network 10")
PRIV_KEY = os.getenv("PRIVATE_KEY", "")
IDENTITY_REGISTRY_ID = os.getenv("AGENT_IDENTITY_REGISTRY_ID", "")
AGENT_NAME = os.getenv("AGENT_NAME", "ChainMind")
AGENT_DESC = os.getenv("AGENT_DESCRIPTION", "Autonomous AI smart contract security auditor on Stellar")


def register_agent(metadata_uri: str = "") -> dict:
    """
    Register ChainMind as an on-chain agent on AgentIdentityRegistry on Stellar.
    Returns: {agent_id, tx_hash, owner_address}
    """
    if not PRIV_KEY or not IDENTITY_REGISTRY_ID:
        return {"error": "Identity registry keys not configured", "agent_id": None}

    try:
        server = SorobanServer(RPC_URL)
        keypair = Keypair.from_secret(PRIV_KEY)
        contract = ContractClient(
            contract_id=IDENTITY_REGISTRY_ID,
            soroban_server=server,
            network_passphrase=NETWORK_PASSPHRASE,
        )

        agent_metadata = {
            "name": AGENT_NAME,
            "description": AGENT_DESC,
            "type": "security-auditor",
            "capabilities": [
                "vulnerability-detection",
                "attack-simulation",
                "fix-generation",
                "natural-language-qa",
                "economic-agency-usdc",
            ],
            "ai_models": ["gemini-2.0-flash", "llama-3.3-70b", "mistral-large"],
            "chain": "stellar-testnet",
        }

        result = contract.invoke_contract_function(
            function_name="register_agent",
            parameters=[
                keypair.public_key,
                AGENT_NAME,
                AGENT_DESC,
                metadata_uri or json.dumps(agent_metadata),
            ],
            source=keypair,
        )

        agent_id = result.get("agent_id", "unknown")
        tx_hash = result.get("id", "unknown")

        return {
            "agent_id": agent_id,
            "tx_hash": tx_hash,
            "owner": keypair.public_key,
        }

    except Exception as e:
        print(f"Agent registration failed: {e}")
        return {"error": str(e), "agent_id": None}


if __name__ == "__main__":
    print("\n--- ChainMind AI Agent On-Chain Registration (Stellar Soroban) ---")
    res = register_agent()
    if "error" in res:
        print(f"Registration failed: {res['error']}")
    else:
        print(f"Success! Agent ID: {res['agent_id']}")
        print(f"Tx Hash: {res['tx_hash']}")
        print(f"Owner: {res['owner']}")
        print("----------------------------------------------------------------\n")
