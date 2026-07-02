from stellar_sdk import SorobanServer, Keypair, Network
from stellar_sdk.contract import ContractClient
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("STELLAR_RPC_URL", "https://rpc-testnet.stellar.org:443")
NETWORK_PASSPHRASE = os.getenv("STELLAR_NETWORK_PASSPHRASE", "Testnet SDF Future Network 10")
PRIV_KEY = os.getenv("PRIVATE_KEY", "")
REGISTRY_ID = os.getenv("SIMULATION_REGISTRY_ID", "")


def record_on_chain(
    contract_hash: str,
    risk_score: int,
    vuln_count: int,
    tx_count: int,
    ipfs_report: str = "",
) -> str:
    """
    Record simulation results on Stellar Soroban via SimulationRegistry.
    Returns: transaction hash or error string.
    """
    if not PRIV_KEY or not REGISTRY_ID:
        return "blockchain_not_configured"

    try:
        server = SorobanServer(RPC_URL)
        keypair = Keypair.from_secret(PRIV_KEY)
        contract = ContractClient(
            contract_id=REGISTRY_ID,
            soroban_server=server,
            network_passphrase=NETWORK_PASSPHRASE,
        )

        result = contract.invoke_contract_function(
            function_name="record_simulation",
            parameters=[
                keypair.public_key,
                contract_hash,
                min(risk_score, 100),
                min(vuln_count, 65535),
                min(tx_count, 4294967295),
                ipfs_report or "ChainMind Audit Report",
            ],
            source=keypair,
        )

        tx_hash = result.get("id", "unknown")
        return tx_hash

    except Exception as e:
        print(f"On-chain record failed: {e}")
        return f"error: {str(e)[:100]}"
