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



json_data = {
    "business_name": "猫乐砂",
    "company_logo": "https://i.ibb.co/9VnnBnc/White-Creative-Doodle-Brainstorming-Presentation-2-removebg-preview.png",
    "phone_number": "你的电话号码",
    "date": {
      "year": "2023",
      "month": "12",
      "day": "8"
    },
    "responsible_person": "你的名字",
    "excutive_summary": {
      "company_objective": "提供高品质的猫砂产品，满足中国市场的需求。",
      "products_and_services": "我们的主要产品是猫砂，具有吸水性强、无尘、环保等特点。",
      "target_market": "中国的猫主人和宠物店。",
      "competitive_analysis": "我们的竞争对手主要是其他猫砂品牌，但我们的产品具有更好的性能和更合理的价格。",
      "marketing_plan": "我们将通过社交媒体、线上广告和宠物展会等方式进行推广。",
      "sales_plan": "我们计划通过电商平台和实体店销售我们的产品。",
      "forecast": "我们预计在第一年能达到100万的销售额。",
      "financing": "我们正在寻求投资者的投资，以帮助我们扩大生产和销售。",
      "budget_allocation": "我们的预算将主要用于产品开发、营销和销售。",
      "staffing_and_hiring": "我们计划招聘销售和营销人员，以推动我们的业务发展。",
      "location": "我们的办公地点在中国。",
      "technology": "我们将使用最新的生产技术，以确保产品的质量。",
      "key_performance_indicators": "我们的主要绩效指标包括销售额、客户满意度和市场份额。"
    },
    "company": {
      "company_description": "猫乐砂是一家专注于猫砂生产和销售的公司。",
      "company_overview": "我们的目标是成为中国市场上最受欢迎的猫砂品牌。",
      "company_mission_statement": "我们的使命是提供最好的猫砂产品，让猫主人和他们的猫都能享受到最好的体验。",
      "company_philosophy_and_vision_statement": "我们的理念是以客户为中心，我们的愿景是成为中国最大的猫砂供应商。"
    },
    "products_and_services": {
      "products_and_services_explain": "我们的猫砂是由天然材料制成，具有强大的吸水性和无尘的特点。",
      "products_and_services_problem": "我们的产品解决了市场上许多猫砂尘埃大、不易清理的问题。",
      "products_and_services_pricing": "我们的产品定价在市场平均水平，以吸引更多的客户。"
    },
    "marketing_plan": {
      "market_research": {
        "primary_market_research": "我们通过调查和访谈了解到，中国的猫主人对猫砂的需求很大，但市场上的产品往往不能满足他们的需求。",
        "secondary_market_research": "根据市场报告，中国的猫砂市场正在快速增长，预计未来几年将继续保持增长。"
      },
      "target_customer": {
        "customer_profile": {
          "customer_age": "20-50岁",
          "customer_gender": "不限",
          "customer_location": "中国",
          "customer_income": "中等收入以上",
          "customer_occupation": "不限",
          "customer_education_level": "不限",
          "customer_interests": "养猫",
          "customer_habits": "经常在线上购物"
        },
        "business_profile": {
          "business_industry": "宠物用品",
          "business_location": "中国",
          "business_size": "不限",
          "business_stage": "不限",
          "business_annual_sales": "不限",
          "business_challenges": "找到高品质的猫砂供应商"
        }
      }
    },
    "company_management": {
      "company_management_system": "我们的公司管理系统是以目标为导向，注重团队合作。",
      "company_management_mechanisms": "我们的管理机制包括定期的业务评估和员工培训。"
    },
    "financing_plan": {
      "financing_amount_and_purpose": "我们正在寻求100万的投资，用于扩大生产和销售。",
      "financing_price": "我们的融资价格是每股10元。",
      "financing_investment_return": "我们预计在3年内能实现投资回报。",
      "financing_rights_and_interests_of_investors": "投资者将获得我们公司的股份和分红权。"
    },
    "risks_and_responses": {
      "risks_and_responses_risks": "我们面临的风险包括市场竞争、原材料价格波动等。",
      "risks_and_responses_responses": "我们将通过提供高品质的产品、优化生产流程和建立稳定的供应链来应对这些风险。"
    }
  }

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
    
    def process_string(input_data, acc=None):
        if acc is None:
            acc = {}

        if isinstance(input_data, int): 
            return acc # return acc directly if the input_data is integer

        try:
            if isinstance(input_data, str):            
                try:
                    data = json.loads(input_data)  
                except json.JSONDecodeError: 
                    return acc
            elif isinstance(input_data, dict):
                data = input_data
            else:
                return acc

            if isinstance(data, dict): # ensure data is dict before looping
                for key, val in data.items():
                    if isinstance(val, dict):
                        flatten(val, acc)
                    else:
                        acc[key] = val
        except Exception as e:
            print(f"Error in process_string, data is {input_data}, error is {e}")
            traceback.print_exc(file=sys.stdout)
        
        print('process_string called with:', input_data)
        ...
        print('data after processing:', data)

        return acc




    def flatten(data, acc=None):
        if acc is None:
            acc = {}

        try:
            if not isinstance(data, (str, dict)):
                return acc

            if isinstance(data, str):
                return process_string(data, acc)
            elif isinstance(data, dict):
                for key, val in data.items():
                    if isinstance(val, dict):
                        flatten(val, acc)
                    elif isinstance(val, str):
                        process_string(val, acc)
                    else:
                        acc[key] = val

        except Exception as e:
            # 打印出错的数据和错误情况
            print(f"Error in flatten, data is {data}, error is {e}")
            traceback.print_exc(file=sys.stdout)
        print('flatten called with:', data)
        ...
        print('acc after flattening:', acc)

        return acc


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
                    filtered_data[key] = filter_input(val, template[key])
                else:
                    filtered_data[key] = val
        return filtered_data

    
    filtered_data = filter_input(flatten(data),template)
    log_input_logger.info(f"filtered data: {filtered_data}")

    conn = http.client.HTTPSConnection("us1.pdfgeneratorapi.com")
    jwt_token = create_jwt()
    # 构建 payload
    payload = json.dumps({
        "template": {
            "id": "887291",
            "data": json_data
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