#!/usr/bin/env python3
"""
AI Tool Security Scanner v2
Enhanced security scanner for AI development tools.
"""
import os
import re
import json
import yaml
import sys
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse


class SecurityScanner:
    """Scan AI tools for security issues."""
    
    # Common typosquatting patterns
    TYPOSQUATTING_PATTERNS = {
        'npm': ['req', 'npmm', 'npx', 'node_moduels'],
        'pip': ['pip3', 'pipx', 'pyptron'],
        'git': ['githb', 'gihub', 'githu'],
    }
    
    # Known malicious package patterns (typosquatted popular packages)
    SUSPICIOUS_PACKAGES = {
        'npm': ['pyton', 'pythn', 'node_modules', 'npms', 'yarnpkg'],
    }
    
    # Prompt injection patterns
    PROMPT_INJECTION_PATTERNS = [
        r'ignore\s+(previous|above|all)\s+(instructions?|rules?|commands?)',
        r'(system|You\s+are).*role.*=',
        r'<\|.*\|>',  # Prompt injection tags
        r'\[\[.*\]\]',  # Jailbreak markers
    ]
    
    def __init__(self):
        self.issues: List[Dict] = []
        
    def add_issue(self, file: str, line: int, severity: str, message: str):
        """Add a security issue."""
        self.issues.append({
            "file": file,
            "line": line,
            "severity": severity,
            "message": message
        })
    
    def scan_file(self, path: str) -> List[Dict]:
        """Scan a single file."""
        self.issues = []
        
        if not os.path.exists(path):
            print(f"Error: {path} does not exist")
            return []
        
        # Detect file type and scan
        if path.endswith('.yml') or path.endswith('.yaml'):
            self._scan_github_actions(path)
        elif path.endswith('package.json'):
            self._scan_package_json(path)
        elif path.endswith('.py'):
            self._scan_python(path)
        elif path.endswith('.js') or path.endswith('.ts'):
            self._scan_js(path)
        
        return self.issues
    
    def _scan_github_actions(self, path: str):
        """Scan GitHub Actions workflow."""
        try:
            with open(path, 'r') as f:
                workflow = yaml.safe_load(f)
            
            if not workflow:
                return
            
            # Check for external actions
            if 'jobs' in workflow:
                for job_name, job in workflow['jobs'].items():
                    if 'steps' in job:
                        for i, step in enumerate(job['steps']):
                            if 'uses' in step:
                                action = step['uses']
                                # Check for external/untrusted actions
                                if action.startswith('github/') or action.startswith('actions/'):
                                    pass  # Known trusted sources
                                elif '@' in action:
                                    self.add_issue(
                                        path, i + 1, 'WARNING',
                                        f"External action: {action}"
                                    )
                            
                            # Check for secrets in logs
                            if 'run' in step:
                                if 'secrets.' in step['run'] or '${{ secrets.' in str(step):
                                    self.add_issue(
                                        path, i + 1, 'WARNING',
                                        "Potential secret exposure in logs"
                                    )
                            
                            # Check for cache usage (cache poisoning vulnerability)
                            if 'uses' in step and 'cache' in step['uses']:
                                self.add_issue(
                                    path, i + 1, 'WARNING',
                                    "Cache usage detected - ensure cache keys are versioned and secure"
                                )
            
            # Check for permissions
            if 'permissions' in workflow:
                perms = workflow['permissions']
                # Check for overly broad permissions
                if perms.get('contents') == 'write':
                    self.add_issue(
                        path, 0, 'WARNING',
                        "Workflow has write access to contents - ensure only trusted actions use this"
                    )
                if perms.get('packages') == 'write' or perms.get('id-token') == 'write':
                    self.add_issue(
                        path, 0, 'HIGH',
                        "Workflow has elevated permissions (packages or id-token write)"
                    )
            
            # Check trigger sources
            # Note: 'on' is parsed as boolean True in YAML, so check both
            if 'on' in workflow or True in workflow:
                triggers = workflow.get('on') or workflow.get(True)
                # Handle both dict and list formats
                trigger_list = []
                if isinstance(triggers, dict):
                    trigger_list = list(triggers.keys())
                elif isinstance(triggers, list):
                    trigger_list = triggers
                
                for trigger in trigger_list:
                    if trigger in ['issues', 'issue_comment', 'pull_request', 'issue', 'pull_request']:
                        self.add_issue(
                            path, 0, 'INFO',
                            f"External trigger: {trigger} (ensure input validation - vulnerable to prompt injection)"
                        )
                    if trigger in ['workflow_dispatch', 'repository_dispatch', 'workflow_dispatch']:
                        self.add_issue(
                            path, 0, 'INFO',
                            f"Manual trigger: {trigger} (can be triggered externally)"
                        )
                            
        except Exception as e:
            print(f"Error scanning {path}: {e}")
    
    def _scan_package_json(self, path: str):
        """Scan npm package.json."""
        try:
            with open(path, 'r') as f:
                pkg = json.load(f)
            
            # Check for postinstall scripts
            if 'scripts' in pkg:
                scripts = pkg['scripts']
                if 'postinstall' in scripts:
                    self.add_issue(
                        path, 0, 'HIGH',
                        f"postinstall script detected: {scripts['postinstall']}"
                    )
                if 'preinstall' in scripts:
                    self.add_issue(
                        path, 0, 'HIGH',
                        f"preinstall script detected: {scripts['preinstall']}"
                    )
            
            # Check dependencies
            if 'dependencies' in pkg:
                all_deps = list(pkg.get('dependencies', {}).keys())
                all_deps.extend(list(pkg.get('devDependencies', {}).keys()))
                
                for dep in all_deps:
                    # Check for typosquatting
                    for pkg_manager, typos in self.TYPOSQUATTING_PATTERNS.items():
                        if dep.lower() in typos:
                            self.add_issue(
                                path, 0, 'WARNING',
                                f"Suspicious dependency (possible typosquatting): {dep}"
                            )
                    
                    # Check for known suspicious packages
                    for pkg_manager, suspicious in self.SUSPICIOUS_PACKAGES.items():
                        if dep.lower() in suspicious:
                            self.add_issue(
                                path, 0, 'HIGH',
                                f"Known suspicious package: {dep}"
                            )
                            
        except Exception as e:
            print(f"Error scanning {path}: {e}")
    
    def _scan_python(self, path: str):
        """Scan Python files for prompt injection."""
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                # Check for f-string with external input (prompt injection vulnerability)
                if 'f"' in line or "f'" in line:
                    # Check for common external input sources
                    external_inputs = ['request', 'input', 'issue', 'user', 'query', 'param', 'args']
                    if any(x in line.lower() for x in external_inputs):
                        self.add_issue(
                            path, i, 'WARNING',
                            "Possible prompt injection: f-string with external input"
                        )
                
                # Check for exec/eval with external input
                if 'exec(' in line or 'eval(' in line:
                    if 'request' in line or 'input' in line or 'issue' in line:
                        self.add_issue(
                            path, i, 'HIGH',
                            "Potential code injection: exec/eval with external input"
                        )
                
                # Check prompt injection patterns
                for pattern in self.PROMPT_INJECTION_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.add_issue(
                            path, i, 'WARNING',
                            f"Potential prompt injection pattern: {pattern}"
                        )
                            
        except Exception as e:
            print(f"Error scanning {path}: {e}")
    
    def _scan_js(self, path: str):
        """Scan JavaScript/TypeScript files."""
        try:
            with open(path, 'r') as f:
                content = f.read()
            
            # Check for eval with external input
            if 'eval(' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'eval(' in line:
                        self.add_issue(
                            path, i, 'HIGH',
                            "Potential code injection: eval() with external input"
                        )
            
            # Check for process.env with secrets
            if 'process.env' in content and 'SECRET' in content.upper():
                self.add_issue(
                    path, 0, 'WARNING',
                    "Potential secret exposure via process.env"
                )
                            
        except Exception as e:
            print(f"Error scanning {path}: {e}")
    
    def scan_directory(self, path: str) -> List[Dict]:
        """Scan a directory recursively."""
        self.issues = []
        path_obj = Path(path)
        
        # Scan GitHub workflows
        workflow_dir = path_obj / '.github' / 'workflows'
        if workflow_dir.exists():
            for f in workflow_dir.glob('*.yml'):
                self.scan_file(str(f))
            for f in workflow_dir.glob('*.yaml'):
                self.scan_file(str(f))
        
        # Scan package.json
        if (path_obj / 'package.json').exists():
            self.scan_file(str(path_obj / 'package.json'))
        
        # Scan Python files
        for f in path_obj.rglob('*.py'):
            if any(x in f.parts for x in ['venv', '.venv', 'env', 'node_modules', '.git']):
                continue
            self.scan_file(str(f))
        
        # Scan JS/TS files
        for ext in ['*.js', '*.ts', '*.jsx', '*.tsx']:
            for f in path_obj.rglob(ext):
                if any(x in f.parts for x in ['node_modules', '.git']):
                    continue
                self.scan_file(str(f))
        
        # Scan .env files (should not be committed)
        for f in path_obj.rglob('.env*'):
            if '.git' not in f.parts:
                self.add_issue(
                    str(f), 0, 'HIGH',
                    ".env file detected - should not be committed to version control"
                )
        
        # Scan shell scripts for secrets
        for f in path_obj.rglob('*.sh'):
            if any(x in f.parts for x in ['.git', 'node_modules']):
                continue
            try:
                with open(f, 'r') as fh:
                    content = fh.read()
                    # Check for hardcoded secrets
                    if any(x in content for x in ['API_KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                        if any(x in content for x in ['=', ':=']):
                            self.add_issue(
                                str(f), 0, 'WARNING',
                                "Possible hardcoded secrets in shell script"
                            )
            except:
                pass
        
        # Scan Dockerfiles for security issues
        for f in path_obj.rglob('Dockerfile*'):
            if '.git' not in f.parts:
                try:
                    with open(f, 'r') as fh:
                        content = fh.read()
                        lines = content.split('\n')
                        
                        # Check for running as root
                        if 'USER root' in content or 'USER 0' in content:
                            self.add_issue(
                                str(f), 0, 'WARNING',
                                "Container runs as root user - consider using non-root user"
                            )
                        
                        # Check for latest tag
                        if 'FROM' in content and 'latest' in content:
                            self.add_issue(
                                str(f), 0, 'WARNING',
                                "Using 'latest' tag - specify version for reproducibility"
                            )
                        
                        # Check for ADD instead of COPY
                        if 'ADD ' in content and 'COPY ' not in content:
                            self.add_issue(
                                str(f), 0, 'INFO',
                                "Using ADD - prefer COPY for better caching"
                            )
                        
                        # Check for exposed secrets
                        if any(x in content for x in ['API_KEY', 'SECRET', 'PASSWORD']):
                            if 'ENV' in content:
                                self.add_issue(
                                    str(f), 0, 'HIGH',
                                    "Possible hardcoded secrets in ENV instructions"
                                )
                except:
                    pass
        
        # Scan docker-compose files
        for f in path_obj.rglob('docker-compose*.yml'):
            if '.git' not in f.parts:
                try:
                    with open(f, 'r') as fh:
                        content = fh.read()
                        
                        # Check for hardcoded secrets in environment
                        if any(x in content for x in ['SECRET', 'PASSWORD', 'API_KEY', 'TOKEN']):
                            self.add_issue(
                                str(f), 0, 'WARNING',
                                "Possible hardcoded secrets in docker-compose environment"
                            )
                        
                        # Check for latest tags
                        if 'latest' in content:
                            self.add_issue(
                                str(f), 0, 'WARNING',
                                "Using 'latest' tag - specify version for reproducibility"
                            )
                except:
                    pass
        
        return self.issues


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Tool Security Scanner v2')
    parser.add_argument('path', help='Path to scan (file or directory)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--strict', action='store_true', help='Enable strict mode')
    
    args = parser.parse_args()
    
    scanner = SecurityScanner()
    
    if os.path.isfile(args.path):
        issues = scanner.scan_file(args.path)
    elif os.path.isdir(args.path):
        issues = scanner.scan_directory(args.path)
    else:
        print(f"Error: {args.path} does not exist")
        sys.exit(1)
    
    # Output
    if args.json:
        print(json.dumps(issues, indent=2))
    else:
        if not issues:
            print("No issues found.")
            return
        
        # Group by file
        by_file = {}
        for issue in issues:
            f = issue['file']
            if f not in by_file:
                by_file[f] = []
            by_file[f].append(issue)
        
        for file_path, file_issues in by_file.items():
            print(f"\n[{file_path}]")
            for issue in file_issues:
                line_info = f"Line {issue['line']}" if issue['line'] else ""
                print(f"  [{issue['severity']}] {line_info} {issue['message']}")
        
        print(f"\n{len(issues)} issue(s) found.")


if __name__ == '__main__':
    main()
