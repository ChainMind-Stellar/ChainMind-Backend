# Contributing to ChainMind

Thank you for your interest in contributing to ChainMind — the autonomous AI smart contract security auditor on Stellar.

## Getting Started

### Prerequisites

- Python 3.10+
- Foundry (forge)
- Stellar Testnet account
- API keys: Gemini, Groq, Mistral

### Setup

```bash
git clone https://github.com/your-org/ChainMind-Backend.git
cd ChainMind-Backend/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your API keys and Stellar credentials
```

### Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## How to Contribute

### Reporting Issues

- Search existing issues before opening a new one.
- Use the issue templates (Bug Report / Feature Request).
- Include steps to reproduce, expected behavior, and actual behavior.
- Attach relevant logs or error messages.

### Submitting Changes

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Make your changes following the code style (see below).
4. Test your changes: `python -m compileall backend/`.
5. Commit with a clear message: `feat: add rate limiting middleware`.
6. Push and open a Pull Request.

### Pull Request Guidelines

- Link the issue your PR addresses.
- Keep PRs focused — one feature/fix per PR.
- Update `requirements.txt` if you add dependencies.
- Update relevant TODO files if you complete an issue item.
- Ensure no secrets or API keys are committed.

## Code Style

- Follow PEP 8.
- Use meaningful variable and function names.
- Use `print()` for debug logging (migration to `logging` module is a planned improvement).
- Include a `if __name__ == "__main__":` block for standalone testing.
- Keep functions focused and under 100 lines where possible.

## Project Structure

```
backend/
├── main.py                 # FastAPI entry point & routes
├── agent/                  # On-chain agent operations
│   ├── identity.py         # Agent identity registration
│   ├── payments.py         # USDC payment verification
│   ├── reputation.py       # Reputation score submission
│   └── selfclaw.py         # ZK-proof verification
├── ai/                     # AI model integrations
│   ├── gemini_agent.py     # Gemini 2.0 Flash (primary)
│   ├── groq_agent.py       # Groq Llama (fallback + tx gen)
│   └── mistral_agent.py    # Mistral Large (NL Q&A)
├── blockchain/             # Stellar Soroban integration
│   ├── registry.py         # On-chain audit recording
│   └── register_agent.py   # Agent registration script
├── parser/                 # Solidity contract parser
│   └── contract_parser.py  # Regex-based Solidity parser
├── simulation/             # Simulation engine
│   ├── engine.py           # Foundry forge test runner
│   └── attack_gen.py       # Attack scenario generation
├── Docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── .env.example            # Environment template
```

## Review Process

Maintainers will review your PR within 3–5 business days. Feedback may request changes. Once approved, a maintainer will merge it.

## Community

- Be respectful and inclusive.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Help others by reviewing PRs and answering issues.

Need help? Open a discussion or tag a maintainer in your issue.
