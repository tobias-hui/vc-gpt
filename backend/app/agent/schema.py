from pydantic import BaseModel, Field
from typing import Dict, Optional

class DateProfile(BaseModel):
    year: str = Field(None, description="The year")
    month: str = Field(None, description="The month")
    day: str = Field(None, description="The day")

class ProductsAndServices(BaseModel):
    products_and_services_explain: str = Field(None, description="The products and services explain")
    products_and_services_problem: str = Field(None, description="The products and services problem")
    products_and_services_pricing: str = Field(None, description="The products and services pricing")

class Company(BaseModel):
    company_description: str = Field(None, description="The company description")
    company_overview: str = Field(None, description="The company overview")
    company_mission_statement: str = Field(None, description="The company mission statement")
    company_philosophy_and_vision_statement: str = Field(None, description="The company philosophy and vision statement")

class ExecutiveSummary(BaseModel):
    company_objective: str = Field(None, description="The company objective")
    products_and_services: str = Field(None, description="The products and services")
    target_market: str = Field(None, description="The target market")
    competitive_analysis: str = Field(None, description="The competitive analysis")
    marketing_plan: str = Field(None, description="The marketing plan")
    sales_plan: str = Field(None, description="The sales plan")
    forecast: str = Field(None, description="The forecast")
    financing: str = Field(None, description="The financing")
    budget_allocation: str = Field(None, description="The budget allocation")
    staffing_and_hiring: str = Field(None, description="The staffing and hiring")
    location: str = Field(None, description="The location")
    technology: str = Field(None, description="The technology")
    key_performance_indicators: str = Field(None, description="The key performance indicators")

class CustomerProfile(BaseModel):
    customer_age: str = Field(None, description="The age range of the customer")
    customer_gender: str = Field(None, description="The gender of the customer")
    customer_location: str = Field(None, description="The location of the customer")
    customer_income: str = Field(None, description="The income of the customer")
    customer_occupation: str = Field(None, description="The occupation of the customer")
    customer_education_level: str = Field(None, description="The education level of the customer")
    customer_interests: str = Field(None, description="The interests of the customer")
    customer_habits: str = Field(None, description="The habits of the customer")

class BusinessProfile(BaseModel):
    business_industry: str = Field(None, description="The industry of the business")
    business_location: str = Field(None, description="The location of the business")
    business_size: str = Field(None, description="The size of the business")
    business_stage: str = Field(None, description="The stage of the business")
    business_annual_sales: str = Field(None, description="The annual sales of the business")
    business_challenges: str = Field(None, description="The challenges of the business")

class TargetCustomer(BaseModel):
    customer_profile: CustomerProfile = Field(None, description="The profile info of the customer")
    business_profile: BusinessProfile = Field(None, description="The profile info of the business")

class MarketResearch(BaseModel):
    primary_market_research: str = Field(None, description="Primary market research data")
    secondary_market_research: str = Field(None, description="Secondary market research data")

class MarketingPlan(BaseModel):
    market_research: MarketResearch = Field(None, description="Marketing research data")
    target_customer: TargetCustomer = Field(None, description="Target customer profile")

class CompanyManagement(BaseModel):
    company_management_system: str = Field(None, description="Company management system")
    company_management_mechanisms: str = Field(None, description="Company management mechanisms")

class FinancingPlan(BaseModel):
    financing_amount_and_purpose: str = Field(None, description="Financing amount and purpose")
    financing_price: str = Field(None, description="Financing price")
    financing_investment_return: str = Field(None, description="Financing investment return")
    financing_rights_and_interests_of_investors: str = Field(None, description="Financing rights and interests of investors")

class RisksAndResponses(BaseModel):
    risks_and_responses: str = Field(None, description="Risks and responses data")
    risks_and_responses_responses: str = Field(None, description="Risks and responses responses")

class Input(BaseModel):
    business_name: str = Field(None, description="Name of the business")
    company_logo: str = Field(None, description="URL of the company's logo")
    phone_number: str = Field(None, description="Contact phone number of the business")
    date: DateProfile = Field(None, description="The date")
    responsible_person: str = Field(None, description="Name of the person in charge")
    executive_summary:  ExecutiveSummary = Field(None, description="Executive summary data")
    company: Company = Field(None, description="Company data")
    products_and_services: ProductsAndServices = Field(None, description="Products and services data")
    marketing_plan: MarketingPlan = Field(None, description="Marketing plan data")
    company_management: CompanyManagement = Field(None, description="Company management data")
    financing_plan: FinancingPlan = Field(None, description="Financing plan data")
    risks_and_responses: Dict[str, str] = Field(None, description="Risks and responses data")
