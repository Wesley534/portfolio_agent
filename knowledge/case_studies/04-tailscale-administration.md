# Securing Remote Server Access with Tailscale

**Category:** Infrastructure

## Overview
A tailnet of 18+ devices spanning production servers, staging environments, development laptops, and mobile devices needed secure remote administration without exposing SSH or other services to the public internet.

## Problem
Multiple servers distributed across different networks and cloud providers were managed via SSH on public IPs — a constant target for brute-force attacks. Traditional VPN solutions add complexity and don't provide easy public HTTPS ingress for web services. Needed a unified solution for encrypted peer-to-peer access, service exposure, and device management.

## Solution
Deployed Tailscale (WireGuard-based) across the infrastructure, creating a secure tailnet with 18+ connected devices. Enabled Tailscale Funnel for the main application — providing public HTTPS without opening firewall ports. All servers get unique 100.x.x.x Tailscale IPs with automatic WireGuard encryption. Exit node configured for routing traffic from remote locations. Multi-platform support: Linux servers, Windows desktop, Android phone.

## Key Highlights
- WireGuard-based mesh VPN with 18+ connected devices
- Tailscale Funnel for public HTTPS ingress (no open ports)
- Multi-platform: Linux, Windows, Android
- Cross-network connectivity across production/staging/dev environments
- Exit node for outbound traffic routing
- Peer-to-peer encrypted tunnels with automatic NAT traversal

## Tech Stack
Tailscale 1.98, WireGuard, Ubuntu 24.04, NetBird, Linux, SSH

## Outcome
Reduced attack surface while maintaining convenient encrypted remote access across all environments. The tailnet connects production servers, staging instances, development machines, and mobile devices — all with automatic WireGuard encryption and zero configuration overhead.

## Lessons Learned
Tailscale's mesh VPN is dramatically simpler and more secure than port forwarding or traditional VPNs for small-scale infrastructure. Funnel provides automated TLS and public access without server-side configuration. Running both Tailscale and NetBird adds redundancy but operational complexity — a single mesh VPN suffices at this scale.
