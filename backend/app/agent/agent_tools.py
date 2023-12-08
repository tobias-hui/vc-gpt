import jwt
import json
import re
import json
import http
import time
import logging
from langchain.tools import tool
from typing import Dict
import traceback
import sys

# 创建一个专门用于记录函数输入的日志处理器
log_input_handler = logging.FileHandler('function_input.log')
# 设置日志等级为 INFO
log_input_handler.setLevel(logging.INFO)

# 创建一个新的logger
log_input_logger = logging.getLogger('inputLogger')
log_input_logger.setLevel(logging.INFO)
log_input_logger.addHandler(log_input_handler)


from app.config import Settings
from .schema import Input

setting = Settings()





# 在实际使用时，'template'将为你的模板，'data'为函数的输入
# filtered_data = filter_input(data, template)
# result = generate_bp_pdf(filtered_data)



@tool("generate_bp_pdf", args_schema=Input)
def generate_bp_pdf(data: Input) -> str:
    '''Generate a Business Plan PDF from a given data dictionary that filled the BP content and returns the URL of the generated PDF BP.'''
    
    log_input_logger.info(f"generate_bp_pdf was called with input_data: {data}")  # 使用新的logger记录函数输入

    template = {
        "business_name": "",
        "company_logo": "",
        "phone_number": "",
        "date": {
            "year": "",
            "month": "",
            "day": ""
        },
        "responsible_person": "",
        "executive_summary": {
            "company_objective": "",
            "products_and_services": "",
            "target_market": "",
            "competitive_analysis": "",
            "marketing_plan": "",
            "sales_plan": "",
            "forecast": "",
            "financing": "",
            "budget_allocation": "",
            "staffing_and_hiring": "",
            "location": "",
            "technology": "",
            "key_performance_indicators": ""
        },
        "company": {
            "company_description": "",
            "company_overview": "",
            "company_mission_statement": "",
            "company_philosophy_and_vision_statement": ""
        },
        "products_and_services": {
            "products_and_services_explain": "",
            "products_and_services_problem": "",
            "products_and_services_pricing": ""
        },
        "marketing_plan": {
            "market_research": {
                "primary_market_research": "",
                "secondary_market_research": ""
            },
            "target_customer": {
                "customer_profile": {
                    "customer_age": "",
                    "customer_gender": "",
                    "customer_location": "",
                    "customer_income": "",
                    "customer_occupation": "",
                    "customer_education_level": "",
                    "customer_interests": "",
                    "customer_habits": ""
                },
                "business_profile": {
                    "business_industry": "",
                    "business_location": "",
                    "business_size": "",
                    "business_stage": "",
                    "business_annual_sales": "",
                    "business_challenges": ""
                }
            }
        },
        "company_management": {
            "company_management_system": "",
            "company_management_mechanisms": ""
        },
        "financing_plan": {
            "financing_amount_and_purpose": "",
            "financing_price": "",
            "financing_investment_return": "",
            "financing_rights_and_interests_of_investors": ""
        },
        "risks_and_responses": {
            "risks_and_responses_risks": "",
            "risks_and_responses_responses": ""
        }
    }

    def create_jwt():
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }

        # JWT 负载
        payload = {
            "iss": setting.pdf_api_key,
            "sub": "huik99298@gmail.com",
            "exp": int(time.time()) + 3000
        }

        # 生成 JWT
        token = jwt.encode(payload, setting.pdf_secret_key, algorithm='HS256', headers=header)
        return token
    
    def filter_input(data, template):
        if isinstance(data, str):
            try:
                # 尝试解析字符串为字典：
                data = json.loads(data)
            except json.JSONDecodeError:
                return {}
        if not isinstance(data, dict):
            return {}

        filtered_data = {}

        for key, val in data.items():
            if key in template:
                if isinstance(val, dict):
                    filtered_result = filter_input(val, template[key])
                    if filtered_result: # 非空字典则添加到结果集
                        filtered_data[key] = filtered_result
                elif isinstance(val, str):
                    filtered_result = filter_input(val, template)
                    if filtered_result: # 非空字典则添加到结果集
                        filtered_data[key] = filtered_result
                else:
                    filtered_data[key] = val

        return filtered_data

    def seek_keys(input_data, template):
        result = {}
        if isinstance(input_data, dict):
            for k in input_data:
                if k in template:
                    result[k] = input_data[k]
                else:
                    result.update(seek_keys(input_data[k], template))
        elif isinstance(input_data, list):
            for item in input_data:
                result.update(seek_keys(item, template))

        return result
    filtered_data = seek_keys(data, template)
    log_input_logger.info(f"filtered data: {filtered_data}")

    conn = http.client.HTTPSConnection("us1.pdfgeneratorapi.com")
    jwt_token = create_jwt()
    # 构建 payload
    payload = json.dumps({
        "template": {
            "id": "887291",
            "data": filtered_data
        },
        "format": "pdf",
        "output": "url",
        "name": "Business_Plan"
    }, ensure_ascii=False)

    payload = payload.encode('utf-8')

    headers = {
        'Authorization': f"Bearer {jwt_token}",
        'Content-Type': "application/json; charset=utf-8"
    }

    # 发送请求
    conn.request("POST", "/api/v4/documents/generate", payload, headers)

    # 获取响应
    res = conn.getresponse()
    data = res.read()

    result = data.decode("utf-8")
    response = json.loads(result)["response"]
    # 返回结果
    log_input_logger.info(f"generate_bp_pdf returned: {response}")
    return response