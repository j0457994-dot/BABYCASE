import random
import base64
from typing import str
import re

class EvasionService:
    """MIT-Level: Multi-layer detection evasion"""
    
    @staticmethod
    def apply_stealth(html_content: str, level: str = "medium") -> str:
        """
        Apply multiple evasion techniques based on difficulty level
        Levels: easy, medium, hard, expert
        """
        if level == "easy":
            return EvasionService._basic_evasion(html_content)
        elif level == "medium":
            return EvasionService._intermediate_evasion(html_content)
        elif level == "hard":
            return EvasionService._advanced_evasion(html_content)
        else:  # expert
            return EvasionService._expert_evasion(html_content)
    
    @staticmethod
    def _basic_evasion(content: str) -> str:
        """Basic homoglyph and character substitution"""
        replacements = {
            'o': 'ο', 'a': 'а', 'e': 'е', 
            'p': 'ρ', 'c': 'ϲ', 'x': 'х'
        }
        
        mutated = list(content)
        for i, char in enumerate(mutated):
            if char in replacements and random.random() < 0.02:
                mutated[i] = replacements[char]
        
        return ''.join(mutated)
    
    @staticmethod
    def _intermediate_evasion(content: str) -> str:
        """Add invisible characters and HTML comments"""
        # Zero-width characters
        zwj = "\u200d"  # Zero-width joiner
        zwnj = "\u200c"  # Zero-width non-joiner
        
        # Insert invisible characters randomly
        content = content.replace(" ", f"{zwj} {zwnj}")
        
        # Add HTML comments with random noise
        noise = base64.b64encode(random.randbytes(16)).decode()
        content += f"<!--{noise}-->"
        
        return content
    
    @staticmethod
    def _advanced_evasion(content: str) -> str:
        """CSS injection + encoded payloads"""
        # Encode email addresses using HTML entities
        def encode_email(text: str) -> str:
            return ''.join(f'&#{ord(c)};' if c in '@.' else c for c in text)
        
        # Add invisible tracking bypass
        content = re.sub(
            r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            lambda m: encode_email(m.group(0)),
            content
        )
        
        # CSS cloaking
        cloaked_css = """
        <style>
        .spam-trigger { display: none !important; visibility: hidden !important; }
        .real-content { display: block !important; }
        </style>
        """
        
        return cloaked_css + content
    
    @staticmethod
    def _expert_evasion(content: str) -> str:
        """Harvard-level: Polymorphic mutation + IP rotation hints"""
        # Multiple encoding layers
        encoded = base64.b64encode(content.encode()).decode()
        
        # Create polymorphic template
        template = f"""
        <div style="display:none">MIME-Version: 1.0</div>
        <div data-enc="{encoded[:50]}"></div>
        <div class="content">
            {content}
        </div>
        <div style="display:none">Content-Transfer-Encoding: 7bit</div>
        """
        
        # Add random delays and formatting
        return template.replace("\n", f"\n{random.choice([' ', '  ', '\t'])}")
    
    @staticmethod
    def mutate_subject(subject: str, level: str = "medium") -> str:
        """Apply evasion to email subject lines"""
        prefixes = ["Re:", "Fwd:", "📎", "✅", "⚠️"]
        
        if level in ["hard", "expert"]:
            # Add conversation threading indicators
            subject = f"{random.choice(prefixes)} {subject}"
            subject = subject.replace("Invoice", "Payment Receipt")
            subject = subject.replace("Security", "Account Verification")
        
        return EvasionService.apply_stealth(subject, level)[:200]  # Limit length