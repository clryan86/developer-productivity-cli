# Security Policy

DevPulse reads repository files but does not execute inspected project code. The secret scanner is intentionally high-signal and heuristic; a clean DevPulse result is not a substitute for a dedicated secrets platform. Future Git/remote integrations should treat repository URLs and credentials as untrusted inputs.
