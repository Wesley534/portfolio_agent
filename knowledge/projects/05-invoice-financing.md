# Invoice Financing Marketplace

**Category:** Blockchain Infrastructure
**Status:** Deployed (invoicefinancing.netlify.app)

## Description
A full-stack Soroban-powered platform where suppliers unlock working capital against verified invoices. Smart contracts handle liquidity pool deposits, financing agreements, and automated settlement with principal, interest, and fee distribution on the Stellar network. The React + TypeScript frontend provides dashboards for suppliers, investors, and administrators — with real-time contract state display via Stellar RPC.

## Architecture Decisions
- Separates on-chain contract logic from off-chain user management
- Off-chain transaction history and audit logging
- Soroban smart contracts for trustless settlement
- Stellar network for fast, low-cost transactions
- React frontend with TypeScript for type-safe contract interactions

## Tech Stack
Soroban, Stellar, React.js, TypeScript, Express.js, Prisma, Rust, Vite

## Highlight
Soroban smart contracts with on-chain settlement and off-chain audit trails

## Repository
github.com/Wesley534/stellar_give_project
