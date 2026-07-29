# Harbor Auctions — No-Loss Escrow Marketplace

**Category:** Blockchain Infrastructure
**Status:** Deployed (harborauctions.netlify.app)

## Description
A Soroban-based auction marketplace where only the current highest bid stays locked in escrow — losing bidders get refunded instantly. Features simulated yield accrual against locked principal, on-chain delivery confirmation, and dispute resolution with split settlement. Designed as a single-contract architecture to simplify deployment and frontend integration. The React + TypeScript + Tailwind CSS frontend provides real-time auction state, bid management, and dispute handling.

## Architecture Decisions
- Single-contract design for simpler deployment
- No-loss escrow — only the current winner's bid is locked
- On-chain delivery confirmation and dispute resolution
- Simulated yield accrual for locked principal
- Tailwind CSS for responsive, mobile-friendly auction interface

## Tech Stack
Soroban, Stellar, Rust, React.js, TypeScript, Tailwind CSS, Vite, IPFS

## Highlight
Single-contract design with escrow, yield simulation, and on-chain dispute resolution

## Repository
github.com/Wesley534/no_loss_auction
