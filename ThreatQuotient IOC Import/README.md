# ThreatQuotient IOC Import for Forescout eyeExtend Connect

This eyeExtend Connect app enables Forescout to import Indicators of Compromise (IOCs) from ThreatQuotient using their REST API. The app polls the ThreatQuotient API at configurable intervals to retrieve new indicators and syncs them into Forescout.

## Features

- Polls ThreatQuotient API for new indicators
- Supports multiple indicator types:
  - File indicators (MD5, SHA1, SHA256 hashes)
  - URL indicators
  - IP indicators
  - Domain indicators
- Configurable severity thresholds based on ThreatQuotient scores
- Platform-specific indicator mapping
- Proxy support for API communication
- Configurable polling interval

## Prerequisites

- Forescout eyeExtend Connect
- ThreatQuotient instance with API access
- ThreatQuotient API key
- Source ID from ThreatQuotient containing the indicators to import

## Installation

1. Download the `ThreatQuotient IOC Import` folder
2. Import the app into your Forescout eyeExtend Connect instance
3. Configure the app with your ThreatQuotient credentials and settings

## Configuration

### Required Settings

- **Source Name**: A friendly name for this ThreatQuotient source
- **ThreatQuotient URL**: The base URL of your ThreatQuotient instance
- **API Key**: Your ThreatQuotient API key
- **Source ID**: The ID of the ThreatQuotient source containing indicators to import

### Optional Settings

- **IOC refresh interval**: How often to poll for new indicators (default: 1440 minutes / 24 hours)
- **Severity Thresholds**: Configure score thresholds for Critical, High, and Medium severity levels
- **Proxy Settings**: Configure proxy server if required for API communication

## Indicator Types

The app supports the following indicator types from ThreatQuotient:

### File Indicators
- MD5 hashes
- SHA1 hashes
- SHA256 hashes
- File names

### Network Indicators
- URLs
- IP addresses
- Domain names

## Severity Mapping

Indicators are assigned severity levels based on their ThreatQuotient scores:

- Critical: Score ≥ 90 (configurable)
- High: Score ≥ 70 (configurable)
- Medium: Score ≥ 50 (configurable)
- Low: Score < 50

## Platform Support

The app maps ThreatQuotient platform information to Forescout platform types:
- Windows → Microsoft Windows
- Linux → Linux
- macOS → macOS
- Other → All

## Troubleshooting

1. Check the Forescout logs for any API communication errors
2. Verify your ThreatQuotient API key and permissions
3. Ensure the Source ID is correct and contains indicators
4. Check proxy settings if using a proxy server

## Support

For issues or questions, please contact Forescout support or refer to the ThreatQuotient API documentation.

## License

Copyright © 2024 Forescout Technologies, Inc. All rights reserved. 