import os
import pytest

from ..app.services.extract import extract_action_items,extract_action_items_api_llm

def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items

def test_extract_keywords():
    """测试关键词格式的行动项提取"""
    text = """
    Project plan:
    todo: Research new technologies
    action: Draft project proposal
    next: Schedule team meeting
    regular note without keyword
    """
    
    items = extract_action_items(text)
    assert "todo: Research new technologies" in items
    assert "action: Draft project proposal" in items
    assert "next: Schedule team meeting" in items

def test_extract_no_action_items():
    """测试没有行动项的文本"""
    text = """
    This is just a regular text with no action items.
    It contains multiple sentences but nothing that looks like a task.
    """
    
    items = extract_action_items(text)
    assert len(items) == 0

def test_extract_duplicates():
    """测试重复项的去重功能"""
    text = """
    - [ ] Fix bug
    * Fix bug
    1. Fix bug
    """
    
    items = extract_action_items(text)
    assert len(items) == 1  # 应该只保留一个"Fix bug"
    assert "Fix bug" in items

def test_extract_complex_formatting():
    """测试复杂格式的文本"""
    text = """
    Meeting Minutes:
    
    1. Agenda Items:
       - [ ] Review last week's progress
       - [ ] Discuss upcoming deadlines
    
    2. Action Items:
       * Complete documentation by Friday
       todo: Send status report to team
    
    3. Next Steps:
       action: Schedule follow-up meeting
    """
    
    items = extract_action_items(text)
    assert "Review last week's progress" in items
    assert "Discuss upcoming deadlines" in items
    assert "Complete documentation by Friday" in items
    assert "todo: Send status report to team" in items
    assert "action: Schedule follow-up meeting" in items

def test_extract_sentence_fallback():
    """测试当没有明确行动项时的句子分割回退功能"""
    text = """
    We need to prepare the presentation. Make sure to include all charts.
    The deadline is next Monday. Check with the client for feedback.
    """
    
    items = extract_action_items(text)
    # 这些句子应该被识别为命令式并提取出来
    assert "Check with the client for feedback." in items

def test_extract_action_items_api_llm():
    """测试使用外部LLM API提取行动项"""
    text = "We need to fix the login bug by Friday. Update docs too."
    
    items = extract_action_items_api_llm(text)
    assert "Fix the login bug by Friday" in items
    assert "Update docs too" in items

def test_extract_action_items_api_llm_multilingual():
    """测试混合多语言文本的行动项提取，确保语言一致性"""
    text = """
    会议纪要：
    - 修复登录页面的bug (Fix the login page bug)
    * 编写中文文档 (Write Chinese documentation)
    1. Schedule team meeting in English
    """
    
    items = extract_action_items_api_llm(text)
    # 检查提取的项目是否保持原始语言
    assert any("修复登录页面的bug" in item for item in items)
    assert any("编写中文文档" in item for item in items)
    assert any("Schedule team meeting" in item for item in items)

def test_extract_action_items_api_llm_invalid_symbols():
    """测试包含无效符号的文本处理"""
    text = """
    行动项：
    - @#$%^&*()_+ 无效符号开头的内容
    * 正常行动项：创建新用户
    !@#$%^ 纯无效符号行
    """
    
    items = extract_action_items_api_llm(text)
    assert any("创建新用户" in item for item in items)
    # 确保无效符号行没有被错误提取
    assert not any("@#$%^&*()_+" in item for item in items)

def test_extract_action_items_api_llm_invalid_sentences():
    """测试无效语句的处理"""
    text = """
    正常内容：
    1. 完成项目报告
    无效句子：
    - 这只是一个普通的陈述，不是行动项
    * 今天天气很好
    """
    
    items = extract_action_items_api_llm(text)
    assert any("完成项目报告" in item for item in items)

def test_extract_action_items_api_llm_valid_with_invalid():
    """测试有效命令混合无效内容的处理"""
    text = """
    项目计划：
    - [ ] 设计数据库 schema
    这是一段无关的叙述性文字，没有包含任何行动项。
    * 实现用户认证功能
    更多无关内容...
    1. 编写单元测试
    """
    
    items = extract_action_items_api_llm(text)
    assert any("设计数据库 schema" in item for item in items)
    assert any("实现用户认证功能" in item for item in items)
    assert any("编写单元测试" in item for item in items)

def test_extract_action_items_api_llm_complex_markdown():
    """测试复杂markdown格式的文本处理"""
    text = """
    # 项目里程碑
    
    ## 阶段一
    - [x] 已完成的任务
    - [ ] 待完成的任务：进行需求分析
    
    ## 阶段二
    * **重要**：实现核心功能
    * 次要：添加文档
    
    > 引用内容：这是一段引用，不是行动项
    
    `代码片段：print("Hello")`
    
    普通文本行。
    """
    
    items = extract_action_items_api_llm(text)
    assert any("待完成的任务：进行需求分析" in item for item in items)
    assert any("实现核心功能" in item for item in items)
    assert any("次要：添加文档" in item for item in items)

def test_extract_action_items_api_llm_duplicate_commands():
    """测试重复命令的处理"""
    text = """
    - 修复bug
    * 修复bug
    1. 修复bug
    todo: 修复bug
    action: 修复bug
    """
    
    items = extract_action_items_api_llm(text)
    # 统计"修复bug"出现的次数，应该去重
    fix_bug_count = sum(1 for item in items if "修复bug" in item)
    assert fix_bug_count >= 1  # 至少出现一次