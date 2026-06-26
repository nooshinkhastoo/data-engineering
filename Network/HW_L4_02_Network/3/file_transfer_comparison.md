# FTP vs SFTP vs SCP

| Protocol | Security | Encryption | Port |
|---|---|---|---|
| FTP | Low | No | 21 |
| SFTP | High | Yes | 22 |
| SCP | High | Yes | 22 |

---

# Advantages and Disadvantages

## FTP

Advantages:
- Simple
- Fast

Disadvantages:
- No encryption
- Unsafe

---

## SFTP

Advantages:
- Secure
- Encrypted

Disadvantages:
- Slightly slower

---

## SCP

Advantages:
- Fast secure copy
- Easy to use

Disadvantages:
- No interactive file management

---

# Best Use Cases

FTP:
- Internal trusted network

SFTP:
- Secure enterprise transfer

SCP:
- Quick secure file copy

---

# Commands

## FTP
ftp 192.168.1.10

## SFTP
sftp user@server

## SCP
scp file.txt user@server:/home/user/
