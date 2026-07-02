## Audit Completion Webhook Reliability

The audit completion webhook (`POST /api/webhook/audit-complete`) notifies external systems when an audit pipeline finishes, so it is built to fail gracefully and never drop a notification silently.

### Payload handling

* The webhook body is untrusted input. The handler reads it with optional chaining end-to-end, so a malformed or hostile payload (for example `{ simulation_id: null }`) can never throw a `TypeError`.
* `simulation_id`, `risk_score`, and `status` are validated as non-empty values before a notification is dispatched.

### Response codes

| Situation | Status | Reason |
| --- | --- | --- |
| Valid audit completion dispatched | `200` | Acknowledge delivery |
| Valid event with nothing to process (status update, missing fields) | `200` | Acknowledge; nothing to do |
| Payload is not a recognised webhook object | `404` | Not for us |
| Dispatch failure or timeout | `500` | Signals the caller to retry so the notification is not lost |

### Dispatch safety

* The dispatch function is wrapped in `try/catch`; a failure is logged and answered with `500` instead of escaping as an unhandled exception.
* A hard timeout is applied so a stalled connection cannot hang the request indefinitely. The timer is always cleared.

### Process-level safety net

* `unhandledRejection` / `uncaughtException` handlers log the error and exit so the orchestrator can restart the process with clean state.
* FastAPI exception middleware turns any unhandled error into a clean `500` response.

### Tests

Reliability behaviour is covered in the backend test suite (malformed payloads, dispatch failure, and dispatch timeout).
