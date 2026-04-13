import httpx
import asyncio
from typing import Dict, Optional
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models import schemas
import logging
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)

class OSINTService:
    def __init__(self, db: Session = None):
        self.hunter_key = settings.HUNTER_API_KEY
        self.db = db
        
    async def enrich_target(self, target_id: int, deep_scan: bool = False):
        """Harvard-Level: Multi-source intelligence gathering"""
        if not self.db:
            return None
            
        target = self.db.query(schemas.Target).filter(schemas.Target.id == target_id).first()
        if not target:
            return None
        
        # Parallel OSINT collection
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = []
            tasks.append(self._fetch_hunter_data(client, target.domain))
            tasks.append(self._fetch_tech_stack(client, target.domain))
            
            if deep_scan:
                tasks.append(self._fetch_linkedin_data(client, target.company_name))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return target
    
    async def _fetch_hunter_data(self, client, domain: str) -> Dict:
        """Extract email patterns and C-Suite contacts"""
        try:
            url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={self.hunter_key}"
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "pattern": data.get("data", {}).get("pattern"),
                    "emails": data.get("data", {}).get("emails", []),
                }
        except Exception as e:
            logger.error(f"Hunter.io error: {e}")
        return {}
    
    async def _fetch_tech_stack(self, client, domain: str) -> Dict:
        """Identify technologies used by target"""
        try:
            response = await client.get(f"https://{domain}")
            techs = []
            
            if re.search(r'wp-content|wordpress', response.text, re.I):
                techs.append("WordPress")
            if re.search(r'react|next\.js', response.text, re.I):
                techs.append("React")
                
            return {"technologies": techs}
        except:
            return {"technologies": []}
    
    async def _fetch_linkedin_data(self, client, company_name: str) -> Dict:
        """Placeholder for LinkedIn scraping"""
        return {"linkedin": "not_implemented"}
    
    async def get_complete_dossier(self, target: schemas.Target) -> Dict:
        """Generate comprehensive intelligence report"""
        return {
            "company": {
                "name": target.company_name,
                "domain": target.domain,
                "industry": target.industry,
                "size": target.employee_count,
            },
            "c_suite": {
                "ceo": {"name": target.ceo_name, "email": target.ceo_email},
                "cfo": {"name": target.cfo_name, "email": target.cfo_email},
            },
            "risk_score": target.risk_score
        }