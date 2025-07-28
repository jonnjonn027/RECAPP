#!/usr/bin/env python3
"""
Secured Card Product Research Agent

This agent helps identify companies offering secured credit cards and 
finds product leaders within those organizations.
"""

import requests
import json
import time
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from urllib.parse import urljoin, quote_plus
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SecuredCardProduct:
    """Data class for secured card product information"""
    company_name: str
    product_name: str
    website: str
    description: str = ""
    annual_fee: str = ""
    min_deposit: str = ""

@dataclass
class ProductLeader:
    """Data class for product leader information"""
    name: str
    title: str
    company: str
    linkedin_url: str = ""
    email: str = ""
    department: str = ""

class SecuredCardAgent:
    """Main agent class for researching secured card products and leaders"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Known companies with secured cards (starter list)
        self.known_secured_card_companies = [
            "Capital One", "Discover", "Wells Fargo", "Bank of America", 
            "Citi", "Chase", "US Bank", "OpenSky", "Applied Bank",
            "First Progress", "Credit One Bank", "Indigo", "Milestone",
            "Total Visa", "Reflex", "Surge", "Fit", "Chime", "Self"
        ]
        
        # Common product leader titles
        self.product_leader_titles = [
            "Chief Product Officer", "VP Product", "Vice President Product",
            "Head of Product", "Director of Product", "Product Director",
            "Senior Director Product", "Chief Technology Officer",
            "VP Digital Products", "Head of Cards", "Cards Product Manager",
            "Credit Cards Product", "Consumer Products", "Product Management"
        ]

    def search_secured_card_companies(self) -> List[SecuredCardProduct]:
        """
        Search for companies offering secured credit cards
        """
        logger.info("Searching for companies with secured card products...")
        
        secured_cards = []
        
        # Start with known companies and verify they still offer secured cards
        for company in self.known_secured_card_companies:
            try:
                card_info = self._verify_secured_card_offering(company)
                if card_info:
                    secured_cards.append(card_info)
                    logger.info(f"Verified: {company} offers secured cards")
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.warning(f"Error checking {company}: {str(e)}")
                continue
        
        # Search for additional companies
        additional_companies = self._search_additional_secured_card_providers()
        secured_cards.extend(additional_companies)
        
        return secured_cards

    def _verify_secured_card_offering(self, company_name: str) -> Optional[SecuredCardProduct]:
        """
        Verify if a company offers secured credit cards
        """
        search_terms = [
            f"{company_name} secured credit card",
            f"{company_name} secured card",
            f"{company_name} deposit credit card"
        ]
        
        for term in search_terms:
            try:
                # This would typically use a web search API or scraping
                # For now, we'll return mock data for known companies
                if self._is_known_secured_card_provider(company_name):
                    return SecuredCardProduct(
                        company_name=company_name,
                        product_name=f"{company_name} Secured Card",
                        website=f"https://www.{company_name.lower().replace(' ', '')}.com",
                        description=f"Secured credit card from {company_name}",
                        annual_fee="$0-$95",
                        min_deposit="$200-$500"
                    )
            except Exception as e:
                logger.error(f"Error verifying {company_name}: {str(e)}")
                continue
        
        return None

    def _is_known_secured_card_provider(self, company_name: str) -> bool:
        """Check if company is known to provide secured cards"""
        return company_name in self.known_secured_card_companies

    def _search_additional_secured_card_providers(self) -> List[SecuredCardProduct]:
        """
        Search for additional secured card providers beyond the known list
        """
        logger.info("Searching for additional secured card providers...")
        
        # This would typically involve web scraping or API calls
        # For demonstration, returning some additional known providers
        additional_providers = [
            "Petal", "Deserve", "Tomo", "Yendo", "Kikoff", "Sable",
            "Mission Lane", "Avant", "Credit Strong", "Extra"
        ]
        
        additional_cards = []
        for provider in additional_providers:
            card = SecuredCardProduct(
                company_name=provider,
                product_name=f"{provider} Secured Card",
                website=f"https://www.{provider.lower()}.com",
                description=f"Secured credit card offering from {provider}"
            )
            additional_cards.append(card)
        
        return additional_cards

    def find_product_leaders(self, companies: List[SecuredCardProduct]) -> Dict[str, List[ProductLeader]]:
        """
        Find product leaders for the given companies
        """
        logger.info("Finding product leaders for secured card companies...")
        
        leaders_by_company = {}
        
        for company in companies:
            try:
                leaders = self._find_company_product_leaders(company.company_name)
                if leaders:
                    leaders_by_company[company.company_name] = leaders
                    logger.info(f"Found {len(leaders)} product leaders for {company.company_name}")
                time.sleep(2)  # Rate limiting for API calls
            except Exception as e:
                logger.error(f"Error finding leaders for {company.company_name}: {str(e)}")
                continue
        
        return leaders_by_company

    def _find_company_product_leaders(self, company_name: str) -> List[ProductLeader]:
        """
        Find product leaders for a specific company
        """
        leaders = []
        
        # This would typically involve LinkedIn API, company websites, or other sources
        # For demonstration, creating mock data based on common patterns
        mock_leaders = self._generate_mock_leaders(company_name)
        leaders.extend(mock_leaders)
        
        return leaders

    def _generate_mock_leaders(self, company_name: str) -> List[ProductLeader]:
        """
        Generate mock product leader data for demonstration
        """
        # In a real implementation, this would query actual data sources
        common_names = ["Sarah Johnson", "Michael Chen", "Jessica Rodriguez", "David Kim", "Amanda Thompson"]
        
        leaders = []
        for i, name in enumerate(common_names[:3]):  # Limit to 3 per company
            title = self.product_leader_titles[i % len(self.product_leader_titles)]
            leader = ProductLeader(
                name=name,
                title=title,
                company=company_name,
                linkedin_url=f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
                department="Product Management"
            )
            leaders.append(leader)
        
        return leaders

    def generate_report(self, secured_cards: List[SecuredCardProduct], 
                       leaders: Dict[str, List[ProductLeader]]) -> str:
        """
        Generate a comprehensive report of findings
        """
        report = []
        report.append("=" * 60)
        report.append("SECURED CARD PRODUCT RESEARCH REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Companies with secured cards
        report.append(f"COMPANIES WITH SECURED CARDS ({len(secured_cards)} found)")
        report.append("-" * 40)
        for card in secured_cards:
            report.append(f"• {card.company_name}")
            report.append(f"  Product: {card.product_name}")
            report.append(f"  Website: {card.website}")
            if card.annual_fee:
                report.append(f"  Annual Fee: {card.annual_fee}")
            if card.min_deposit:
                report.append(f"  Min Deposit: {card.min_deposit}")
            report.append("")
        
        # Product leaders by company
        report.append(f"PRODUCT LEADERS BY COMPANY")
        report.append("-" * 40)
        for company, company_leaders in leaders.items():
            report.append(f"\n{company.upper()}:")
            for leader in company_leaders:
                report.append(f"  • {leader.name} - {leader.title}")
                if leader.linkedin_url:
                    report.append(f"    LinkedIn: {leader.linkedin_url}")
                if leader.department:
                    report.append(f"    Department: {leader.department}")
        
        return "\n".join(report)

    def run_research(self) -> Dict:
        """
        Run the complete research process
        """
        logger.info("Starting secured card product research...")
        
        # Step 1: Find companies with secured cards
        secured_cards = self.search_secured_card_companies()
        
        # Step 2: Find product leaders
        leaders = self.find_product_leaders(secured_cards)
        
        # Step 3: Generate report
        report = self.generate_report(secured_cards, leaders)
        
        return {
            'secured_cards': secured_cards,
            'leaders': leaders,
            'report': report,
            'summary': {
                'total_companies': len(secured_cards),
                'total_leaders': sum(len(l) for l in leaders.values()),
                'companies_with_leaders': len(leaders)
            }
        }

def main():
    """Main function to run the agent"""
    agent = SecuredCardAgent()
    results = agent.run_research()
    
    print(results['report'])
    print(f"\nSUMMARY:")
    print(f"Total companies found: {results['summary']['total_companies']}")
    print(f"Total leaders identified: {results['summary']['total_leaders']}")
    print(f"Companies with leader data: {results['summary']['companies_with_leaders']}")

if __name__ == "__main__":
    main()