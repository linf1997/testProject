"""
HTTP请求客户端封装类
基于Requests库封装HTTP请求
"""
import requests
import logging
from typing import Dict, Any, Optional
import json


class HttpClient:
    """HTTP请求客户端类"""
    
    def __init__(self, timeout: int = 30):
        """
        初始化HTTP客户端
        :param timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
    
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        发送HTTP请求
        :param method: 请求方法（GET、POST、PUT、DELETE等）
        :param url: 请求URL
        :param kwargs: 其他请求参数（params、json、data、headers等）
        :return: Response对象
        """
        try:
            method = method.upper()
            self.logger.info(f"发送{method}请求: {url}")
            
            if kwargs.get('json'):
                self.logger.info(f"请求参数: {json.dumps(kwargs['json'], ensure_ascii=False, indent=2)}")
            
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            self.logger.info(f"响应状态码: {response.status_code}")
            try:
                self.logger.info(f"响应内容: {response.text[:500]}")  # 只记录前500个字符
            except:
                pass
            
            return response
        
        except requests.exceptions.Timeout:
            self.logger.error(f"请求超时: {url}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"请求失败: {str(e)}")
            raise
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """发送GET请求"""
        return self.request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """发送POST请求"""
        return self.request('POST', url, **kwargs)
    
    def put(self, url: str, **kwargs) -> requests.Response:
        """发送PUT请求"""
        return self.request('PUT', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        """发送DELETE请求"""
        return self.request('DELETE', url, **kwargs)
    
    def close(self):
        """关闭session"""
        self.session.close()




