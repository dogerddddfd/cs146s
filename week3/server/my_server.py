from fastmcp import FastMCP
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError
from ratelimit import limits, sleep_and_retry
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# GitHub API速率限制配置（未认证用户：60次/小时）
GITHUB_RATE_LIMIT_CALLS = 55  # 留5次缓冲
GITHUB_RATE_LIMIT_PERIOD = 3600  # 1小时（秒）

# 解析GitHub API速率限制信息
def parse_github_rate_limit(response):
    """解析GitHub API响应中的速率限制信息"""
    if 'X-RateLimit-Limit' in response.headers:
        limit = int(response.headers['X-RateLimit-Limit'])
        remaining = int(response.headers['X-RateLimit-Remaining'])
        reset = int(response.headers['X-RateLimit-Reset'])
        
        # 计算重置时间（秒）
        reset_time = reset - int(time.time())
        
        logger.info(f"GitHub API速率限制: {limit}次/小时，剩余: {remaining}次，重置时间: {reset_time}秒后")
        
        return {
            'limit': limit,
            'remaining': remaining,
            'reset': reset,
            'reset_time': reset_time
        }
    return None

# 创建带有主动速率限制的GitHub请求函数
@sleep_and_retry
@limits(calls=GITHUB_RATE_LIMIT_CALLS, period=GITHUB_RATE_LIMIT_PERIOD)
def github_request(url, **kwargs):
    """带有主动速率限制的GitHub API请求"""
    response = requests.get(url, **kwargs)
    
    # 解析速率限制信息
    rate_limit_info = parse_github_rate_limit(response)
    
    # 如果剩余请求次数不多，增加额外延迟
    if rate_limit_info and rate_limit_info['remaining'] < 10:
        logger.warning(f"GitHub API速率限制即将耗尽，剩余{rate_limit_info['remaining']}次请求")
        # 增加额外延迟以避免达到限制
        time.sleep(5)
    
    return response

mcp = FastMCP("My MCP Server")

# 其他工具保持不变...

@mcp.tool(
    name="get_github_user_info",
    description="获取GitHub用户信息",
)
def get_github_user_info(username: str) -> dict:
    """获取GitHub用户信息，带完整错误处理和速率限制"""
    try:
        # 使用带有主动速率限制的请求函数
        response = github_request(
            f'https://api.github.com/users/{username}',
            timeout=10,
            headers={'Accept': 'application/vnd.github.v3+json'}
        )
        
        # 检查HTTP状态码
        response.raise_for_status()
        
        return response.json()
        
    except ConnectionError as e:
        logger.error(f"连接GitHub API失败: {e}")
        raise Exception(f"无法连接到GitHub API，请检查网络连接。错误详情: {str(e)}")
        
    except Timeout as e:
        logger.error(f"GitHub API请求超时: {e}")
        raise Exception(f"GitHub API请求超时，请稍后重试。错误详情: {str(e)}")
        
    except HTTPError as e:
        logger.error(f"GitHub API返回错误状态码: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 404:
            raise Exception(f"找不到用户 '{username}'。请检查用户名是否正确。")
        elif e.response.status_code == 403:
            # 处理速率限制
            retry_after = e.response.headers.get('Retry-After', '未知')
            raise Exception(f"GitHub API速率限制已达。请等待 {retry_after} 秒后重试。")
        else:
            raise Exception(f"GitHub API返回错误 {e.response.status_code}: {e.response.reason}")
            
    except ValueError as e:
        logger.error(f"JSON解析失败: {e}")
        raise Exception(f"无法解析GitHub API响应。错误详情: {str(e)}")
        
    except Exception as e:
        logger.error(f"获取GitHub用户信息时发生未知错误: {e}")
        raise Exception(f"获取GitHub用户信息时发生未知错误。错误详情: {str(e)}")

# get_github_repo_info函数也需要类似修改...
@mcp.tool(
    name="get_github_repo_info",
    description="获取GitHub仓库信息",
)
def get_github_repo_info(username: str, repo: str) -> dict:
    """获取GitHub仓库信息"""
    try:
        response = github_request(
            f'https://api.github.com/repos/{username}/{repo}',
            timeout=10,
            headers={'Accept': 'application/vnd.github.v3+json'}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"获取GitHub仓库信息时发生错误: {e}")
        raise Exception(f"获取GitHub仓库信息时发生错误。错误详情: {str(e)}")

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)