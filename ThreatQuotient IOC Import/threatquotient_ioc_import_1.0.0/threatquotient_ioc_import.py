"""
Copyright © 2024 Forescout Technologies, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import urllib.request
import urllib.error
import json
import datetime
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration parameters
url = params.get("connect_threatquotient_url", '').strip()
api_key = params.get("connect_threatquotient_api_key", '').strip()
source_id = params.get("connect_threatquotient_source_id", '').strip()
tq_poll_interval = params.get("connect_threatquotient_poll_interval", 1440)  # Default 24 hours
tq_severity_mapping = {
    "critical": params.get("connect_threatquotient_critical_score", 90),
    "high": params.get("connect_threatquotient_high_score", 70),
    "medium": params.get("connect_threatquotient_medium_score", 50)
}

# Requests Proxy
is_proxy_enabled = params.get("connect_proxy_enable")
if is_proxy_enabled == "true":
    proxy_ip = params.get("connect_proxy_ip")
    proxy_port = params.get("connect_proxy_port")
    proxy_user = params.get("connect_proxy_username")
    proxy_pass = params.get("connect_proxy_password")
    if not proxy_user:
        proxy_url = f"https://{proxy_ip}:{proxy_port}"
        proxies = {"https": proxy_url}
        logger.debug("Proxy enabled / no user")
    else:
        proxy_url = f"https://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}"
        proxies = {"https": proxy_url}
        logger.debug("Proxy enabled / user")
else:
    logger.debug("Proxy disabled")
    proxies = None

def get_threatquotient_indicators():
    """Fetch indicators from ThreatQuotient API with pagination support"""
    headers = {
        "Content-Type": "application/json"
    }
    
    # Handle API key authentication
    if api_key.startswith("Bearer "):
        headers["Authorization"] = api_key
    else:
        headers["Authorization"] = f"Bearer {api_key}"
    
    # Calculate time range based on poll interval
    end_time = datetime.datetime.utcnow()
    start_time = end_time - timedelta(minutes=int(tq_poll_interval))
    
    # Format dates for API
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Build API request
    api_url = f"{url}/api/v1/indicators"
    
    all_indicators = []
    offset = 0
    limit = 1000  # Maximum allowed by API
    
    while True:
        params = {
            "source_id": source_id,
            "created_after": start_time_str,
            "created_before": end_time_str,
            "status": "active",
            "limit": limit,
            "offset": offset,
            "sort_by": "created_at",
            "sort_order": "desc"
        }
        
        try:
            response = urllib.request.Request(api_url, headers=headers, data=json.dumps(params).encode('utf-8'), method="GET")
            if proxies:
                response.set_proxy(proxy_url, proxies)
            with urllib.request.urlopen(response) as f:
                data = json.loads(f.read().decode('utf-8'))
            
            if not data.get("data"):
                break
                
            all_indicators.extend(data["data"])
            offset += limit
            
            if len(data["data"]) < limit:
                break
                
        except urllib.error.HTTPError as e:
            if e.code == 401:
                logger.error("Unauthorized: Invalid API key")
            elif e.code == 403:
                logger.error("Forbidden: Insufficient permissions")
            elif e.code == 429:
                logger.error("Rate limit exceeded")
            elif e.code == 500:
                logger.error("ThreatQuotient server error")
            else:
                logger.error(f"Error fetching indicators from ThreatQuotient: {e}")
            return None
    
    return {"data": all_indicators}

def process_indicator(indicator):
    """Process a single indicator and convert it to Forescout IOC format"""
    ioc_info = {}
    
    # Extract basic information
    ioc_info["name"] = indicator.get("title", "Unknown Threat")
    ioc_info["severity"] = evaluate_severity(indicator.get("score", 0))
    
    # Process different indicator types
    indicator_type = indicator.get("type", "").lower()
    
    # File indicators
    if indicator_type in ["file", "filename", "filepath"]:
        if "md5" in indicator:
            ioc_info["md5"] = indicator["md5"]
        if "sha1" in indicator:
            ioc_info["sha1"] = indicator["sha1"]
        if "sha256" in indicator:
            ioc_info["sha256"] = indicator["sha256"]
        if "filename" in indicator:
            ioc_info["file_name"] = indicator["filename"]
            
    # Network indicators
    elif indicator_type in ["url", "ip", "ipv4", "ipv6", "domain", "hostname"]:
        if "url" in indicator:
            ioc_info["cnc"] = indicator["url"]
        elif "ip" in indicator:
            ioc_info["cnc"] = indicator["ip"]
        elif "domain" in indicator:
            ioc_info["cnc"] = indicator["domain"]
            
    # Email indicators
    elif indicator_type in ["email", "email_subject", "email_body"]:
        if "email" in indicator:
            ioc_info["cnc"] = indicator["email"]
            
    # Malware indicators
    elif indicator_type in ["malware", "malware_family"]:
        if "name" in indicator:
            ioc_info["name"] = f"Malware: {indicator['name']}"
    
    # Add platform information if available
    if "platforms" in indicator:
        platforms = indicator["platforms"]
        platform_mapping = {
            "windows": "Microsoft Windows",
            "windows_10": "Microsoft Windows 10",
            "windows_11": "Microsoft Windows 11",
            "linux": "Linux",
            "ubuntu": "Linux",
            "centos": "Linux",
            "macos": "macOS",
            "android": "Android",
            "ios": "iOS"
        }
        
        for platform in platforms:
            platform_lower = platform.lower()
            if platform_lower in platform_mapping:
                ioc_info["platform"] = platform_mapping[platform_lower]
                break
        if "platform" not in ioc_info:
            ioc_info["platform"] = "All"
    
    return ioc_info

def evaluate_severity(score):
    """Evaluate severity based on score"""
    if score >= tq_severity_mapping["critical"]:
        return "Critical"
    elif score >= tq_severity_mapping["high"]:
        return "High"
    elif score >= tq_severity_mapping["medium"]:
        return "Medium"
    return "Low"

def main():
    """Main function to process indicators from ThreatQuotient"""
    response = {}
    ioc_infos = []
    
    try:
        # Validate required parameters
        required_params = ["connect_threatquotient_url", "connect_threatquotient_api_key", "connect_threatquotient_source_id"]
        for param in required_params:
            if not params.get(param):
                logger.error(f"Missing required parameter: {param}")
                return {"error": f"Missing required parameter: {param}"}
        
        # Fetch indicators from ThreatQuotient
        indicators = get_threatquotient_indicators()
        
        if indicators and "data" in indicators:
            for indicator in indicators["data"]:
                ioc_info = process_indicator(indicator)
                if ioc_info:
                    ioc_infos.append(ioc_info)
        
        if not ioc_infos:
            logger.debug("No indicators found from ThreatQuotient")
        else:
            logger.debug(f"Found {len(ioc_infos)} indicators from ThreatQuotient")
            response["ioc"] = ioc_infos
            
            # Add metadata to response
            response["metadata"] = {
                "last_poll": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "indicator_count": len(ioc_infos)
            }
        
        return response
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    main() 