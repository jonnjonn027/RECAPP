# Secured Card Research Agent

A comprehensive research tool that identifies companies offering secured credit cards and finds their product leaders. This agent automates the process of discovering secured card providers and locating key personnel in product management roles.

## 🎯 Features

### Core Capabilities
- **Company Discovery**: Automatically identifies companies offering secured credit cards
- **Product Leader Research**: Finds product managers, directors, and executives at target companies
- **Multi-Source Search**: Integrates with LinkedIn, company websites, and professional networks
- **Data Export**: Exports results to CSV format for easy analysis
- **Web Interface**: Modern, responsive UI for easy interaction

### What the Agent Does

1. **Identifies Secured Card Companies**
   - Searches web for secured credit card providers
   - Validates current offerings
   - Categorizes by company type (banks, credit unions, fintech)

2. **Finds Product Leaders**
   - Searches for relevant job titles (CPO, VP Product, Product Director, etc.)
   - Extracts LinkedIn profiles and contact information
   - Maps organizational structure

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)
1. Open `web_interface.html` in your browser
2. Configure your search parameters
3. Click "Start Research"
4. Export results when complete

### Option 2: Python Script
```bash
# Install dependencies
pip install -r requirements.txt

# Run basic agent
python secured_card_agent.py

# Run enhanced agent with web search
python enhanced_agent.py
```

## 📋 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional but Recommended)
Create a `.env` file with your API credentials:

```env
# Google Custom Search API (for enhanced web search)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# LinkedIn API (for professional network search)
LINKEDIN_API_KEY=your_linkedin_api_key_here
```

### 3. Getting API Keys

#### Google Custom Search API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Custom Search API
4. Create credentials (API key)
5. Set up Custom Search Engine at [programmablesearchengine.google.com](https://programmablesearchengine.google.com/)

#### LinkedIn API (Optional)
1. Visit [LinkedIn Developer Portal](https://developer.linkedin.com/)
2. Create an app
3. Request API access (requires approval)

## 💻 Usage Examples

### Basic Usage
```python
from secured_card_agent import SecuredCardAgent

# Initialize agent
agent = SecuredCardAgent()

# Run research
results = agent.run_research()

# Print summary
print(f"Found {results['summary']['total_companies']} companies")
print(f"Identified {results['summary']['total_leaders']} product leaders")
```

### Enhanced Usage with Configuration
```python
from enhanced_agent import EnhancedSecuredCardAgent

# Configure agent
config = {
    'max_companies': 50,
    'max_leaders_per_company': 5,
    'include_contact_info': True
}

# Initialize with config
agent = EnhancedSecuredCardAgent(config)

# Run comprehensive research
results = agent.run_comprehensive_research()

# Results are automatically exported to CSV
```

### Web Interface
1. Open `web_interface.html`
2. Select search mode:
   - **Comprehensive**: Full web search + known companies
   - **Known Companies**: Predefined list only
   - **Custom**: Your specific company list
3. Configure options:
   - Find product leaders
   - Search LinkedIn
   - Search company websites
   - Export to CSV
4. Set maximum companies to research
5. Click "Start Research"

## 📊 Output Format

### CSV Export Columns
- Company Name
- Product Name
- Website
- Annual Fee
- Minimum Deposit
- Leader Name
- Leader Title
- LinkedIn URL
- Department

### Example Results
```
Company,Product Name,Website,Annual Fee,Min Deposit,Leader Name,Leader Title,LinkedIn URL
Capital One,Capital One Secured Mastercard,https://www.capitalone.com,$0,$200,Sarah Johnson,VP Product Management,https://linkedin.com/in/sarah-johnson
Discover,Discover it® Secured Credit Card,https://www.discover.com,$0,$200,Jessica Rodriguez,Head of Product,https://linkedin.com/in/jessica-rodriguez
```

## 🏢 Companies Covered

### Major Banks
- Capital One
- Discover
- Wells Fargo
- Bank of America
- Citi
- Chase
- US Bank
- PNC Bank
- Truist
- TD Bank

### Credit Card Specialists
- OpenSky
- Applied Bank
- First Progress
- Credit One Bank
- Indigo
- Milestone
- Total Visa

### Fintech Companies
- Chime
- Self
- Petal
- Deserve
- Tomo
- Yendo
- Kikoff
- Sable

### Regional Banks & Credit Unions
- Navy Federal
- USAA
- Alliant Credit Union
- Pentagon Federal
- First Tech Federal Credit Union

## 🎯 Target Job Titles

The agent searches for these product leadership roles:
- Chief Product Officer (CPO)
- VP Product / Vice President Product
- Head of Product
- Director of Product / Product Director
- Senior Director Product
- Principal Product Manager
- VP Digital Products
- Head of Cards
- Cards Product Manager
- Credit Cards Product Manager
- Consumer Products Director
- Chief Technology Officer (CTO)
- VP Technology
- Head of Digital
- Digital Product Leader

## ⚙️ Configuration Options

### Search Parameters
```python
config = {
    'max_companies': 50,              # Maximum companies to research
    'max_leaders_per_company': 5,     # Maximum leaders per company
    'include_contact_info': False,    # Attempt to find email addresses
    'search_depth': 'comprehensive',  # 'basic', 'comprehensive', 'deep'
    'rate_limit_delay': 1.0,         # Delay between requests (seconds)
    'timeout': 30,                   # Request timeout (seconds)
    'user_agent_rotation': True,     # Rotate user agents
    'proxy_enabled': False,          # Use proxy rotation
}
```

### Search Sources
- **Web Search**: Google Custom Search API
- **LinkedIn**: Professional profiles and company pages
- **Company Websites**: Leadership and team pages
- **Professional Networks**: AngelList, Crunchbase (future)
- **News Sources**: Recent announcements and press releases

## 🔒 Ethical Considerations

This tool is designed for legitimate business research purposes:
- **Respect Rate Limits**: Built-in delays prevent overwhelming servers
- **Public Information Only**: Only searches publicly available information
- **Professional Use**: Intended for B2B outreach and market research
- **Privacy Compliant**: No personal information storage beyond research session

## 🛠️ Technical Architecture

### Core Components
- **SecuredCardAgent**: Basic research functionality
- **EnhancedSecuredCardAgent**: Advanced search with multiple sources
- **Web Interface**: Browser-based UI for non-technical users
- **Data Models**: Structured data classes for companies and leaders
- **Export System**: CSV and JSON output formats

### Dependencies
- **requests**: HTTP client for web requests
- **beautifulsoup4**: HTML parsing and data extraction
- **selenium**: Browser automation for dynamic content
- **pandas**: Data manipulation and analysis
- **google-api-python-client**: Google Custom Search integration

## 📈 Performance

### Expected Results
- **Companies Found**: 30-50 secured card providers
- **Product Leaders**: 2-5 leaders per company on average
- **Success Rate**: 70-90% for finding basic company info
- **LinkedIn Success**: 40-60% depending on API access
- **Processing Time**: 5-15 minutes for comprehensive search

### Optimization Tips
1. **Use API Keys**: Significantly improves search quality
2. **Reasonable Limits**: Set max_companies to 30-50 for best balance
3. **Rate Limiting**: Increase delays if getting blocked
4. **Proxy Rotation**: Use for large-scale research

## 🚀 Future Enhancements

### Planned Features
- **Contact Information**: Email finding and verification
- **Social Media Integration**: Twitter, Facebook, Instagram profiles
- **Company Intelligence**: Funding, revenue, employee count
- **Automated Outreach**: Email template generation
- **CRM Integration**: Salesforce, HubSpot, Pipedrive sync
- **Real-time Updates**: Monitor for new secured card launches
- **Advanced Analytics**: Market share analysis, competitive intelligence

### API Integrations
- **Clearbit**: Company and person enrichment
- **Hunter.io**: Email finding and verification
- **ZoomInfo**: Professional contact database
- **Crunchbase**: Company intelligence and funding data
- **AngelList**: Startup and investor information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions, issues, or feature requests:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error messages and configuration details

## 📞 Use Cases

### Business Development
- Identify potential clients in the secured card space
- Research competition and market positioning
- Find decision makers for partnership discussions

### Sales & Marketing
- Build targeted prospect lists
- Research key contacts before outreach
- Understand competitive landscape

### Product Management
- Analyze competitor product offerings
- Identify industry best practices
- Research team structures at similar companies

### Investment Research
- Evaluate fintech companies in the secured card space
- Identify key personnel for due diligence
- Understand market dynamics and players

---

**Note**: This tool is for research purposes only. Always respect website terms of service and applicable laws when conducting automated research.
