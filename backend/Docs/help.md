## Wallet Security Notes

* Production systems must disable core dumps before handling Stellar secret keys.
* Use `ulimit -c 0` or the platform equivalent to prevent crash dumps from capturing key material.
* Avoid logging `secret` or `private_key` values, even in debug builds.
* Store Stellar private keys in environment variables or a secrets manager — never in code or config files committed to version control.
* Rotate API keys (Gemini, Groq, Mistral, Stellar) regularly and restrict their scope.
