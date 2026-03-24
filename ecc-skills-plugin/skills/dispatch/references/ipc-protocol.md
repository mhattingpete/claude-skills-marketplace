## IPC Protocol Specification

The IPC system uses sequence-numbered files in `.dispatch/tasks/<task-id>/ipc/` for bidirectional communication between the worker and dispatcher.

### Directionality

IPC is **worker-initiated only**. The worker writes questions; the dispatcher writes answers to those questions. The dispatcher must never write unsolicited files to the IPC directory — the worker will not detect or process them.

To provide additional context to a running worker, append notes to the plan file instead (see **Adding Context to a Running Worker** above).

### File naming

- `001.question` — Worker's question (plain text)
- `001.answer` — Dispatcher's answer (plain text)
- `001.done` — Acknowledgment from worker that it received the answer
- Sequence numbers are zero-padded to 3 digits: `001`, `002`, `003`, etc.

### Atomic write pattern

All writes use a two-step pattern to prevent reading partial files:
1. Write to `<filename>.tmp`
2. `mv <filename>.tmp <filename>` (atomic on POSIX filesystems)

Both the worker (writing questions) and the dispatcher (writing answers) follow this pattern.

### Sequence numbering

The next sequence number is derived from the count of existing `*.question` files in the IPC directory, plus one. The worker determines this when it needs to ask a question.

### Startup reconciliation

If the dispatcher restarts mid-conversation (e.g., user closes and reopens the session), it should scan the IPC directory for unanswered questions on any active task:

1. List all task directories under `.dispatch/tasks/`.
2. For each, check `ipc/` for `*.question` files without matching `*.answer` files.
3. If found, surface the question to the user and resume the IPC flow from step 3 onward.

This ensures questions are never silently lost.
