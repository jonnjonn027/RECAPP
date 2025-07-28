#!/usr/bin/env python3
"""
Enhanced Secured Card Product Research Agent

This enhanced version includes real web search capabilities and 
integration options for LinkedIn and other professional networks.
"""

import requests
import json
import time
import re
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, quote_plus
import logging
from bs4 import BeautifulSoup
import csv

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
    apr_range: str = ""
    credit_bureau_reporting: str = ""
    graduation_possible: str = ""

@dataclass
class ProductLeader:
    """Data class for product leader information"""
    name: str
    title: str
    company: str
    linkedin_url: str = ""
    email: str = ""
    department: str = ""
    location: str = ""
    experience_years: str = ""
    previous_companies: List[str] = None

    def __post_init__(self):
        if self.previous_companies is None:
            self.previous_companies = []

class EnhancedSecuredCardAgent:
    """Enhanced agent with real data source integration"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # API keys (would be loaded from environment or config)
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.linkedin_api_key = os.getenv('LINKEDIN_API_KEY')
        
        # Enhanced list of known secured card companies
        self.known_secured_card_companies = [
            # Major Banks
            "Capital One", "Discover", "Wells Fargo", "Bank of America", 
            "Citi", "Chase", "US Bank", "PNC Bank", "Truist", "TD Bank",
            
            # Credit Card Specialists
            "OpenSky", "Applied Bank", "First Progress", "Credit One Bank", 
            "Indigo", "Milestone", "Total Visa", "Reflex", "Surge", "Fit",
            
            # Fintech Companies
            "Chime", "Self", "Petal", "Deserve", "Tomo", "Yendo", 
            "Kikoff", "Sable", "Mission Lane", "Avant", "Credit Strong", 
            "Extra", "Sesame Cash", "MoneyLion", "Grow Credit",
            
            # Regional Banks
            "Navy Federal", "USAA", "Alliant Credit Union", "Pentagon Federal",
            "First Tech Federal Credit Union", "Golden 1 Credit Union"
        ]
        
        # Comprehensive product leader titles
        self.product_leader_titles = [
            "Chief Product Officer", "CPO", "VP Product", "Vice President Product",
            "Head of Product", "Director of Product", "Product Director",
            "Senior Director Product", "Principal Product Manager",
            "VP Digital Products", "Head of Cards", "Cards Product Manager",
            "Credit Cards Product", "Consumer Products", "Product Management",
            "Chief Technology Officer", "CTO", "VP Technology",
            "Head of Digital", "Digital Product Leader", "VP Consumer Banking",
            "Head of Consumer Lending", "Director of Card Products",
            "Senior Product Manager", "Lead Product Manager"
        ]

    def search_web_for_secured_cards(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search the web for secured card information using Google Custom Search API
        """
        if not self.google_api_key or not self.google_search_engine_id:
            logger.warning("Google API credentials not available, using fallback method")
            return self._fallback_web_search(query)
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.google_search_engine_id,
                'q': query,
                'num': num_results
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            results = response.json()
            return results.get('items', [])
            
        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            return self._fallback_web_search(query)

    def _fallback_web_search(self, query: str) -> List[Dict]:
        """
        Fallback web search method using DuckDuckGo or similar
        """
        # This would implement a fallback search method
        # For now, returning empty list
        logger.info(f"Using fallback search for: {query}")
        return []

    def discover_secured_card_companies(self) -> List[SecuredCardProduct]:
        """
        Discover companies offering secured credit cards through web search
        """
        logger.info("Discovering secured card companies through web search...")
        
        search_queries = [
            "best secured credit cards 2024",
            "secured credit card companies list",
            "secured credit cards for bad credit",
            "deposit credit cards providers",
            "secured credit card comparison"
        ]
        
        discovered_companies = set()
        
        for query in search_queries:
            try:
                results = self.search_web_for_secured_cards(query)
                companies = self._extract_companies_from_search(results)
                discovered_companies.update(companies)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error searching for '{query}': {str(e)}")
                continue
        
        # Combine with known companies
        all_companies = list(discovered_companies) + self.known_secured_card_companies
        unique_companies = list(set(all_companies))
        
        # Get detailed information for each company
        secured_cards = []
        for company in unique_companies:
            try:
                card_info = self._get_detailed_card_info(company)
                if card_info:
                    secured_cards.append(card_info)
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                logger.warning(f"Error getting details for {company}: {str(e)}")
                continue
        
        return secured_cards

    def _extract_companies_from_search(self, search_results: List[Dict]) -> List[str]:
        """
        Extract company names from search results
        """
        companies = []
        
        for result in search_results:
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            
            # Look for company names in title and snippet
            text = f"{title} {snippet}".lower()
            
            # Extract potential company names using patterns
            company_patterns = [
                r'(\w+\s*bank)',
                r'(\w+\s*credit union)',
                r'(\w+\s*financial)',
                r'(capital one|discover|chase|citi|wells fargo)',
                r'(\w+\s*card)',
            ]
            
            for pattern in company_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    company = match.strip().title()
                    if len(company) > 2 and company not in companies:
                        companies.append(company)
        
        return companies

    def _get_detailed_card_info(self, company_name: str) -> Optional[SecuredCardProduct]:
        """
        Get detailed information about a company's secured card offering
        """
        try:
            # Search for specific card information
            query = f"{company_name} secured credit card details annual fee deposit"
            search_results = self.search_web_for_secured_cards(query, num_results=5)
            
            if not search_results:
                # Use known company data
                return self._get_known_company_info(company_name)
            
            # Extract card details from search results
            card_info = self._parse_card_details(search_results, company_name)
            return card_info
            
        except Exception as e:
            logger.error(f"Error getting card details for {company_name}: {str(e)}")
            return self._get_known_company_info(company_name)

    def _get_known_company_info(self, company_name: str) -> Optional[SecuredCardProduct]:
        """
        Get information for known companies
        """
        if company_name in self.known_secured_card_companies:
            return SecuredCardProduct(
                company_name=company_name,
                product_name=f"{company_name} Secured Card",
                website=f"https://www.{company_name.lower().replace(' ', '').replace('bank', '').replace('creditunion', 'cu')}.com",
                description=f"Secured credit card from {company_name}",
                annual_fee="$0-$95",
                min_deposit="$200-$500",
                apr_range="18.99%-26.99%",
                credit_bureau_reporting="All 3 bureaus",
                graduation_possible="Yes"
            )
        return None

    def _parse_card_details(self, search_results: List[Dict], company_name: str) -> SecuredCardProduct:
        """
        Parse card details from search results
        """
        # This would implement sophisticated parsing of search results
        # For now, returning basic info
        return SecuredCardProduct(
            company_name=company_name,
            product_name=f"{company_name} Secured Card",
            website=search_results[0].get('link', '') if search_results else '',
            description=search_results[0].get('snippet', '') if search_results else '',
            annual_fee="Varies",
            min_deposit="Varies"
        )

    def find_product_leaders_advanced(self, companies: List[SecuredCardProduct]) -> Dict[str, List[ProductLeader]]:
        """
        Advanced product leader search using multiple sources
        """
        logger.info("Finding product leaders using advanced search methods...")
        
        leaders_by_company = {}
        
        for company in companies:
            try:
                leaders = []
                
                # Method 1: LinkedIn search (if API available)
                linkedin_leaders = self._search_linkedin_leaders(company.company_name)
                leaders.extend(linkedin_leaders)
                
                # Method 2: Company website search
                website_leaders = self._search_company_website(company.website)
                leaders.extend(website_leaders)
                
                # Method 3: Professional network search
                network_leaders = self._search_professional_networks(company.company_name)
                leaders.extend(network_leaders)
                
                # Remove duplicates and filter
                unique_leaders = self._deduplicate_leaders(leaders)
                
                if unique_leaders:
                    leaders_by_company[company.company_name] = unique_leaders
                    logger.info(f"Found {len(unique_leaders)} leaders for {company.company_name}")
                
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error finding leaders for {company.company_name}: {str(e)}")
                continue
        
        return leaders_by_company

    def _search_linkedin_leaders(self, company_name: str) -> List[ProductLeader]:
        """
        Search for product leaders on LinkedIn
        """
        if not self.linkedin_api_key:
            logger.info(f"LinkedIn API not available, using web search for {company_name}")
            return self._search_linkedin_web(company_name)
        
        # LinkedIn API search would go here
        return []

    def _search_linkedin_web(self, company_name: str) -> List[ProductLeader]:
        """
        Search LinkedIn through web search
        """
        leaders = []
        
        for title in self.product_leader_titles[:5]:  # Limit searches
            query = f"site:linkedin.com {company_name} \"{title}\""
            try:
                results = self.search_web_for_secured_cards(query, num_results=3)
                parsed_leaders = self._parse_linkedin_results(results, company_name)
                leaders.extend(parsed_leaders)
                time.sleep(1)
            except Exception as e:
                logger.warning(f"LinkedIn search failed for {company_name} {title}: {str(e)}")
                continue
        
        return leaders

    def _parse_linkedin_results(self, results: List[Dict], company_name: str) -> List[ProductLeader]:
        """
        Parse LinkedIn profile information from search results
        """
        leaders = []
        
        for result in results:
            try:
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                link = result.get('link', '')
                
                # Extract name and title from LinkedIn result
                name_match = re.search(r'([A-Za-z\s]+)\s*-\s*([^|]+)', title)
                if name_match:
                    name = name_match.group(1).strip()
                    job_title = name_match.group(2).strip()
                    
                    leader = ProductLeader(
                        name=name,
                        title=job_title,
                        company=company_name,
                        linkedin_url=link,
                        department="Product Management"
                    )
                    leaders.append(leader)
                    
            except Exception as e:
                logger.warning(f"Error parsing LinkedIn result: {str(e)}")
                continue
        
        return leaders

    def _search_company_website(self, website: str) -> List[ProductLeader]:
        """
        Search company website for leadership information
        """
        if not website:
            return []
        
        try:
            # Look for leadership/team pages
            leadership_urls = [
                f"{website}/leadership",
                f"{website}/team",
                f"{website}/about/leadership",
                f"{website}/company/leadership",
                f"{website}/about-us/team"
            ]
            
            leaders = []
            for url in leadership_urls:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        page_leaders = self._extract_leaders_from_page(soup, website)
                        leaders.extend(page_leaders)
                        break  # Found a working leadership page
                except Exception as e:
                    continue
            
            return leaders
            
        except Exception as e:
            logger.warning(f"Error searching company website {website}: {str(e)}")
            return []

    def _extract_leaders_from_page(self, soup: BeautifulSoup, company_name: str) -> List[ProductLeader]:
        """
        Extract leader information from a company webpage
        """
        leaders = []
        
        # Look for common patterns in leadership pages
        leadership_selectors = [
            '.leadership-team .member',
            '.team-member',
            '.executive',
            '.leader',
            '.bio'
        ]
        
        for selector in leadership_selectors:
            members = soup.select(selector)
            for member in members:
                try:
                    name = self._extract_name(member)
                    title = self._extract_title(member)
                    
                    if name and title and any(keyword in title.lower() for keyword in ['product', 'cto', 'cpo', 'digital']):
                        leader = ProductLeader(
                            name=name,
                            title=title,
                            company=company_name,
                            department="Product Management"
                        )
                        leaders.append(leader)
                        
                except Exception as e:
                    continue
        
        return leaders

    def _extract_name(self, element) -> str:
        """Extract name from HTML element"""
        name_selectors = ['.name', '.title', 'h3', 'h4', '.member-name']
        for selector in name_selectors:
            name_elem = element.select_one(selector)
            if name_elem:
                return name_elem.get_text().strip()
        return ""

    def _extract_title(self, element) -> str:
        """Extract job title from HTML element"""
        title_selectors = ['.title', '.position', '.role', '.job-title']
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem:
                return title_elem.get_text().strip()
        return ""

    def _search_professional_networks(self, company_name: str) -> List[ProductLeader]:
        """
        Search other professional networks and databases
        """
        # This would search other sources like AngelList, Crunchbase, etc.
        # For now, returning empty list
        return []

    def _deduplicate_leaders(self, leaders: List[ProductLeader]) -> List[ProductLeader]:
        """
        Remove duplicate leaders based on name and company
        """
        seen = set()
        unique_leaders = []
        
        for leader in leaders:
            key = (leader.name.lower(), leader.company.lower())
            if key not in seen:
                seen.add(key)
                unique_leaders.append(leader)
        
        return unique_leaders

    def export_to_csv(self, secured_cards: List[SecuredCardProduct], 
                     leaders: Dict[str, List[ProductLeader]], 
                     filename: str = "secured_card_research.csv"):
        """
        Export research results to CSV format
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Company', 'Product Name', 'Website', 'Annual Fee', 'Min Deposit',
                    'Leader Name', 'Leader Title', 'LinkedIn URL', 'Department'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for card in secured_cards:
                    company_leaders = leaders.get(card.company_name, [])
                    
                    if company_leaders:
                        for leader in company_leaders:
                            writer.writerow({
                                'Company': card.company_name,
                                'Product Name': card.product_name,
                                'Website': card.website,
                                'Annual Fee': card.annual_fee,
                                'Min Deposit': card.min_deposit,
                                'Leader Name': leader.name,
                                'Leader Title': leader.title,
                                'LinkedIn URL': leader.linkedin_url,
                                'Department': leader.department
                            })
                    else:
                        # Write company info even without leaders
                        writer.writerow({
                            'Company': card.company_name,
                            'Product Name': card.product_name,
                            'Website': card.website,
                            'Annual Fee': card.annual_fee,
                            'Min Deposit': card.min_deposit,
                            'Leader Name': '',
                            'Leader Title': '',
                            'LinkedIn URL': '',
                            'Department': ''
                        })
            
            logger.info(f"Results exported to {filename}")
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")

    def run_comprehensive_research(self) -> Dict:
        """
        Run comprehensive research with all enhanced features
        """
        logger.info("Starting comprehensive secured card product research...")
        
        # Step 1: Discover companies with secured cards
        secured_cards = self.discover_secured_card_companies()
        logger.info(f"Found {len(secured_cards)} companies with secured cards")
        
        # Step 2: Find product leaders using advanced methods
        leaders = self.find_product_leaders_advanced(secured_cards)
        
        # Step 3: Export results
        self.export_to_csv(secured_cards, leaders)
        
        # Step 4: Generate detailed report
        report = self._generate_comprehensive_report(secured_cards, leaders)
        
        return {
            'secured_cards': secured_cards,
            'leaders': leaders,
            'report': report,
            'summary': {
                'total_companies': len(secured_cards),
                'total_leaders': sum(len(l) for l in leaders.values()),
                'companies_with_leaders': len(leaders),
                'avg_leaders_per_company': sum(len(l) for l in leaders.values()) / len(leaders) if leaders else 0
            }
        }

    def _generate_comprehensive_report(self, secured_cards: List[SecuredCardProduct], 
                                     leaders: Dict[str, List[ProductLeader]]) -> str:
        """
        Generate a comprehensive research report
        """
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE SECURED CARD PRODUCT RESEARCH REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 40)
        report.append(f"• Total companies identified: {len(secured_cards)}")
        report.append(f"• Total product leaders found: {sum(len(l) for l in leaders.values())}")
        report.append(f"• Companies with leadership data: {len(leaders)}")
        report.append(f"• Average leaders per company: {sum(len(l) for l in leaders.values()) / len(leaders) if leaders else 0:.1f}")
        report.append("")
        
        # Companies by category
        major_banks = [c for c in secured_cards if any(bank in c.company_name.lower() for bank in ['bank', 'chase', 'citi', 'wells', 'capital'])]
        credit_unions = [c for c in secured_cards if 'credit union' in c.company_name.lower()]
        fintech = [c for c in secured_cards if c.company_name in ['Chime', 'Self', 'Petal', 'Tomo', 'Yendo']]
        
        report.append("COMPANIES BY CATEGORY")
        report.append("-" * 40)
        report.append(f"Major Banks: {len(major_banks)}")
        report.append(f"Credit Unions: {len(credit_unions)}")
        report.append(f"Fintech Companies: {len(fintech)}")
        report.append(f"Other Financial Institutions: {len(secured_cards) - len(major_banks) - len(credit_unions) - len(fintech)}")
        report.append("")
        
        # Detailed company listings
        report.append("DETAILED COMPANY INFORMATION")
        report.append("-" * 40)
        for card in secured_cards:
            report.append(f"\n{card.company_name.upper()}")
            report.append(f"  Product: {card.product_name}")
            report.append(f"  Website: {card.website}")
            if card.annual_fee:
                report.append(f"  Annual Fee: {card.annual_fee}")
            if card.min_deposit:
                report.append(f"  Minimum Deposit: {card.min_deposit}")
            if card.apr_range:
                report.append(f"  APR Range: {card.apr_range}")
            
            # Add leaders for this company
            company_leaders = leaders.get(card.company_name, [])
            if company_leaders:
                report.append(f"  Product Leaders ({len(company_leaders)}):")
                for leader in company_leaders:
                    report.append(f"    • {leader.name} - {leader.title}")
                    if leader.linkedin_url:
                        report.append(f"      LinkedIn: {leader.linkedin_url}")
        
        return "\n".join(report)

def main():
    """Main function to run the enhanced agent"""
    print("Starting Enhanced Secured Card Research Agent...")
    
    # Configuration
    config = {
        'max_companies': 50,
        'max_leaders_per_company': 5,
        'include_contact_info': False  # Set to True if you have proper APIs
    }
    
    agent = EnhancedSecuredCardAgent(config)
    results = agent.run_comprehensive_research()
    
    print(results['report'])
    print(f"\nRESEARCH COMPLETE!")
    print(f"Results exported to CSV file.")

if __name__ == "__main__":
    main()