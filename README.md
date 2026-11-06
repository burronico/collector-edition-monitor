# Collector Edition Monitor

An automated monitoring system for videogame special editions, collector's editions, preorder announcements and restocks.

## Project overview

The project uses Python and GitHub Actions to monitor selected websites and send relevant notifications to a Discord channel.

The system runs in GitHub's cloud infrastructure, meaning no personal computer needs to remain switched on.

## Current architecture

- **Python:** Website monitoring and notification logic.
- **GitHub Actions:** Automated execution.
- **Discord Webhook:** Notification delivery.
- **JSON:** Storage of previously detected articles.

## Current monitoring sources

| Website | Monitoring method | Status |
|---|---|---|
| PlayStation Blog | RSS feed | Operational |

## Project files

- `monitor.py` — Main monitoring script.
- `seen_posts.json` — Stores previously detected articles.
- `.github/workflows/monitor.yml` — Automatically executes the monitoring script.
- `.github/workflows/test-discord.yml` — Tests the Discord connection.

## Configuration

The Discord webhook URL is stored securely in GitHub repository secrets.

Required secret:

`DISCORD_WEBHOOK_URL`

Never place webhook URLs, passwords or other private credentials directly in the source code.

## Automatic execution

The monitoring workflow is scheduled twice per hour, at minutes 07 and 37.

It can also be started manually through the GitHub Actions interface.

## Current limitations

- Only the PlayStation Blog RSS feed is currently monitored.
- The system currently searches for predefined edition-related keywords.
- Website monitoring is subject to source availability and GitHub Actions scheduling delays.
- Retailer stock monitoring has not yet been implemented.

## Future development

1. Add more official gaming news sources.
2. Monitor physical collector's editions across retailers.
3. Detect preorder openings and restocks.
4. Improve keyword filtering and notification accuracy.
5. Expand monitoring to digital Deluxe, Ultimate and Premium editions.
6. Improve reliability and error reporting.

## Cost

The project is designed to operate using free GitHub Actions resources and Discord webhooks.
