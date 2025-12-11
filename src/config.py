import json
from typing import Any
import requests
import os


def download_with_requests(output_path: str = "cache/api.json") -> None:
    """下载 models.dev 项目的 API 配置文件
    
    Args:
        output_path: 保存文件路径，默认 "cache/api.json"
    """
    url = "https://models.dev/api.json"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(response.text)


def get_profile(provider: str, model_name: str, data_json: str = "cache/api.json") -> dict[str, Any]:
    """获取模型信息
    模型信息来自于 models.dev 项目。
    使用 `curl https://models.dev/api.json > temp/api.json` 下载或更新模型配置文件。
    
    Args:
        provider: 模型供应商
        model_name: 模型名称
        data_json: 模型配置文件路径
    
    Returns:
        模型配置字典
    """
    if not os.path.exists(data_json):
        download_with_requests(data_json)

    with open(data_json, "r") as f:
        data = json.load(f)
        
    try:
        result = data[provider]["models"][model_name]
        result["model_provider"] = provider
    except KeyError:
        raise ValueError(f" Provider {provider} or model {model_name} not found")
    return result