"""
YAML文件处理工具类
用于读取接口配置YAML文件
"""
import os
import yaml
import logging
from typing import Dict, Any


class YamlHandler:
    """YAML文件处理类"""
    
    def __init__(self, yaml_path: str):
        """
        初始化YAML处理器
        :param yaml_path: YAML文件路径
        """
        self.yaml_path = yaml_path
        self.logger = logging.getLogger(__name__)
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML文件不存在: {yaml_path}")
    
    def read_yaml(self) -> Dict[str, Any]:
        """
        读取YAML文件
        :return: YAML配置字典
        """
        try:
            with open(self.yaml_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                if content is None:
                    return {}
                self.logger.info(f"成功读取YAML文件: {self.yaml_path}")
                return content
        except Exception as e:
            self.logger.error(f"读取YAML文件失败: {str(e)}")
            raise
    
    def get_api_config(self) -> Dict[str, Any]:
        """
        获取API配置信息
        :return: API配置字典，包含url、method、params等
        """
        config = self.read_yaml()
        return config




