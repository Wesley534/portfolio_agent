# Deploying Soroban Smart Contracts to Stellar Testnet

**Category:** Blockchain

## Overview
DisburseFlow — a forked and extended Stellar Disbursement Platform — needed Soroban smart contracts to manage embedded wallets for bulk payment recipients. The goal: deploy Rust-based smart-wallet contracts to Stellar testnet, integrate WebAuthn passkey authentication, and use sponsored accounts to bundle wallet creation and payments into single transactions to minimize gas fees. Critically, the entire blockchain layer is invisible to both end users and administrators — wallet creation is masked behind a token-based flow, and all amounts display in fiat currency (USD, EUR) through Circle's payment rails.

## Problem
The Stellar Disbursement Platform handles bulk disbursements but has no embedded wallet — every recipient needs their own Stellar account. For non-crypto-savvy users, asking them to set up wallets is a non-starter. DisburseFlow needed: a Soroban smart wallet controlled by device biometrics (passkeys/WebAuthn), sponsored transactions so the distribution account pays recipient gas fees, gas bundling to combine wallet creation + payment in single transactions, and a Rust → WASM compilation pipeline deployed to Stellar testnet.

## Solution
Built and deployed the DisburseFlow smart contract ecosystem using Soroban (Rust → WASM) with a smart-wallet contract implementing CustomAccountInterface for WebAuthn authentication via secp256r1 ECDSA. Wallet creation uses HostFunctionTypeCreateContractV2 with contract IDs derived from the distribution account and SHA-256 of user public keys. Sponsored transactions have the distribution account as source for InvokeHostFunction operations. Channel accounts handle sequencing with a 300-second timeout. Gas bundling via ChannelTransactionBundleModel groups wallet creation and disbursement in single Soroban transactions. Wallet creation is masked behind UUID invitation tokens — users just register a passkey. The Circle service converts USDC→USD and EURC→EUR automatically for a fiat-first admin experience.

## Key Highlights
- Soroban smart-wallet contract with WebAuthn (passkey) auth via secp256r1 ECDSA
- Rust → WASM compilation with soroban-sdk v22, deployed to Stellar testnet
- Sponsored accounts — distribution account sponsors gas for recipient operations
- Gas bundling — wallet creation and payment in single Soroban transaction
- Wallet creation fully masked behind token-based invitation flow
- Fiat-first admin UI — admins see USD/EUR, not XLM or USDC
- Circle API integration translates Stellar assets to fiat codes

## Tech Stack
Soroban, Stellar, Rust, WASM, Soroban SDK v22, Go, WebAuthn, secp256r1/P-256, Stellar RPC, Circle API

## Outcome
Deployed and verified Soroban smart-wallet contracts on Stellar testnet enabling: embedded wallets controlled by user passkeys (no secret key management), sponsored transaction flow where the distribution account pays all gas fees, bundled wallet creation + first disbursement in single transactions cutting gas costs ~50%, and zero crypto exposure for end users or administrators. The platform is deployable with `make dev` and testable with the Stellar Demo Wallet.

## Lessons Learned
1. **Sponsored accounts are essential for adoption** — if recipients need XLM reserves, they won't use your dApp
2. **Bundling saves real money** — combining wallet creation and payment in a single Soroban transaction can cut gas costs nearly in half
3. **Transaction simulation is non-negotiable** — Soroban RPC SimulateTransaction returns exact gas costs and auth entries; submitting without simulation guarantees failure
4. **Channel accounts prevent contention** — parallel disbursements with unique sequence numbers prevent transaction conflicts
5. **Masking blockchain complexity is the real product** — the biggest achievement isn't the smart contract, it's that the blockchain is invisible: wallet creation is a background process, and the admin UI shows familiar fiat amounts
