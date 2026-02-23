#!/usr/bin/env python3
"""
Union Site Detector for Tor Network

Requirements:
- Python 3.x installed on your system
"""

import requests
import time
import sys
from bs4 import BeautifulSoup as soup

def test_site(url):
    """Test a single URL for union presence."""
    
    # Set up proxy configuration (Tor)
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    
    try:
        # Access the URL
        response = requests.get(url, timeout=10, proxies=proxies)
        
        # If request fails with Tor error codes, likely not a union site
        if "TorDNSEL" in response.text or \
           ("HTTP Error 524" in response.text and "cloudflare" in url) or \
           (response.status_code == 0):
            return False
        
        # Parse HTML content
        doc = soup(response.text, 'html.parser')
        
        # Check for known union indicators
        indicators = [
            'union', 'unie', 'cooperatie',
            'federation', 'vereniging', 
            'samenwerkingsverband'
        ]
        
        found_indicator = False
        
        # Search page title and content for indicators
        if doc.title:
            text_content = str(doc.title) + " " + response.text.lower()
            
            for indicator in indicators:
                if indicator.lower() in text_content:
                    found_indicator = True
                    break
                
        return found_indicator
    
    except Exception as e:
        print(f"[Error testing {url}]: {e}")
    
    return False

def main():
    """Main execution flow."""
    
    try:
        # List of URLs to check (example: known union sites)
        test_urls = [
            "``` http://unionexample.onion", ```
            "https://example.torproject.org/union",
            "http://test.torproject.org"
        ]
        
        print("[*] Starting scan...")
        
        for url in test_urls:
            if test_site(url):
                print(f"[✓] UNION DETECTED at {url}")
            else:
                print(f"[✗] No union detected: {url}")

    except KeyboardInterrupt:
        print("\n[!] Scan cancelled.")
    
    except Exception as e:
        print(f"[Critical Error]: {e}")

if __name__ == "__main__":
    main()
