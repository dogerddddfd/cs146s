import requests

# 获取用户信息
user_response = requests.get('https://api.github.com/users/octocat')
user_data = user_response.json()
print(f"用户名: {user_data['login']}")
print(f"仓库数: {user_data['public_repos']}")

# 获取仓库信息
repo_response = requests.get('https://api.github.com/repos/octocat/Hello-World')
repo_data = repo_response.json()
print(f"仓库名: {repo_data['name']}")
print(f"描述: {repo_data['description']}")
print(f"星标数: {repo_data['stargazers_count']}")