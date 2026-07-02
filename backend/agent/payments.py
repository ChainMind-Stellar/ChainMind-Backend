from stellar_sdk import SorobanServer, Keypair, Network
from stellar_sdk.contract import ContractClient
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("STELLAR_RPC_URL", "https://rpc-testnet.stellar.org:443")
NETWORK_PASSPHRASE = os.getenv("STELLAR_NETWORK_PASSPHRASE", "Testnet SDF Future Network 10")
PAYMENT_GATEWAY_ID = os.getenv("PAYMENT_GATEWAY_ID", "")


def verify_payment_on_chain(payment_id: int) -> dict:
    """
    Verify that a developer has paid the USDC audit fee on Stellar.
    Returns: {paid: bool, payer: str, contract_hash: str}
    """
    if not PAYMENT_GATEWAY_ID:
        return {"paid": True, "payer": "free_mode", "contract_hash": ""}

    try:
        server = SorobanServer(RPC_URL)
        keypair = Keypair.from_secret(os.getenv("PRIVATE_KEY", ""))
        contract = ContractClient(
            contract_id=PAYMENT_GATEWAY_ID,
            soroban_server=server,
            network_passphrase=NETWORK_PASSPHRASE,
        )

        result = contract.invoke_contract_function(
            function_name="verify_payment",
            parameters=[payment_id],
            source=keypair,
        )

        # Result is (bool, Address, Bytes) from the contract
        paid = result.get("paid", False)
        payer = result.get("payer", "")
        contract_hash = result.get("contract_hash", "")

        return {
            "paid": paid,
            "payer": payer,
            "contract_hash": contract_hash,
        }
    except Exception as e:
        print(f"Payment verification failed: {e}")
        return {"paid": False, "payer": "", "contract_hash": "", "error": str(e)}


def get_agent_earnings() -> dict:
    """
    Get the agent's current USDC balance and fee info from the PaymentGateway.
    """
    if not PAYMENT_GATEWAY_ID:
        return {"balance_usdc": 0, "fee_usdc": 0}

    try:
        server = SorobanServer(RPC_URL)
        keypair = Keypair.from_secret(os.getenv("PRIVATE_KEY", ""))
        contract = ContractClient(
            contract_id=PAYMENT_GATEWAY_ID,
            soroban_server=server,
            network_passphrase=NETWORK_PASSPHRASE,
        )

        balance = contract.invoke_contract_function(
            function_name="get_balance",
            parameters=[],
            source=keypair,
        )
        fee = contract.invoke_contract_function(
            function_name="get_fee",
            parameters=[],
            source=keypair,
        )

        return {
            "balance_usdc": balance / 1e7,
            "fee_usdc": fee / 1e7,
        }
    except Exception as e:
        return {"error": str(e)}
