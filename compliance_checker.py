#!/usr/bin/env python3
"""
Apify Actor Compliance Checker
==============================
Comprehensive 12-point store-readiness audit for all actors under an Apify org.

Checks: Description, SEO Metadata, Categories, Publication Status, README.md,
Input Schema, Output Schema, Example Input, Source Code Quality, Latest Build,
Permissions, Recent Runs.

Usage:
    APIFY_API_TOKEN=<token> python3 compliance_checker.py
"""

import os, sys, json, time, urllib.request
from datetime import datetime

TOKEN = os.environ.get("APIFY_API_TOKEN", "")
BASE = "https://api.apify.com/v2"

if not TOKEN:
    print("ERROR: APIFY_API_TOKEN not set.")
    sys.exit(1)

def api_get(path, timeout=15):
    sep = "&" if "?" in path else "?"
    url = f"{BASE}{path}{sep}token={TOKEN}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Apify-Compliance-Checker/1.0")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def check_description(actor):
    desc = actor.get("description", "")
    if not desc: return False, "MISSING", "No description set."
    if len(desc) < 50: return False, "TOO_SHORT", f"Only {len(desc)} chars."
    if len(desc) > 300: return None, "WARN", f"{len(desc)} chars — may truncate."
    return True, "OK", f"{len(desc)} chars"

def check_seo(actor):
    st = actor.get("seoTitle", "")
    sd = actor.get("seoDescription", "")
    issues = []
    if not st: return False, "MISSING", "No SEO title."
    if len(st) > 60: issues.append(f"Title {len(st)} chars (max 60)")
    if not sd: issues.append("No SEO description")
    if issues: return None, "WARN", "; ".join(issues)
    return True, "OK", f"Title {len(st)}c | Desc {len(sd)}c"

def check_categories(actor):
    cats = actor.get("categories", [])
    valid = {"AI","DEVELOPER_TOOLS","ECOMMERCE","LEAD_GENERATION","OPEN_SOURCE","SEO_TOOLS","SOCIAL_MEDIA","TRAVEL","VIDEOS"}
    if not cats: return False, "MISSING", "No categories."
    invalid = [c for c in cats if c not in valid]
    if invalid: return False, "INVALID", str(invalid)
    return True, "OK", ", ".join(cats)

def check_readme(versions):
    for v in reversed(versions):
        for f in v.get("sourceFiles", []):
            if f["name"] == "README.md":
                content = f.get("content", "")
                size = len(content)
                required = ["## Features", "## Input", "## Output"]
                missing = [s for s in required if s.lower() not in (content.lower() if isinstance(content, str) else "")]
                if size < 100: return False, "TOO_SHORT", f"{size} chars (v{v['versionNumber']})"
                if missing: return None, "INCOMPLETE", f"Missing: {', '.join(missing)} (v{v['versionNumber']})"
                return True, "OK", f"{size} chars, all sections (v{v['versionNumber']})"
    return False, "MISSING", "No README.md"

def check_input_schema(versions):
    for v in reversed(versions):
        for f in v.get("sourceFiles", []):
            if f["name"] == ".actor/INPUT_SCHEMA.json":
                try:
                    schema = json.loads(f.get("content", "{}"))
                except json.JSONDecodeError:
                    return False, "INVALID_JSON", f"Not valid JSON (v{v['versionNumber']})"
                issues = []
                if "title" not in schema: issues.append("missing title")
                if "properties" not in schema: issues.append("missing properties")
                if not schema.get("properties"): issues.append("no properties defined")
                for bad in ["prefill", "enumTitles"]:
                    if bad in str(schema): issues.append(f"forbidden field '{bad}'")
                if issues: return False, "ISSUES", "; ".join(issues)
                return True, "OK", f"{len(schema.get('properties',{}))} fields (v{v['versionNumber']})"
    return False, "MISSING", "No INPUT_SCHEMA.json"

def check_output_schema(versions):
    for v in reversed(versions):
        for f in v.get("sourceFiles", []):
            if f["name"] == ".actor/OUTPUT_SCHEMA.json":
                try:
                    schema = json.loads(f.get("content", "{}"))
                except json.JSONDecodeError:
                    return False, "INVALID_JSON", f"Not valid JSON (v{v['versionNumber']})"
                if "actorOutputSchemaVersion" not in schema:
                    return False, "WRONG_FORMAT", "Use 'actorOutputSchemaVersion' not 'schemaVersion'"
                return True, "OK", f"Present (v{v['versionNumber']})"
    return None, "MISSING", "No OUTPUT_SCHEMA.json (optional)"

def check_example_input(actor):
    body = actor.get("exampleRunInput", {}).get("body", "")
    if not body: return False, "MISSING", "No example input."
    try:
        if not json.loads(body): return None, "EMPTY", "Empty JSON object"
    except json.JSONDecodeError:
        return False, "INVALID_JSON", "Not valid JSON"
    return True, "OK", body[:80]

def check_source(versions):
    for v in reversed(versions):
        for f in v.get("sourceFiles", []):
            if f["name"] == "main.py":
                c = f.get("content", "").lower()
                checks = {
                    "retry": "retry" in c or "backoff" in c,
                    "user_agent": "user-agent" in c,
                    "error_handling": "try:" in c and "except" in c,
                    "logging": "logging" in c or "print(" in c,
                    "timeout": "timeout" in c,
                }
                score = sum(checks.values())
                missing = [k for k,v in checks.items() if not v]
                if score == 5: return True, "OK", f"All 5 pass (v{v['versionNumber']})"
                if score >= 3: return None, "WARN", f"Missing: {', '.join(missing)}"
                return False, "LOW", f"Missing: {', '.join(missing)}"
    return False, "MISSING", "No main.py"

def check_builds(aid):
    try:
        items = api_get(f"/acts/{aid}/builds").get("data", {}).get("items", [])
        if not items: return None, "NONE", "No builds"
        s = items[0].get("status")
        v = items[0].get("versionNumber", "?")
        if s == "SUCCEEDED": return True, "OK", f"#{items[0].get('buildNumber')} v{v} SUCCEEDED"
        return False, s, f"#{items[0].get('buildNumber')} v{v} {s}"
    except Exception as e:
        return False, "ERROR", str(e)[:80]

def check_permissions(actor):
    p = actor.get("actorPermissionLevel", "?")
    if p == "FULL_PERMISSIONS": return True, "OK", "FULL"
    return None, "WARN", p

def check_runs(aid):
    try:
        items = api_get(f"/acts/{aid}/runs?limit=5").get("data", {}).get("items", [])
        ok = [r for r in items if r.get("status") == "SUCCEEDED"]
        if ok: return True, "OK", f"{len(ok)}/{len(items)} succeeded"
        if items: return None, "NONE_OK", f"{len(items)} runs, 0 succeeded"
        return None, "NONE", "Never tested"
    except Exception as e:
        return None, "ERROR", str(e)[:80]

def audit(actor, versions):
    return [
        ("Description", check_description(actor)),
        ("SEO", check_seo(actor)),
        ("Categories", check_categories(actor)),
        ("Published", (True, "OK", "Published") if actor.get("isPublic") else (False, "NO", "Not published")),
        ("README", check_readme(versions)),
        ("Input Schema", check_input_schema(versions)),
        ("Output Schema", check_output_schema(versions)),
        ("Example Input", check_example_input(actor)),
        ("Source Code", check_source(versions)),
        ("Latest Build", check_builds(actor["id"])),
        ("Permissions", check_permissions(actor)),
        ("Runs", check_runs(actor["id"])),
    ]

def main():
    print("=" * 70)
    print(f"  APIFY ACTOR COMPLIANCE AUDIT — {datetime.now():%Y-%m-%d %H:%M}")
    print("=" * 70)
    
    user = api_get("/users/me")["data"]
    print(f"\n✓ {user.get('username')} ({user.get('email')})")
    
    items = api_get("/acts").get("data", {}).get("items", [])
    items.sort(key=lambda a: a.get("name", ""))
    print(f"✓ {len(items)} actors\n")
    
    results = []
    for i, a in enumerate(items):
        print(f"[{i+1}/{len(items)}] {a['name']}...")
        detail = api_get(f"/acts/{a['id']}")["data"]
        results.append((a["name"], a["id"], audit(detail, detail.get("versions", []))))
        time.sleep(0.3)
    
    # Summary table
    headers = [c[0] for c in results[0][2]]
    print(f"\n{'Actor':30}", end="")
    for h in headers: print(f"{h[:9]:>10}", end="")
    print("\n" + "-" * (30 + len(headers) * 10))
    
    total_pass = 0; total_checks = 0
    for name, aid, checks in results:
        print(f"{name[:30]:30}", end="")
        for _, (passed, status, msg) in checks:
            total_checks += 1
            if passed is True: total_pass += 1; print("     ✅    ", end="")
            elif passed is False: print("     ❌    ", end="")
            else: print("     ⚠️    ", end="")
        print()
    
    print(f"\nScore: {total_pass}/{total_checks} ({total_pass*100//total_checks}%)")
    
    # Detailed failures
    print("\n" + "=" * 70)
    print("  FAILURES & WARNINGS")
    print("=" * 70)
    for name, aid, checks in results:
        issues = [(cn, st, msg) for cn, (p, st, msg) in checks if p is False or p is None]
        if issues:
            print(f"\n## {name} ({aid})")
            for cn, st, msg in issues:
                icon = "❌" if any(c[0]==cn and c[1] is False for c in checks) else "⚠️"
                print(f"  {icon} {cn}: [{st}] {msg}")

if __name__ == "__main__":
    main()
