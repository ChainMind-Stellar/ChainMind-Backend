from stellar_sdk import SorobanServer, Keypair, Network
from stellar_sdk.contract import ContractClient
import os, json
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("STELLAR_RPC_URL", "https://rpc-testnet.stellar.org:443")
NETWORK_PASSPHRASE = os.getenv("STELLAR_NETWORK_PASSPHRASE", "Testnet SDF Future Network 10")
PRIV_KEY = os.getenv("PRIVATE_KEY", "")
IDENTITY_REGISTRY_ID = os.getenv("AGENT_IDENTITY_REGISTRY_ID", "")


def register_ai_agent(
    name: str, description: str, metadata_uri: str = "https://chainmind.ai"
) -> str:
    """
    Register the AI agent on Stellar Soroban using AgentIdentityRegistry.
    """
    if not PRIV_KEY or not IDENTITY_REGISTRY_ID:
        return "Error: Blockchain credentials or contract address not found in .env"

    try:
        server = SorobanServer(RPC_URL)
        keypair = Keypair.from_secret(PRIV_KEY)
        contract = ContractClient(
            contract_id=IDENTITY_REGISTRY_ID,
            soroban_server=server,
            network_passphrase=NETWORK_PASSPHRASE,
        )

        print(f"Registering agent '{name}' from account: {keypair.public_key}...")

        result = contract.invoke_contract_function(
            function_name="register_agent",
            parameters=[keypair.public_key, name, description, metadata_uri],
            source=keypair,
        )

        tx_hash = result.get("id", "unknown")
        print(f"Successfully registered! TX: {tx_hash}")
        return tx_hash

    except Exception as e:
        print(f"Registration failed: {e}")
        return f"error: {str(e)}"


if __name__ == "__main__":
    name = os.getenv("AGENT_NAME", "ChainMind")
    description = os.getenv("AGENT_DESCRIPTION", "AI Security Auditor")
    register_ai_agent(name, description)
