import yaml
import requests
import time
from collections import defaultdict
from urllib.parse import urlparse

# Function to load configuration from the YAML file
def load_config(file_path):
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        
    for endpoint in config:
        if 'url' not in endpoint:
            raise ValueError("Missing 'url' field in endpoint")
        if 'method' not in endpoint:
            endpoint['method'] = 'GET'
    return config


# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=5)
        response_time = (time.time() - start_time) * 1000
        
        if 200 <= response.status_code < 300 and response_time <= 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Extract domain without port
def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            # domain = endpoint["url"].split("//")[-1].split(":")[0]
            domain = extract_domain(endpoint["url"])
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1
		
        print("Availability Report:")
        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
