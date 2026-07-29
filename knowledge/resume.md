# Peter Wesley — Secure Fullstack Engineer

## Contact
- **Location:** Nairobi, Kenya
- **Email:** peterwesley484@gmail.com
- **GitHub:** github.com/Wesley534
- **LinkedIn:** linkedin.com/in/peter-wesley-22b744268
- **WhatsApp:** +254114578444

## Summary
Nairobi-based secure fullstack engineer who builds fullstack applications, blockchain infrastructure, and production systems with security designed in from the start. Cybersecurity background (CEH methodology, VAPT, digital forensics) shapes every architecture decision — whether building React SPAs, FastAPI backends, or Soroban smart contracts. Experienced in deploying and securing production infrastructure with Nginx, Docker, Tailscale, and Linux administration.

## Education
**Bachelor of Science in Computer Security and Forensics**
Meru University of Science and Technology — 2020 to Present

## Core Capabilities
- **Fullstack Engineering:** React.js, TypeScript, Vite, Tailwind CSS, Material UI, TanStack Query, Axios, Framer Motion, Responsive Web Design — combined with FastAPI, Laravel, and Express backends for end-to-end application delivery
- **Backend Engineering:** FastAPI, Laravel, Express — secure data handling, database migrations, role-based access, production deployment with PostgreSQL, MySQL, Prisma, SQLAlchemy, Alembic
- **Security Engineering:** JWT authentication, OTP verification, threat modeling, VAPT assessments, security-first architecture, OWASP guidelines, Nmap, Burp Suite
- **Blockchain Infrastructure:** Soroban smart contracts, Stellar ecosystem tooling, Rust-based contract deployment, SEP-41 token standard, sponsored transactions, WebAuthn/passkey authentication

## Case Studies & Engineering Experience

### Infrastructure
- **Laravel ERP Behind Nginx:** Deployed a Laravel 7 ERP on Ubuntu VPS with Nginx reverse proxy, PHP 7.4-FPM via Unix socket, 50 MB upload limit for KYC documents, Tailscale Funnel for automated HTTPS at the edge — no Certbot, no open ports
- **HTTPS with Tailscale Funnel:** Replaced traditional Let's Encrypt/Certbot with Tailscale Funnel for zero-touch TLS certificate management. Self-signed cert for LAN access, Tailscale handles public ingress.
- **Dockerized EDMS Reverse Proxy:** Built a sophisticated Nginx proxy with 4 location blocks (React SPA, Django static assets, REST API, Django sub-path with SCRIPT_NAME) for a Mayan EDMS deployment with 200 MB upload limit and Traefik integration planned
- **Tailscale Mesh VPN:** Deployed a WireGuard-based tailnet connecting 18+ devices across production, staging, and development environments with automated encryption and Funnel for public HTTPS ingress
- **Office Scanner + EDMS Integration:** Connected physical AirScan/eSCL office scanners to a Dockerized Mayan EDMS through SANE integration layer, with sophisticated Nginx routing and 200 MB upload capacity

### Blockchain
- **DisburseFlow — Soroban Smart Wallet Deployment:** Forked the Stellar Disbursement Platform and added Soroban smart contracts for embedded wallets with WebAuthn passkey authentication. Sponsored accounts eliminate XLM reserve requirements for recipients. Gas bundling combines wallet creation + first disbursement into single transactions. The blockchain layer is completely invisible — wallet creation is masked behind token-based invitations, and the admin interface shows fiat amounts (USD/EUR) via Circle's payment API.

## Selected Projects

### Backend Engineering
- **Financial Companion** — Full-stack personal finance app with FastAPI backend, React frontend (TypeScript, Vite), Alembic-managed migrations, SQLAlchemy ORM, AI-powered transaction categorization. Separates API logic from business rules for testability.
- **AiCointrack** — Cross-platform crypto tracker with Flutter mobile frontend, FastAPI backend, Firebase authentication, JWT access tokens, MySQL with Alembic migrations, HuggingFace AI analytics.
- **Secure Learning Management System** — Co-developed grades/learning platform with JWT + OTP multi-factor authentication, role-based authorization (admin, teacher, student), secure REST APIs with input validation. FastAPI + React stack.
- **KYC Identity Verification Microservice** — FastAPI microservice for facial recognition and liveness detection. API-key authenticated, integrates with Laravel orchestrator, zero persistent storage of biometric data.

### Blockchain Infrastructure
- **Invoice Financing Marketplace** — Full-stack Soroban platform where suppliers unlock working capital against verified invoices. Smart contracts handle liquidity pools, financing agreements, automated settlement on Stellar.
- **Harbor Auctions** — No-loss escrow auction marketplace where only the highest bid stays locked. Single-contract architecture with yield simulation, on-chain delivery confirmation, and dispute resolution.
- **SEP-41 Token Contract** — Soroban implementation of Stellar SEP-41 token standard with balance management, approvals, delegated transfers, minting, burning.
- **School Management Contract** — Soroban smart contract for on-chain student registration, payments, and administrative operations.
- **Stellar Donation Platform** — React-based donation platform with Stellar blockchain integration for transparent, tamper-proof donation tracking.

### Security Engineering
- **Network Security Simulation** — Configured Linux-based server environments with Wireshark for packet analysis and iptables for firewall rule implementation against simulated threats.
- **Authentication & Authorization Systems** — Designed reusable secure auth across multiple applications: JWT (30-min expiry), bcrypt, OTP/MFA, RBAC, API-key microservice communication patterns.
- **Vulnerability Assessment & Penetration Testing** — Conducted VAPT assessments with network scanning, vulnerability identification, OWASP guidelines, and risk-rated remediation documentation.

## Certifications & Credentials

### Security
1. **Cisco Ethical Hacker** — Cisco — Hands-on ethical hacking, penetration testing, vulnerability assessment, web application security
2. **ISC2 Candidate** (March 2025 – March 2026) — Cybersecurity fundamentals, threat analysis, security governance, risk management
3. **Introduction to Cybersecurity** (Feb 2025) — Cisco — Threat detection, network security fundamentals
4. **Cisco Junior Cybersecurity Analyst Career Path** — In Progress — Cybersecurity analysis, incident response, SOC operations
5. **Cyber Shujaa — Cisco Ethical Hacker** (Cohort IV) — USIU-Africa, Serianu Ltd & Kenya Bankers Association — Ethical hacking with distinction

### Software Engineering
6. **Power Learn Project (PLP)** — Practical software engineering: application development, databases, REST APIs, version control, deployment

### Blockchain
7. **Stellar GIVE Impact Bootcamp** — Stellar Development Foundation — Production-oriented Soroban smart contracts, DeFi, invoice financing
8. **Stellar Quest — Blockchain Development** — Stellar Development Foundation — Gamified blockchain learning with challenges in smart contracts and dApp deployment

### Other
9. **Meru University Innovation Hub Member** — Technology innovation, collaborative project development

## Technical Skills
### Frontend
React.js, TypeScript, JavaScript, Vite, Tailwind CSS, Material UI, TanStack Query, Axios, Framer Motion, React Router, Responsive Web Design, HTML/CSS

### Backend
FastAPI, Express.js, Laravel, Python, Node.js, REST APIs, JWT, OAuth 2.0, bcrypt, OTP

### Databases & ORM
PostgreSQL, MySQL, Prisma, SQLAlchemy, Alembic, Firebase

### Blockchain
Rust, Soroban, Stellar, Solidity, Ethereum, SEP-41, Web3, Smart Contracts

### Security
VAPT, OWASP, Nmap, Burp Suite, Wireshark, iptables, Digital Forensics, Threat Analysis, OSINT, Network Monitoring, Firewall Configuration

### Infrastructure
Docker, Linux Administration, Ubuntu, Nginx, Tailscale, WireGuard, NetBird, Cloudflare, Let's Encrypt, Netlify, SSH, Git & GitHub

### Mobile
Flutter, Dart

### Tools & Methods
SEO, Troubleshooting, User Support, Environment Management, Postman, API Security, CI/CD Basics

## Engineering Philosophy
- "Reliable first, clever second"
- "Security designed in from the start, not added as an afterthought"
- "Clear architecture over clever abstractions"
- "Documented decisions over tribal knowledge"

## Links
- **Portfolio:** wesley534.netlify.app
- **GitHub:** github.com/Wesley534
- **X/Twitter:** @Wesley467954392
- **Stellar Quest Profile:** quest.stellar.org/profile/1307001494972923904
