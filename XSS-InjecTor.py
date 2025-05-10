import requests
from urllib.parse import urlparse
from termcolor import cprint

def load_wordlist(source):
    if source.startswith("http://") or source.startswith("https://"):
        try:
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            lines = response.text.splitlines()
        except Exception as e:
            cprint(f"[!] Error loading wordlist from URL: {e}", "red")
            return []
    else:
        try:
            with open(source, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            cprint(f"[!] Error reading local wordlist: {e}", "red")
            return []
    
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

def classify(payload, response_text):
    if payload in response_text:
        if any(x in payload.lower() for x in ["<script", "onerror", "onload", "svg", "img", "alert", "prompt"]):
            return "high"
        return "medium"
    return "low"

def test_xss(domain, payloads, param="q"):
    for payload in payloads:
        try:
            response = requests.get(domain, params={param: payload}, timeout=8)
            level = classify(payload, response.text)
            if level == "high":
                cprint(f"[!!!] High risk reflection: {payload}", "red")
            elif level == "medium":
                cprint(f"[!] Reflected but neutral: {payload}", "yellow")
            else:
                cprint(f"[-] Clean: {payload}", "green")
        except requests.exceptions.RequestException as e:
            cprint(f"[!] Request error with payload: {payload} - {e}", "magenta")

if __name__ == "__main__":
    domain = input("Full domain (e.g. https://example.com/page): ").strip()
    param = input("Parameter to test (e.g. q): ").strip()
    wordlist_source = input("Wordlist path or URL: ").strip()
    payloads = load_wordlist(wordlist_source)
    if payloads:
        test_xss(domain, payloads, param)
