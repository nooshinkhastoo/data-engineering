# Local Port Forwarding

Forward local port to remote server.

Example:
ssh -L 8080:localhost:80 user@server

Use Case: Access remote internal website locally.

Remote Port Forwarding
Expose local service to remote server.
Example:

ssh -R 9090:localhost:3000 user@server

Use Case: Expose local development server.

Dynamic Port Forwarding (SOCKS Proxy)
Creates SOCKS proxy.
Example:

ssh -D 1080 user@server

Use Case: Secure internet browsing through SSH tunnel.

