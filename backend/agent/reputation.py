from stellar_sdk import SorobanServer, Keypair, Network
from stellar_sdk.contract import ContractClient
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("STELLAR_RPC_URL", "https://rpc-testnet.stellar.org:443")
NETWORK_PASSPHRASE = os.getenv("STELLAR_NETWORK_PASSPHRASE", "Testnet SDF Future Network 10")
PRIV_KEY = os.getenv("PRIVATE_KEY", "")
REPUTATION_REGISTRY_ID = os.getenv("AGENT_REPUTATION_REGISTRY_ID", "")


def submit_audit_reputation(
    agent_id: int,
    score: int,
    contract_name: str,
    vuln_count: int,
) -> str:
    """
    Submits a reputation signal to AgentReputationRegistry on Stellar based on audit quality.
    Score 1-10 (higher is better).
    Returns tx_hash or error string.
    """
    if not PRIV_KEY or not REPUTATION_REGISTRY_ID:
        return "reputation_not_configured"

    try:
        server = SorobanServer(RPC_URL)
        keypair = Keypair.from_secret(PRIV_KEY)
        contract = ContractClient(
            contract_id=REPUTATION_REGISTRY_ID,
            soroban_server=server,
            network_passphrase=NETWORK_PASSPHRASE,
        )

        feedback = f"Audited {contract_name}: found {vuln_count} vulnerabilities"

        result = contract.invoke_contract_function(
            function_name="submit_feedback",
            parameters=[
                keypair.public_key,
                agent_id,
                min(score, 10),
                feedback,
            ],
            source=keypair,
        )

        tx_hash = result.get("id", "unknown")
        return tx_hash

    except Exception as e:
        print(f"Reputation update failed: {e}")
        return f"error: {str(e)[:100]}"
