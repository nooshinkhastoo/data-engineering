# SSL vs TLS

SSL is an old encryption protocol.
TLS is the newer and more secure version of SSL.

SSL is deprecated because it has security vulnerabilities.
TLS provides stronger encryption and better security.

---

# Self-Signed vs CA-Signed Certificates

## Self-Signed Certificate

- Signed by the owner
- Not trusted by browsers
- Used mostly for testing

## CA-Signed Certificate

- Signed by trusted Certificate Authority
- Trusted by browsers
- Used in production systems

---

# SSL/TLS Best Practices

1. Use TLS 1.2 or TLS 1.3
2. Disable old SSL versions
3. Use strong cipher suites
4. Renew certificates before expiration
5. Use certificates from trusted CA

---

# Why HTTP is Unsafe

HTTP sends data in plain text.
Attackers can read usernames, passwords, and sensitive data.

HTTPS uses encryption through TLS.
It protects data confidentiality and integrity.

