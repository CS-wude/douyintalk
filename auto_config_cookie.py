#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音Cookie自动配置工具
基于auto_cookie_douyin.py，自动获取cookie并配置到config/cookie_config.txt
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, Optional, Union
from urllib.parse import urlparse


class DouyinCookieConfigManager:
    """抖音Cookie配置管理器 - 自动配置到config文件"""
    
    # 支持的浏览器列表
    SUPPORT_BROWSERS = {
        "Chrome": "chrome",
        "Edge": "edge", 
        "Firefox": "firefox",
        "Opera": "opera",
        "Brave": "brave",
        "Arc": "arc",
        "Vivaldi": "vivaldi",
        "Chromium": "chromium",
    }
    
    # Cookie验证必需的关键字段
    REQUIRED_FIELDS = ["odin_tt", "passport_csrf_token"]
    
    # 登录状态检查字段
    LOGIN_FIELD = "sessionid_ss"
    
    def __init__(self):
        # 配置文件路径
        self.config_dir = os.path.join(os.path.dirname(__file__), "config")
        self.cookie_config_file = os.path.join(self.config_dir, "cookie_config.txt")
        self.backup_file = os.path.join(self.config_dir, "cookie_backup.json")
        self.log_file = "cookie_config_log.txt"
        
        # 确保config目录存在
        os.makedirs(self.config_dir, exist_ok=True)
        
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        # 写入日志文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def validate_douyin_url(self, url: str) -> bool:
        """验证抖音用户主页链接"""
        douyin_patterns = [
            r"https?://www\.douyin\.com/user/[\w-]+",
            r"https?://v\.douyin\.com/[\w-]+",
            r"https?://www\.iesdouyin\.com/share/user/[\d]+",
        ]
        
        for pattern in douyin_patterns:
            if re.match(pattern, url):
                return True
                
        return False
    
    def extract_user_id(self, url: str) -> Optional[str]:
        """从抖音链接中提取用户ID"""
        patterns = [
            r"https?://www\.douyin\.com/user/([\w-]+)",
            r"https?://www\.iesdouyin\.com/share/user/([\d]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_available_browsers(self) -> Dict[str, bool]:
        """检查可用的浏览器"""
        available = {}
        
        try:
            import rookiepy
            
            for browser_name, browser_func in self.SUPPORT_BROWSERS.items():
                try:
                    # 测试浏览器是否可用
                    func = getattr(rookiepy, browser_func)
                    # 尝试获取一个测试域名的cookie来检查浏览器是否可用
                    func(domains=["douyin.com"])
                    available[browser_name] = True
                except Exception:
                    available[browser_name] = False
                    
        except ImportError:
            self.log("rookiepy 库未安装，请先安装: pip install rookiepy", "ERROR")
            return {}
            
        return available
    
    def get_cookies_from_browser(self, browser_name: str) -> Optional[Dict[str, str]]:
        """从指定浏览器获取抖音Cookie"""
        try:
            import rookiepy
            
            if browser_name not in self.SUPPORT_BROWSERS:
                self.log(f"不支持的浏览器: {browser_name}", "ERROR")
                return None
                
            browser_func = self.SUPPORT_BROWSERS[browser_name]
            func = getattr(rookiepy, browser_func)
            
            self.log(f"正在从 {browser_name} 浏览器获取Cookie...")
            
            # 获取douyin.com域名的cookie
            cookies = func(domains=["douyin.com"])
            
            if not cookies:
                self.log(f"从 {browser_name} 未找到抖音Cookie", "WARNING")
                return None
                
            # 转换为字典格式
            cookie_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
            
            self.log(f"成功从 {browser_name} 获取到 {len(cookie_dict)} 个Cookie字段")
            return cookie_dict
            
        except ImportError:
            self.log("rookiepy 库未安装，请先安装: pip install rookiepy", "ERROR")
            return None
        except Exception as e:
            self.log(f"从 {browser_name} 获取Cookie失败: {e}", "ERROR")
            return None
    
    def validate_cookie(self, cookie_dict: Dict[str, str]) -> Dict[str, Union[bool, str]]:
        """验证Cookie的有效性"""
        result = {
            "valid": False,
            "logged_in": False,
            "missing_fields": [],
            "message": ""
        }
        
        # 检查必需字段
        missing_fields = []
        for field in self.REQUIRED_FIELDS:
            if field not in cookie_dict or not cookie_dict[field]:
                missing_fields.append(field)
        
        result["missing_fields"] = missing_fields
        
        if missing_fields:
            result["message"] = f"Cookie缺少必需字段: {', '.join(missing_fields)}"
            return result
        
        # 检查登录状态
        if self.LOGIN_FIELD in cookie_dict and cookie_dict[self.LOGIN_FIELD]:
            result["logged_in"] = True
            result["message"] = "Cookie有效，已登录状态"
        else:
            result["message"] = "Cookie有效，但未登录状态"
        
        result["valid"] = True
        return result
    
    def cookie_dict_to_string(self, cookie_dict: Dict[str, str]) -> str:
        """将Cookie字典转换为字符串格式"""
        return "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])
    
    def read_config_file(self) -> str:
        """读取配置文件内容"""
        if not os.path.exists(self.cookie_config_file):
            # 如果配置文件不存在，创建默认配置
            self.create_default_config()
        
        try:
            with open(self.cookie_config_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            self.log(f"读取配置文件失败: {e}", "ERROR")
            return ""
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = """# 抖音Cookie配置文件
# 使用说明：
# 1. 将您的完整cookie字符串粘贴到下面的cookie行
# 2. 或者设置浏览器自动获取方式：chrome 或 edge
# 3. 以 # 开头的行为注释行，会被忽略

# 方式1：直接填写cookie字符串（推荐）
# 请将完整的cookie字符串粘贴到下面（去掉前面的#号）：
#cookie=your_cookie_string_here

# 方式2：自动从浏览器获取（备用）
# 支持 chrome 或 edge
browser=chrome

# 注意事项：
# - Cookie有效期较短，通常几小时到几天
# - 如果获取失败，请重新登录抖音网页版获取新的cookie
# - 建议定期更新cookie以保持有效性
"""
        with open(self.cookie_config_file, "w", encoding="utf-8") as f:
            f.write(default_config)
        
        self.log(f"已创建默认配置文件: {self.cookie_config_file}")
    
    def update_config_file(self, cookie_string: str, browser_name: str = "chrome"):
        """更新配置文件中的cookie"""
        # 备份原配置文件
        self.backup_config()
        
        # 读取原配置文件
        content = self.read_config_file()
        lines = content.split('\n')
        
        # 更新时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 构建新的配置内容
        new_lines = []
        cookie_updated = False
        
        for line in lines:
            if line.strip().startswith('cookie=') or line.strip().startswith('#cookie='):
                # 更新cookie行
                new_lines.append(f"cookie={cookie_string}")
                cookie_updated = True
            elif line.strip().startswith('browser='):
                # 更新浏览器行
                new_lines.append(f"browser={browser_name}")
            elif line.strip().startswith('# 注意事项：'):
                # 在注意事项前添加更新时间
                new_lines.append(f"# 最后更新时间：{timestamp}")
                new_lines.append(line)
            else:
                new_lines.append(line)
        
        # 如果没找到cookie行，在合适位置添加
        if not cookie_updated:
            # 在第一个注释块后添加cookie
            insert_index = 0
            for i, line in enumerate(new_lines):
                if line.strip().startswith('# 方式1：'):
                    insert_index = i + 2
                    break
            
            new_lines.insert(insert_index, f"cookie={cookie_string}")
        
        # 写入更新后的配置
        with open(self.cookie_config_file, "w", encoding="utf-8") as f:
            f.write('\n'.join(new_lines))
        
        self.log(f"✅ Cookie已更新到配置文件: {self.cookie_config_file}")
    
    def backup_config(self):
        """备份当前配置"""
        if os.path.exists(self.cookie_config_file):
            try:
                # 读取当前配置
                with open(self.cookie_config_file, "r", encoding="utf-8") as f:
                    current_config = f.read()
                
                # 创建备份数据
                backup_data = {
                    "timestamp": datetime.now().isoformat(),
                    "config_content": current_config
                }
                
                # 保存备份
                with open(self.backup_file, "w", encoding="utf-8") as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                
                self.log(f"配置文件已备份到: {self.backup_file}")
                
            except Exception as e:
                self.log(f"备份配置文件失败: {e}", "WARNING")
    
    def save_cookie_info(self, cookie_dict: Dict[str, str], user_url: str = "", browser_name: str = ""):
        """保存详细的cookie信息到JSON文件"""
        cookie_info = {
            "timestamp": datetime.now().isoformat(),
            "user_url": user_url,
            "browser_source": browser_name,
            "cookie_dict": cookie_dict,
            "cookie_string": self.cookie_dict_to_string(cookie_dict),
            "validation": self.validate_cookie(cookie_dict),
            "config_file": self.cookie_config_file
        }
        
        info_file = os.path.join(self.config_dir, "cookie_info.json")
        with open(info_file, "w", encoding="utf-8") as f:
            json.dump(cookie_info, f, ensure_ascii=False, indent=2)
        
        self.log(f"Cookie详细信息已保存到: {info_file}")
    
    def auto_configure_cookie(self, user_url: str) -> bool:
        """自动获取Cookie并配置到config文件的主流程"""
        self.log("=== 抖音Cookie自动配置工具 ===")
        
        # 验证URL
        if not self.validate_douyin_url(user_url):
            self.log("输入的URL不是有效的抖音用户主页链接", "ERROR")
            self.log("支持的格式示例:")
            self.log("  - https://www.douyin.com/user/MS4wLjABAAAA...")
            self.log("  - https://v.douyin.com/iJsAmXXr/")
            return False
        
        user_id = self.extract_user_id(user_url)
        if user_id:
            self.log(f"检测到用户ID: {user_id}")
        
        # 检查可用浏览器
        self.log("正在检查可用的浏览器...")
        available_browsers = self.get_available_browsers()
        
        if not available_browsers:
            self.log("未找到可用的浏览器或rookiepy库未安装", "ERROR")
            return False
        
        # 显示可用浏览器
        available_list = [name for name, available in available_browsers.items() if available]
        if not available_list:
            self.log("没有找到包含抖音Cookie的浏览器", "WARNING")
            return False
        
        self.log(f"找到可用浏览器: {', '.join(available_list)}")
        
        # 尝试从每个浏览器获取Cookie
        for browser_name in available_list:
            self.log(f"\n--- 尝试从 {browser_name} 获取Cookie ---")
            
            cookie_dict = self.get_cookies_from_browser(browser_name)
            if not cookie_dict:
                continue
            
            # 验证Cookie
            validation = self.validate_cookie(cookie_dict)
            
            if validation["valid"]:
                self.log(f"✅ Cookie验证成功: {validation['message']}")
                
                # 转换为字符串
                cookie_string = self.cookie_dict_to_string(cookie_dict)
                
                # 更新配置文件
                self.update_config_file(cookie_string, browser_name.lower())
                
                # 保存详细信息
                self.save_cookie_info(cookie_dict, user_url, browser_name)
                
                # 显示配置结果
                self.log("\n=== 配置完成 ===")
                self.log(f"配置文件: {self.cookie_config_file}")
                self.log(f"Cookie字段数量: {len(cookie_dict)}")
                self.log(f"登录状态: {'已登录' if validation['logged_in'] else '未登录'}")
                self.log(f"源浏览器: {browser_name}")
                
                # 显示Cookie字符串的前100个字符
                if len(cookie_string) > 100:
                    self.log(f"Cookie预览: {cookie_string[:100]}...")
                else:
                    self.log(f"Cookie字符串: {cookie_string}")
                
                return True
            else:
                self.log(f"❌ Cookie验证失败: {validation['message']}", "WARNING")
        
        self.log("所有浏览器都未找到有效的抖音Cookie", "ERROR")
        return False
    
    def show_config_status(self):
        """显示当前配置状态"""
        self.log("\n=== 当前配置状态 ===")
        
        if os.path.exists(self.cookie_config_file):
            self.log(f"✅ 配置文件存在: {self.cookie_config_file}")
            
            # 读取配置内容
            content = self.read_config_file()
            lines = content.split('\n')
            
            cookie_found = False
            browser_setting = "未设置"
            
            for line in lines:
                if line.strip().startswith('cookie=') and not line.strip().startswith('#cookie='):
                    cookie_value = line.split('=', 1)[1] if '=' in line else ""
                    if cookie_value and cookie_value != "your_cookie_string_here":
                        cookie_found = True
                        self.log(f"✅ 发现Cookie配置（长度: {len(cookie_value)}）")
                elif line.strip().startswith('browser='):
                    browser_setting = line.split('=', 1)[1] if '=' in line else "未设置"
            
            if not cookie_found:
                self.log("❌ 未找到有效的Cookie配置")
            
            self.log(f"浏览器设置: {browser_setting}")
            
        else:
            self.log(f"❌ 配置文件不存在: {self.cookie_config_file}")
        
        # 检查备份文件
        if os.path.exists(self.backup_file):
            self.log(f"✅ 备份文件存在: {self.backup_file}")
        else:
            self.log("❌ 无备份文件")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = f"""
=== 抖音Cookie自动配置工具使用说明 ===

功能：
- 自动从浏览器获取抖音Cookie
- 验证Cookie有效性和登录状态
- 自动配置到 {self.cookie_config_file}
- 备份原有配置，防止数据丢失

使用方法：
1. 在浏览器中登录抖音账号
2. 运行此脚本
3. 输入抖音用户主页链接
4. 程序会自动获取并配置Cookie

支持的浏览器：
- Chrome, Edge, Firefox, Opera, Brave, Arc, Vivaldi, Chromium

注意事项：
- Windows系统需要管理员权限运行
- 确保已安装 rookiepy 库: pip install rookiepy
- 需要先在浏览器中登录抖音账号
- 程序会自动备份原配置文件

输出文件：
- {self.cookie_config_file}: Cookie配置文件
- {self.backup_file}: 配置备份文件
- {self.log_file}: 运行日志文件

命令：
- python auto_config_cookie.py [URL]  # 配置Cookie
- python auto_config_cookie.py status # 查看配置状态
- python auto_config_cookie.py help   # 显示帮助
"""
        print(help_text)


def main():
    """主函数"""
    manager = DouyinCookieConfigManager()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ["-h", "--help", "help"]:
            manager.show_help()
            return
        elif arg == "status":
            manager.show_config_status()
            return
        else:
            user_url = sys.argv[1]
    else:
        # 交互式输入
        print("=== 抖音Cookie自动配置工具 ===")
        print("请输入抖音用户主页链接:")
        print("示例: https://www.douyin.com/user/MS4wLjABAAAA...")
        print("或输入 'help' 查看帮助, 'status' 查看配置状态")
        
        user_input = input("链接: ").strip()
        
        if user_input.lower() == "help":
            manager.show_help()
            return
        elif user_input.lower() == "status":
            manager.show_config_status()
            return
        
        if not user_input:
            print("未输入链接，退出程序")
            return
        
        user_url = user_input
    
    # 执行Cookie配置
    success = manager.auto_configure_cookie(user_url)
    
    if success:
        print("\n✅ Cookie配置成功！")
        print(f"配置文件: {manager.cookie_config_file}")
        print(f"备份文件: {manager.backup_file}")
        print(f"日志文件: {manager.log_file}")
        print("\n现在可以使用配置文件中的Cookie进行抖音数据获取了！")
    else:
        print("\n❌ Cookie配置失败！")
        print("请检查:")
        print("1. 是否在浏览器中登录了抖音账号")
        print("2. 是否以管理员权限运行程序")
        print("3. 是否安装了 rookiepy 库")
        print("\n输入 'python auto_config_cookie.py help' 查看详细帮助")


if __name__ == "__main__":
    main()
