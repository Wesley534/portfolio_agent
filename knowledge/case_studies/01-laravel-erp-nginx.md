# Deploying a Laravel ERP Behind Nginx

**Category:** Infrastructure

## Overview
A Laravel 7.30.7 ERP managing records, loan disbursements, mobile payments, and KYC identity verification — needed to be securely exposed to end users on a single Ubuntu 24.04 VPS (3.8 GB RAM, 48 GB disk).

## Problem
The ERP required HTTPS, efficient PHP-FPM request routing, support for large file uploads (50 MB limit for KYC identity documents), and a maintainable deployment on constrained hardware. The application integrates with payment APIs, mapping services, SMS/WhatsApp integrations, and a KYC AI microservice — demanding clean URL routing, proper proxy header forwarding, and service isolation.

## Solution
Configured Nginx as the reverse proxy serving the Laravel application via PHP 7.4-FPM on a Unix socket (`/run/php/php7.4-fpm.sock`). Terminated TLS with a self-signed certificate for internal LAN access. Configured Tailscale Funnel for public HTTPS at the edge (automated TLS, no Certbot needed). Implemented 50 MB upload limit, Laravel-compatible URL rewriting via `try_files`, hidden file access denial, and gzip compression.

## Key Highlights
- Reverse proxy configuration serving Laravel via PHP-FPM on Unix socket
- SSL/TLS termination with self-signed certificate for LAN access
- 50 MB upload limit for KYC document submissions
- Tailscale Funnel for public HTTPS at the edge (automated TLS)
- Hidden file protection (.git, .env, etc.)
- Dual HTTP/HTTPS server blocks with clean separation

## Tech Stack
Nginx, Ubuntu 24.04, PHP 7.4, Laravel 7, PHP-FPM, MySQL, Tailscale Funnel

## Outcome
The ERP is securely accessible via HTTPS through Tailscale Funnel with automated TLS, clean URL routing, and efficient PHP-FPM management — running smoothly on a single VPS with modest resources.

## Lessons Learned
Running a full ERP on a modest VPS works well when Nginx handles static assets efficiently and PHP-FPM manages dynamic requests. Tailscale Funnel's automated TLS eliminates the complexity of manual certificate management — no Certbot, no cron jobs, no open ports.
