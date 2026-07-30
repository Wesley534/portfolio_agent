# Secure HTTPS Deployment with Tailscale Funnel

**Category:** Infrastructure

## Overview
A Laravel ERP and its internal services were initially served over plain HTTP on the local network. Public HTTPS was needed for remote access by field agents and administrators — without the operational overhead of traditional certificate management.

## Problem
Services were served over plain HTTP on port 80, exposing API traffic including payment callbacks, KYC identity document uploads, and sensitive financial data. Traditional Let's Encrypt + Certbot would require maintaining cron jobs, monitoring expiry dates, and opening port 80/443 for ACME challenges.

## Solution
Used Tailscale Funnel to provide automated HTTPS at the network edge. Tailscale automatically provisions and renews TLS certificates for the *.ts.net domain, terminating HTTPS before forwarding as plain HTTP to local Nginx. For internal LAN access, a self-signed certificate was generated with OpenSSL, configured in Nginx's SSL server block with TLS 1.2/1.3 only, strong ciphers, and server-side cipher preference.

## Key Highlights
- Tailscale Funnel provides automatic TLS cert issuance and renewal — zero server-side ACME config
- Self-signed certificate for internal LAN HTTPS access
- TLS 1.2 and 1.3 only with strong cipher configuration
- No public ports exposed — Funnel handles ingress at the edge
- Dual HTTP (funnel) / HTTPS (LAN) server blocks

## Tech Stack
Tailscale Funnel, Tailscale 1.98, Nginx, Ubuntu 24.04, OpenSSL

## Outcome
All application traffic is served securely over HTTPS with zero-touch certificate management. Tailscale Funnel handles automatic issuance, renewal, and TLS termination — eliminating Certbot, cron jobs, and manual renewal. Public ingress requires no open firewall ports.

## Lessons Learned
Tailscale Funnel is a superior alternative to Let's Encrypt for small-scale deployments — automated TLS without any server-side Certbot configuration, cron jobs, or port management. The dual-server-block pattern (HTTP for funnel, HTTPS for LAN) keeps the configuration clean.
