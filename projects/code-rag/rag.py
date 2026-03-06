#!/usr/bin/env python3
"""
Local Code RAG CLI
Lightweight code search using TF-IDF.
"""
import os
import re
import json
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class CodeRAG:
    """Local code RAG engine."""
    
    def __init__(self, index_path: str = ".code-rag.json"):
        self.index_path = index_path
        self.files: List[Dict] = []
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words=None,  # Keep code keywords
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = None
        
        if os.path.exists(index_path):
            self._load()
    
    def _load(self):
        """Load index from file."""
        with open(self.index_path, 'r') as f:
            data = json.load(f)
            self.files = data.get('files', [])
    
    def _save(self):
        """Save index to file."""
        with open(self.index_path, 'w') as f:
            json.dump({'files': self.files}, f)
    
    def _extract_code_blocks(self, content: str, max_lines: int = 100) -> List[str]:
        """Extract meaningful code blocks."""
        blocks = []
        lines = content.split('\n')
        
        current_block = []
        in_docstring = False
        
        for line in lines[:max_lines]:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
                continue
            
            # Toggle docstring detection
            if '"""' in stripped or "'''" in stripped:
                in_docstring = not in_docstring
                continue
            
            # Skip comments
            if stripped.startswith('#') or stripped.startswith('//'):
                continue
            
            current_block.append(line)
        
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return blocks
    
    def index_directory(self, path: str, extensions: List[str] = None):
        """Index a directory."""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.go', '.rs', '.java', '.cpp']
        
        path_obj = Path(path)
        self.files = []
        
        for ext in extensions:
            for filepath in path_obj.rglob(f'*{ext}'):
                # Skip common directories
                if any(x in filepath.parts for x in ['node_modules', '.git', 'venv', '__pycache__']):
                    continue
                
                try:
                    # Skip large files
                    if filepath.stat().st_size > 1_000_000:
                        continue
                    
                    content = filepath.read_text(errors='ignore')
                    blocks = self._extract_code_blocks(content)
                    
                    for i, block in enumerate(blocks):
                        if len(block.strip()) < 20:  # Skip tiny blocks
                            continue
                        
                        self.files.append({
                            'path': str(filepath),
                            'block_id': i,
                            'content': block,
                            'language': ext[1:]
                        })
                
                except Exception:
                    continue
        
        # Build TF-IDF index
        if self.files:
            texts = [f['content'] for f in self.files]
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        self._save()
        return len(self.files)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search the indexed code."""
        if not self.files or self.tfidf_matrix is None:
            return []
        
        # Transform query
        query_vec = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        
        # Get top-k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.05:
                result = self.files[idx].copy()
                result['score'] = float(similarities[idx])
                results.append(result)
        
        return results


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Local Code RAG CLI')
    subparsers = parser.add_subparsers()
    
    # index command
    index_parser = subparsers.add_parser('index', help='Index a directory')
    index_parser.add_argument('path', help='Directory to index')
    index_parser.add_argument('--extensions', nargs='+', 
                             default=['.py', '.js', '.ts', '.go', '.rs'],
                             help='File extensions to index')
    
    # search command
    search_parser = subparsers.add_parser('search', help='Search code')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--top-k', type=int, default=5, help='Max results')
    search_parser.add_argument('--context', type=int, default=3, help='Lines of context')
    
    args = parser.parse_args()
    
    rag = CodeRAG()
    
    if hasattr(args, 'path'):
        # Index
        print(f"Indexing {args.path}...")
        count = rag.index_directory(args.path, args.extensions)
        print(f"Indexed {count} code blocks")
    
    elif hasattr(args, 'query'):
        # Search
        results = rag.search(args.query, args.top_k)
        
        if not results:
            print("No results found.")
            return
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['path']}:{result['block_id']}")
            print(f"   Score: {result['score']:.3f}")
            
            # Show context
            lines = result['content'].split('\n')[:args.context]
            for line in lines:
                print(f"   {line}")


if __name__ == '__main__':
    main()
