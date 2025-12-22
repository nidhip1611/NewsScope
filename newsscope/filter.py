"""
Numeric Grounding Filter for NewsScope
"""

import re
from typing import Tuple, List, Set


class NumericGroundingFilter:
    """
    Checks if numbers in generated claims are grounded in the source article.
    """
    
    def __init__(self):
        self.number_patterns = [
            r'\b\d+\.?\d*%',           # Percentages
            r'\$\d+[\d,]*\.?\d*',      # Dollar amounts
            r'\b\d{1,3}(?:,\d{3})+\b',  # Numbers with commas
            r'\b\d+\.?\d*\s*(?:million|billion|trillion)\b',  # Large numbers
            r'\b\d+\.?\d*\b',          # Plain numbers
        ]
    
    def extract_numbers(self, text: str) -> Set[str]:
        """Extract all numbers from text."""
        if not text:
            return set()
        
        numbers = set()
        text_lower = text.lower()
        
        for pattern in self.number_patterns:
            matches = re.findall(pattern, text_lower)
            numbers.update(matches)
        
        return numbers
    
    def check(self, claim: str, article: str) -> Tuple[bool, List[str]]:
        """
        Check if all numbers in claim appear in article.
        
        Returns:
            (is_grounded, ungrounded_numbers)
        """
        claim_numbers = self.extract_numbers(claim)
        
        if not claim_numbers:
            return True, []
        
        article_numbers = self.extract_numbers(article)
        ungrounded = []
        
        for num in claim_numbers:
            # Extract core digits for comparison
            core_digits = re.sub(r'[^\d.]', '', num)
            
            found = False
            for article_num in article_numbers:
                article_digits = re.sub(r'[^\d.]', '', article_num)
                if core_digits == article_digits:
                    found = True
                    break
            
            if not found:
                ungrounded.append(num)
        
        return len(ungrounded) == 0, ungrounded


def filter_claims(claims: List[dict], article: str) -> List[dict]:
    """
    Filter claims to keep only those with grounded numbers.
    """
    filter = NumericGroundingFilter()
    grounded_claims = []
    
    for claim in claims:
        claim_text = claim.get("claim_text", "")
        is_grounded, _ = filter.check(claim_text, article)
        
        if is_grounded:
            grounded_claims.append(claim)
    
    return grounded_claims
