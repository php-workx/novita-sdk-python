#!/usr/bin/env python3
"""Analyze test coverage gaps in the Novita SDK."""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

def extract_methods(file_path: Path) -> Tuple[List[str], List[str]]:
    """Extract sync and async methods from a resource file."""
    content = file_path.read_text()

    # Find methods in the sync class
    sync_pattern = r'class \w+\(BaseResource\):.*?(?=class |\Z)'
    sync_match = re.search(sync_pattern, content, re.DOTALL)
    sync_methods = []
    if sync_match:
        sync_content = sync_match.group(0)
        sync_methods = re.findall(r'^\s{4}def (\w+)\(', sync_content, re.MULTILINE)

    # Find methods in the async class
    async_pattern = r'class \w+\(AsyncBaseResource\):.*?(?=\Z)'
    async_match = re.search(async_pattern, content, re.DOTALL)
    async_methods = []
    if async_match:
        async_content = async_match.group(0)
        async_methods = re.findall(r'^\s{4}async def (\w+)\(', async_content, re.MULTILINE)

    return sync_methods, async_methods


def extract_tests(file_path: Path, resource_name: str) -> Tuple[Set[str], Set[str]]:
    """Extract sync and async tested method names for a resource from a test file."""
    if not file_path.exists():
        return set(), set()

    content = file_path.read_text()
    call_pattern = rf'\bgpu\.{resource_name}\.(\w+)\('
    sync_calls: Set[str] = set()
    async_calls: Set[str] = set()

    for match in re.finditer(call_pattern, content):
        method = match.group(1)
        line_start = content.rfind("\n", 0, match.start()) + 1
        line_prefix = content[line_start:match.start()]
        if "await" in line_prefix:
            async_calls.add(method)
        else:
            sync_calls.add(method)

    return sync_calls, async_calls


def analyze_resource(resource_name: str, src_dir: Path, test_dir: Path) -> Dict:
    """Analyze coverage for a specific resource."""
    src_file = src_dir / f"{resource_name}.py"
    test_file = test_dir / f"test_gpu_{resource_name}.py"

    if not src_file.exists():
        return {}

    sync_methods, async_methods = extract_methods(src_file)
    tested_sync, tested_async = extract_tests(test_file, resource_name)

    # Find what's covered and what's missing
    all_methods = set(sync_methods)
    missing_sync = all_methods - tested_sync

    missing_async = set(async_methods) - tested_async

    return {
        'sync_methods': sync_methods,
        'async_methods': async_methods,
        'tested_sync': tested_sync,
        'tested_async': tested_async,
        'missing_sync': sorted(missing_sync),
        'missing_async': sorted(missing_async),
        'test_count': len(tested_sync | tested_async),
    }


def main():
    """Run the coverage analysis."""
    base = Path(__file__).resolve().parent
    src_dir = base / 'src/novita/api/resources/gpu'
    test_dir = base / 'tests/unit'

    resources = [
        'clusters', 'endpoints', 'images', 'instances',
        'jobs', 'metrics', 'networks', 'products',
        'registries', 'storages', 'templates'
    ]

    print("=" * 80)
    print("NOVITA SDK TEST COVERAGE ANALYSIS")
    print("=" * 80)

    total_methods = 0
    total_tested = 0
    total_missing = 0

    for resource in resources:
        result = analyze_resource(resource, src_dir, test_dir)
        if not result:
            continue

        print(f"\n{'=' * 80}")
        print(f"Resource: {resource.upper()}")
        print(f"{'=' * 80}")
        print(f"Total sync methods: {len(result['sync_methods'])}")
        print(f"Total async methods: {len(result['async_methods'])}")
        print(f"Tests written: {result['test_count']}")

        total_methods += len(result['sync_methods'])
        total_tested += result['test_count']

        if result['missing_sync']:
            print(f"\nMISSING SYNC TESTS ({len(result['missing_sync'])}):")
            for method in result['missing_sync']:
                print(f"  - {method}()")
                total_missing += 1

        if result['missing_async']:
            print(f"\nMISSING ASYNC TESTS ({len(result['missing_async'])}):")
            for method in result['missing_async']:
                print(f"  - async {method}()")

    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total methods across all resources: {total_methods}")
    print(f"Total unique tests: {total_tested}")
    print(f"Missing sync method tests: {total_missing}")
    print(f"Coverage: {(total_tested / total_methods * 100) if total_methods > 0 else 0:.1f}%")


if __name__ == '__main__':
    main()
