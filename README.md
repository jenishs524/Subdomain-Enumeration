# Subdomain-Enumeration


🎯 Objective

To automate the discovery of subdomains belonging to a target domain. Manual subdomain discovery—using search engines, DNS brute‑force, and public datasets—is time‑consuming and often incomplete. This tool consolidates multiple discovery techniques into a single, efficient pipeline, allowing security professionals to:

    Uncover hidden assets (e.g., dev.internal.company.com, staging.api.target.com).

    Identify exposed admin panels, test environments, and forgotten services that may be vulnerable.

    Map the attack surface of an organisation before launching further penetration testing activities.

    Enrich intelligence for threat hunting and continuous security monitoring.

🧠 How It Works – Technical Overview

The tool employs a multi‑layered approach to maximise subdomain discovery:
1. Brute‑Force Resolution (Active Discovery)

    Uses a curated wordlist of common subdomain names (e.g., www, mail, ftp, admin, api, dev, test, staging, dashboard, remote, git, jenkins, jira, confluence, nexus, sonar).

    For each subdomain, the tool performs a DNS A record query (IPv4) using a high‑performance DNS resolver.

    If the query returns a valid IP address, the subdomain is confirmed as active and logged.

    This approach is fast and effective for discovering standard‑naming conventions.

2. Passive DNS & OSINT Integration (Passive Discovery)

    Optionally queries public DNS datasets (e.g., SecurityTrails, VirusTotal, Censys, or local historical DNS databases) to discover subdomains that have been observed in the past but may not currently resolve.

    Passive DNS sources aggregate historical DNS records from global resolvers, providing a rich repository of subdomains that may have been taken offline or moved—valuable for uncovering legacy attack surfaces.

3. Permutation & Alteration (Advanced Discovery)

    Generates permutations of known subdomains (e.g., www → www1, www2, www-dev, www-test) using common patterns observed in real‑world naming conventions.

    This catches subtle variations that standard wordlists might miss.

4. Parallel Execution

    Utilises multi‑threading or asynchronous I/O to perform hundreds or thousands of DNS queries simultaneously, drastically reducing scan time.

    A full scan of a large wordlist (10,000+ entries) can be completed in minutes, not hours.

✨ Advanced Features (Real‑World Upgrade)
Feature	Implementation
Multi‑Source Integration	Combines brute‑force, passive DNS (SecurityTrails, VirusTotal), and permutation attacks for maximum coverage.
Large Wordlist Support	Supports wordlists of tens of thousands of entries (including leaks from real‑world subdomain collections like subdomains.txt from SecLists).
Wildcard Detection	Automatically detects and ignores wildcard DNS entries (e.g., *.target.com returning the same IP), preventing false positives.
Live Validation	Performs HTTP/HTTPS probes on discovered subdomains to verify they are actively hosting web services, reducing false positives from stale DNS records.
Banner Grabbing	Optionally fetches HTTP response headers (Server, X‑Powered‑By) to fingerprint the underlying technology (e.g., Apache, Nginx, Tomcat) for further vulnerability assessment.
Export in Multiple Formats	Saves results in plain text (.txt), JSON (.json), or CSV, facilitating integration with other tools (nmap, nuclei, eyewitness).
Progress Tracking & Resume	Saves intermediate results so scans can be resumed if interrupted, useful for extremely large target domains.
Recursive Discovery	Optionally probes discovered subdomains for additional sub‑subdomains (e.g., api.dev.target.com → v1.api.dev.target.com).
Threat Intelligence Enrichment	Cross‑references discovered subdomains with known threat intelligence feeds to identify if any are associated with known malware/phishing campaigns.
🛠️ Tools & Technologies

    Python 3 – core logic, threading, and asynchronous DNS resolution.

    dnspython – robust DNS query library for reliable A, AAAA, CNAME lookups.

    requests – for passive DNS API calls (SecurityTrails, VirusTotal) and optional HTTP probes.

    threading / asyncio – for high‑performance parallel scanning.

    Public Wordlists – curated from SecLists, Assassins‑Subdomain‑Discovery, and common‑names lists.

    JSON / CSV – for structured output.

🔬 Testing & Use Case

Scenario:
A penetration tester is engaged to assess example.com. The client is concerned about forgotten development systems exposing internal data.

Process:

    Run the enumeration tool against example.com:
    bash

python3 recon_pipeline.py example.com --wordlist subdomains.txt --passive --threads 50

    Discovery phase:

        Brute‑force discovers: www.example.com (93.184.216.34), mail.example.com (93.184.216.35), admin.example.com (203.0.113.5).

        Passive DNS (SecurityTrails) reveals: old-dev.example.com (198.51.100.10), staging-api.example.com (198.51.100.20).

        Permutation engine finds: www2.example.com (93.184.216.36).

    Validation:

        HTTP probe on admin.example.com returns a 200 OK with an X-Powered-By: PHP/5.6.40 header – an outdated and potentially vulnerable PHP version.

        staging-api.example.com responds with a 404, indicating the host is still resolvable but likely taken down – however, its existence reveals the organisation's naming pattern.

Outcome:

    The tester prioritises: admin.example.com (high potential due to outdated PHP), staging-api.example.com (could be a back‑end API with weak security).

    The client receives a complete list of exposed subdomains, enabling them to:

        Decommission or secure admin.example.com.

        Review staging-api.example.com access controls.

        Implement a consistent subdomain naming policy to avoid leakage of internal naming conventions.

This demonstrates how subdomain enumeration transforms a simple domain name into a detailed map of an organisation's internet‑facing assets, forming the foundation for all subsequent penetration testing activities.
📁 Output Example (JSON Structure)

A typical result file (JSON) contains an array of discovered subdomains with associated metadata:

    Subdomain – The full subdomain (e.g., api.target.com).

    IP Address – The resolved IPv4 address (if available).

    Discovery Source – bruteforce, passive, or permutation.

    HTTP Status – (Optional) Status code from HTTP probe (200, 403, 404, etc.).

    Server Header – (Optional) The server software identified (e.g., nginx/1.18.0).

    Response Time – Time to resolve and/or respond, useful for performance analysis.

📝 Conclusion

The Subdomain Enumeration Tool is an essential asset for any reconnaissance or penetration testing workflow. It automates the discovery of hidden, forgotten, or misconfigured subdomains that may represent the weakest link in an organisation's security posture. By combining active brute‑force, passive DNS intelligence, and intelligent permutation techniques, it provides a far more comprehensive view than any single method could achieve. During testing, it successfully discovered subdomains that were not resolvable via standard DNS (revealing legacy systems and development endpoints), highlighting the importance of layered enumeration. This tool empowers security teams to understand their external attack surface and proactively remediate exposure, making it a foundational capability for modern security operations.
