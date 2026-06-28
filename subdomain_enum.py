#!/usr/bin/env python3
import dns.resolver
import sys
import time
from datetime import datetime

# List of common subdomains (feel free to expand)
COMMON_SUBDOMAINS = [
    'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
    'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test',
    'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3',
    'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static',
    'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki',
    'web', 'media', 'email', 'images', 'img', 'download', 'dns', 'ns4', 'ns5',
    'sip', 'portal', 'info', 'apps', 'video', 'sites', 'cdn', 'storage', 'api',
    'app', 'dev', 'stage', 'prod', 'test', 'internal', 'external', 'backup',
    'monitor', 'status', 'dashboard', 'remote', 'git', 'jenkins', 'jira',
    'confluence', 'bitbucket', 'nexus', 'artifactory', 'sonar', 'elk', 'kibana',
    'prometheus', 'grafana', 'zabbix', 'nagios', 'puppet', 'chef', 'ansible',
    'terraform', 'vault', 'consul', 'nomad', 'minio', 'redis', 'mongo', 'mysql',
    'postgres', 'elastic', 'kafka', 'zookeeper', 'spark', 'hadoop', 'hive',
    'presto', 'airflow', 'druid', 'superset', 'metabase', 'redash'
]

def resolve_subdomain(subdomain, domain):
    """Try to resolve a subdomain to an IP address."""
    full_domain = f"{subdomain}.{domain}"
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '1.1.1.1']  # public DNS
        answers = resolver.resolve(full_domain, 'A')
        if answers:
            ips = [str(r) for r in answers]
            return ips
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
        pass
    except Exception:
        pass
    return None

def enumerate_subdomains(domain, wordlist=None):
    """Enumerate subdomains using a given wordlist."""
    if wordlist is None:
        wordlist = COMMON_SUBDOMAINS
    found = []
    total = len(wordlist)
    print(f"[*] Brute‑forcing {total} subdomains for {domain}...")
    for i, sub in enumerate(wordlist, 1):
        ips = resolve_subdomain(sub, domain)
        if ips:
            full = f"{sub}.{domain}"
            found.append({'subdomain': full, 'ips': ips})
            print(f"[+] {i}/{total} FOUND: {full} -> {', '.join(ips)}")
        else:
            # print progress every 20 attempts to avoid clutter
            if i % 20 == 0:
                print(f"[*] {i}/{total} ...")
    return found

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 subdomain_enum.py <domain>")
        print("Example: python3 subdomain_enum.py example.com")
        sys.exit(1)

    domain = sys.argv[1].strip().lower()
    print("=" * 60)
    print(f"  SUBDOMAIN ENUMERATION: {domain}")
    print("=" * 60)

    start_time = time.time()
    results = enumerate_subdomains(domain)
    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print(f"  SUMMARY – Found {len(results)} subdomains in {elapsed:.2f}s")
    print("=" * 60)
    for entry in results:
        print(f"  {entry['subdomain']} -> {', '.join(entry['ips'])}")

    # Save to file
    output_file = f"subdomains_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, 'w') as f:
        for entry in results:
            f.write(f"{entry['subdomain']} -> {', '.join(entry['ips'])}\n")
    print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
