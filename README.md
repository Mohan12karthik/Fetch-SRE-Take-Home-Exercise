# Fetch Site Reliability Engineering Take Home Exercise

## Overview

This project is a Site Reliability Engineer (SRE) challenge from Fetch Rewards. It monitors HTTP endpoints defined in a YAML configuration and logs the cumulative availability of each domain every 15 seconds.

---

## Features

- Accepts a YAML configuration file defining multiple HTTP endpoints
- Sends requests using appropriate method, headers, and body (if any)
- Determines endpoint availability based on:
  - HTTP status code between 200 and 299
  - Response time ≤ 500ms
- Ignores port numbers and URL paths when grouping endpoints by domain
- Prints cumulative availability percentage per domain every 15 seconds

---

## 🛠️ Installation & Running the Monitor

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/fetch-sre-monitor.git
cd fetch-sre-monitor 
```
### 2. Install Dependencies
  - You’ll need Python 3.7+ and requests and pyyaml:
```bash
pip install -r requirements.txt
```
  - Or install manually:
```bash
pip install requests pyyaml
```
### 3. Run the Monitor
```bash
python3 main.py sample.yaml
```
Press Ctrl+C to stop.

## Sample Output
```bash
(venv) (base) mohankarthikv@Mohans-MacBook-Pro sre-take-home-exercise-python % python3 main.py sample.yaml
Availability Report:
dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
---
Availability Report:
dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
---
Availability Report:
dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
---
Availability Report:
dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 25% availability percentage
---
^C
Monitoring stopped by user.
```

## Configuration Format (sample.yaml)

```yaml
- name: example GET
  url: https://example.com/
  method: GET

- name: example POST
  url: https://example.com/data
  method: POST
  headers:
    content-type: application/json
  body: '{"key": "value"}'
```
  - name – optional free-text description

  - url – required, valid HTTP/HTTPS URL

  - method – optional, defaults to GET

  - headers – optional HTTP headers

  - body – optional JSON-encoded string for POST/PUT

## Identified Issues and Fixes

1. Incorrect Domain Grouping
  - Issue: Used full URL path (e.g., /body) as domain key.

  - Fix: Used urlparse(url).hostname to extract only the domain, ignoring path and port.

2. Timeout/Performance
  - Fix: Used timeout=1 in HTTP requests to enforce a 1-second limit and calculated response time in milliseconds.

3. Cumulative Availability
  - Fix: Used a defaultdict to store and calculate total and successful checks per domain.

4. Command-Line Argument Validation
  - Fix: Added validation for the required YAML config file argument.

## License
  - This project is part of a coding challenge and is not intended for production use.
