#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON格式测试工具
用于测试生成的JSON是否能够正确解析，避免控制字符错误
"""

import json
import os
from datetime import datetime

def clean_string_for_json(text: str) -> str:
    """清理字符串中的控制字符"""
    if not isinstance(text, str):
        return text
    
    cleaned_value = ""
    for char in text:
        char_code = ord(char)
        if char_code >= 32:  # 可见字符
            cleaned_value += char
        elif char in ['\n', '\r', '\t']:  # 保留常见的格式字符，但转为空格
            cleaned_value += ' '  # 转为空格
        # 其他控制字符直接忽略
    
    # 清理多余的空格
    cleaned_value = ' '.join(cleaned_value.split())
    return cleaned_value

def test_json_with_sample_data():
    """使用示例数据测试JSON格式"""
    print("🧪 JSON格式测试工具")
    print("=" * 50)
    
    # 模拟用户信息（包含可能有问题的字符）
    sample_user_info = {
        "nickname": "秋琳说电影",
        "signature": "招高水平代剪文案 \n能做沙盘有战争电影解说经验的请联系我",  # 包含换行符
        "sec_user_id": "",
        "uid": "295095704230269",
        "unique_id": "33410363400",
        "avatar": "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/test.jpeg",
        "ip_location": "IP属地：山东",
        "follower_count": 310586,
        "following_count": 9,
        "aweme_count": 69,
        "total_favorited": 7865372
    }
    
    # 清理用户信息
    cleaned_user_info = {}
    for key, value in sample_user_info.items():
        if isinstance(value, str):
            cleaned_user_info[key] = clean_string_for_json(value)
        else:
            cleaned_user_info[key] = value
    
    # 构建完整JSON
    complete_json_data = {
        "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_url": "https://www.douyin.com/user/MS4wLjABAAAAtest",
        "processing_index": 1,
        "user_info": cleaned_user_info
    }
    
    # 转换为JSON字符串
    try:
        json_string = json.dumps(complete_json_data, ensure_ascii=False, indent=2)
        print("✅ JSON序列化成功")
        print(f"JSON长度: {len(json_string)} 字符")
        
        # 测试反序列化
        try:
            parsed_data = json.loads(json_string)
            print("✅ JSON反序列化成功")
            
            # 显示清理后的签名
            original_signature = sample_user_info.get('signature', '')
            cleaned_signature = cleaned_user_info.get('signature', '')
            
            print(f"\n📝 签名字段对比:")
            print(f"原始签名: {repr(original_signature)}")
            print(f"清理后签名: {repr(cleaned_signature)}")
            
            # 保存测试文件
            test_filename = "test_json_output.json"
            with open(test_filename, 'w', encoding='utf-8') as f:
                f.write(json_string)
            
            print(f"\n💾 测试JSON已保存到: {test_filename}")
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON反序列化失败: {e}")
            print(f"错误位置: {e.pos}")
            return False
            
    except Exception as e:
        print(f"❌ JSON序列化失败: {e}")
        return False

def test_existing_json_file(file_path: str):
    """测试已存在的JSON文件"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 测试文件: {file_path}")
        print(f"文件大小: {len(content)} 字符")
        
        # 尝试解析
        parsed_data = json.loads(content)
        print("✅ 现有JSON文件解析成功")
        
        # 显示基本信息
        if 'user_info' in parsed_data:
            user_info = parsed_data['user_info']
            nickname = user_info.get('nickname', '未知')
            signature = user_info.get('signature', '无签名')
            print(f"用户昵称: {nickname}")
            print(f"用户签名: {repr(signature)}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        print(f"错误位置: 第{e.lineno}行，第{e.colno}列")
        
        # 显示错误附近的内容
        lines = content.split('\n')
        if e.lineno <= len(lines):
            error_line = lines[e.lineno - 1]
            print(f"错误行内容: {repr(error_line)}")
            
        return False
    except Exception as e:
        print(f"❌ 文件读取失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 启动JSON格式测试")
    
    # 测试示例数据
    print("\n1️⃣ 测试示例数据")
    success1 = test_json_with_sample_data()
    
    # 测试现有文件（如果存在）
    print("\n2️⃣ 测试现有JSON文件")
    test_files = [
        "integrated_output/20250901_173711_002_秋琳说电影.json",
        "test_json_output.json"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📂 找到文件: {test_file}")
            test_existing_json_file(test_file)
        else:
            print(f"⚠️ 文件不存在: {test_file}")
    
    print("\n" + "=" * 50)
    print("🎯 测试完成")
    
    if success1:
        print("✅ 建议: JSON格式处理正常，可以继续使用")
    else:
        print("❌ 建议: 需要检查JSON格式处理逻辑")

if __name__ == "__main__":
    main()
