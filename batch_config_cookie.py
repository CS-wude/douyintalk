#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音Cookie批量自动配置工具
基于auto_config_cookie.py，从urls_config.txt文件批量读取链接并配置Cookie
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

# 导入原有的配置管理器
try:
    from auto_config_cookie import DouyinCookieConfigManager
except ImportError:
    print("❌ 无法导入 auto_config_cookie 模块，请确保文件存在")
    sys.exit(1)


class BatchDouyinCookieManager(DouyinCookieConfigManager):
    """批量抖音Cookie配置管理器"""
    
    def __init__(self):
        super().__init__()
        
        # 批量配置相关路径
        self.urls_config_file = os.path.join(os.path.dirname(__file__), "urls_config.txt")
        self.batch_log_file = "batch_cookie_config_log.txt"
        self.batch_result_file = os.path.join(self.config_dir, "batch_results.json")
        
        # 批量处理统计
        self.batch_stats = {
            "total_urls": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": None,
            "end_time": None,
            "results": []
        }
    
    def batch_log(self, message: str, level: str = "INFO"):
        """批量处理专用日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] [BATCH] {message}"
        print(log_entry)
        
        # 同时写入批量日志文件和原日志文件
        for log_file in [self.batch_log_file, self.log_file]:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
    
    def read_urls_config(self) -> List[str]:
        """读取URLs配置文件"""
        if not os.path.exists(self.urls_config_file):
            self.batch_log(f"URLs配置文件不存在: {self.urls_config_file}", "ERROR")
            return []
        
        urls = []
        try:
            with open(self.urls_config_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                
                # 处理单行多个链接（逗号或分号分隔）
                if ',' in line or ';' in line:
                    # 使用正则表达式分割，支持逗号和分号
                    split_urls = re.split(r'[,;]', line)
                    for url in split_urls:
                        url = url.strip()
                        if url and self.validate_douyin_url(url):
                            urls.append(url)
                        elif url:
                            self.batch_log(f"第{line_num}行发现无效链接: {url}", "WARNING")
                else:
                    # 单个链接
                    if self.validate_douyin_url(line):
                        urls.append(line)
                    else:
                        self.batch_log(f"第{line_num}行发现无效链接: {line}", "WARNING")
            
            self.batch_log(f"从配置文件读取到 {len(urls)} 个有效链接")
            return urls
            
        except Exception as e:
            self.batch_log(f"读取URLs配置文件失败: {e}", "ERROR")
            return []
    
    def create_default_urls_config(self):
        """创建默认的URLs配置文件"""
        default_content = """# 抖音用户链接配置文件
# 使用说明：
# 1. 每行一个链接，或者用逗号、分号分隔多个链接
# 2. 以 # 开头的行为注释行，会被忽略
# 3. 支持短链接和完整链接格式

# 示例链接（请替换为实际链接）:
# https://v.douyin.com/iSNbMea7/
# https://www.douyin.com/user/MS4wLjABAAAAk9ajo7ujVMAdMy8gTPNpFtxemAX9XiTFs_oVIzosg8PuREt0dm3gATQ17yhEP48C

# 也可以在一行放多个链接（用逗号分隔）:
# https://v.douyin.com/link1/, https://v.douyin.com/link2/

# 完整格式的链接也支持:
# https://www.douyin.com/user/MS4wLjABAAAA...
"""
        
        with open(self.urls_config_file, "w", encoding="utf-8") as f:
            f.write(default_content)
        
        self.batch_log(f"已创建默认URLs配置文件: {self.urls_config_file}")
    
    def process_single_url(self, url: str, index: int, total: int) -> Dict:
        """处理单个URL的Cookie配置"""
        result = {
            "url": url,
            "index": index,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "message": "",
            "user_id": None,
            "browser_used": None,
            "cookie_fields_count": 0,
            "logged_in": False
        }
        
        self.batch_log(f"[{index}/{total}] 开始处理: {url}")
        
        try:
            # 提取用户ID
            user_id = self.extract_user_id(url)
            if user_id:
                result["user_id"] = user_id
                self.batch_log(f"[{index}/{total}] 检测到用户ID: {user_id}")
            
            # 检查可用浏览器
            available_browsers = self.get_available_browsers()
            
            if not available_browsers:
                result["message"] = "未找到可用的浏览器或rookiepy库未安装"
                self.batch_log(f"[{index}/{total}] ❌ {result['message']}", "ERROR")
                return result
            
            # 获取可用浏览器列表
            available_list = [name for name, available in available_browsers.items() if available]
            if not available_list:
                result["message"] = "没有找到包含抖音Cookie的浏览器"
                self.batch_log(f"[{index}/{total}] ❌ {result['message']}", "WARNING")
                return result
            
            # 尝试从每个浏览器获取Cookie
            for browser_name in available_list:
                self.batch_log(f"[{index}/{total}] 尝试从 {browser_name} 获取Cookie...")
                
                cookie_dict = self.get_cookies_from_browser(browser_name)
                if not cookie_dict:
                    continue
                
                # 验证Cookie
                validation = self.validate_cookie(cookie_dict)
                
                if validation["valid"]:
                    self.batch_log(f"[{index}/{total}] ✅ Cookie验证成功: {validation['message']}")
                    
                    # 转换为字符串
                    cookie_string = self.cookie_dict_to_string(cookie_dict)
                    
                    # 更新配置文件
                    self.update_config_file(cookie_string, browser_name.lower())
                    
                    # 保存详细信息
                    self.save_cookie_info(cookie_dict, url, browser_name)
                    
                    # 更新结果
                    result["success"] = True
                    result["message"] = f"Cookie配置成功 - {validation['message']}"
                    result["browser_used"] = browser_name
                    result["cookie_fields_count"] = len(cookie_dict)
                    result["logged_in"] = validation["logged_in"]
                    
                    self.batch_log(f"[{index}/{total}] ✅ 配置成功 (浏览器: {browser_name}, 字段数: {len(cookie_dict)})")
                    return result
                else:
                    self.batch_log(f"[{index}/{total}] ❌ Cookie验证失败: {validation['message']}", "WARNING")
            
            result["message"] = "所有浏览器都未找到有效的抖音Cookie"
            self.batch_log(f"[{index}/{total}] ❌ {result['message']}", "ERROR")
            
        except Exception as e:
            result["message"] = f"处理过程中发生错误: {str(e)}"
            self.batch_log(f"[{index}/{total}] ❌ {result['message']}", "ERROR")
        
        return result
    
    def save_batch_results(self):
        """保存批量处理结果"""
        try:
            with open(self.batch_result_file, "w", encoding="utf-8") as f:
                json.dump(self.batch_stats, f, ensure_ascii=False, indent=2)
            
            self.batch_log(f"批量处理结果已保存到: {self.batch_result_file}")
        except Exception as e:
            self.batch_log(f"保存批量处理结果失败: {e}", "ERROR")
    
    def show_batch_summary(self):
        """显示批量处理摘要"""
        stats = self.batch_stats
        duration = 0
        
        if stats["start_time"] and stats["end_time"]:
            start = datetime.fromisoformat(stats["start_time"])
            end = datetime.fromisoformat(stats["end_time"])
            duration = (end - start).total_seconds()
        
        self.batch_log("\n" + "="*60)
        self.batch_log("批量处理完成摘要")
        self.batch_log("="*60)
        self.batch_log(f"总链接数: {stats['total_urls']}")
        self.batch_log(f"成功配置: {stats['successful']} ✅")
        self.batch_log(f"配置失败: {stats['failed']} ❌")
        self.batch_log(f"跳过处理: {stats['skipped']} ⏭️")
        self.batch_log(f"处理时长: {duration:.2f} 秒")
        
        if stats["successful"] > 0:
            self.batch_log(f"成功率: {(stats['successful'] / stats['total_urls'] * 100):.1f}%")
        
        # 显示失败的链接
        failed_urls = [r for r in stats["results"] if not r["success"]]
        if failed_urls:
            self.batch_log("\n失败的链接:")
            for result in failed_urls:
                self.batch_log(f"  - {result['url']}: {result['message']}")
        
        # 显示成功的链接
        successful_urls = [r for r in stats["results"] if r["success"]]
        if successful_urls:
            self.batch_log("\n成功配置的链接:")
            for result in successful_urls:
                browser = result.get("browser_used", "未知")
                fields = result.get("cookie_fields_count", 0)
                login_status = "已登录" if result.get("logged_in") else "未登录"
                self.batch_log(f"  - {result['url']} (浏览器: {browser}, 字段: {fields}, 状态: {login_status})")
        
        self.batch_log("="*60)
    
    def run_batch_config(self, delay_seconds: int = 2) -> bool:
        """运行批量配置主流程"""
        self.batch_log("=== 抖音Cookie批量自动配置工具启动 ===")
        
        # 检查URLs配置文件
        if not os.path.exists(self.urls_config_file):
            self.batch_log("URLs配置文件不存在，正在创建默认配置文件...")
            self.create_default_urls_config()
            self.batch_log("请编辑 urls_config.txt 文件，添加需要处理的抖音用户链接", "WARNING")
            return False
        
        # 读取URLs
        urls = self.read_urls_config()
        if not urls:
            self.batch_log("未找到有效的抖音链接，请检查 urls_config.txt 文件", "ERROR")
            return False
        
        # 初始化统计
        self.batch_stats["total_urls"] = len(urls)
        self.batch_stats["start_time"] = datetime.now().isoformat()
        
        self.batch_log(f"准备处理 {len(urls)} 个链接")
        
        # 处理每个URL
        for index, url in enumerate(urls, 1):
            result = self.process_single_url(url, index, len(urls))
            self.batch_stats["results"].append(result)
            
            if result["success"]:
                self.batch_stats["successful"] += 1
            else:
                self.batch_stats["failed"] += 1
            
            # 如果不是最后一个URL，添加延迟避免频繁请求
            if index < len(urls) and delay_seconds > 0:
                self.batch_log(f"等待 {delay_seconds} 秒后处理下一个链接...")
                time.sleep(delay_seconds)
        
        # 完成处理
        self.batch_stats["end_time"] = datetime.now().isoformat()
        
        # 保存结果和显示摘要
        self.save_batch_results()
        self.show_batch_summary()
        
        return self.batch_stats["successful"] > 0
    
    def show_urls_config_status(self):
        """显示URLs配置文件状态"""
        self.batch_log("=== URLs配置文件状态 ===")
        
        if os.path.exists(self.urls_config_file):
            self.batch_log(f"✅ 配置文件存在: {self.urls_config_file}")
            
            urls = self.read_urls_config()
            self.batch_log(f"有效链接数: {len(urls)}")
            
            if urls:
                self.batch_log("链接预览:")
                for i, url in enumerate(urls[:5], 1):  # 只显示前5个
                    user_id = self.extract_user_id(url)
                    user_info = f" (用户ID: {user_id})" if user_id else ""
                    self.batch_log(f"  {i}. {url}{user_info}")
                
                if len(urls) > 5:
                    self.batch_log(f"  ... 还有 {len(urls) - 5} 个链接")
            else:
                self.batch_log("❌ 未找到有效链接")
        else:
            self.batch_log(f"❌ 配置文件不存在: {self.urls_config_file}")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = f"""
=== 抖音Cookie批量自动配置工具使用说明 ===

功能：
- 从 {self.urls_config_file} 批量读取抖音用户链接
- 自动获取Cookie并配置到 {self.cookie_config_file}
- 支持多个链接的批量处理
- 新配置会覆盖原配置
- 详细的处理日志和结果统计

URLs配置文件格式：
- 每行一个链接，或用逗号/分号分隔多个链接
- 以 # 开头的行为注释行
- 支持短链接和完整链接格式

使用方法：
1. 编辑 {self.urls_config_file} 文件，添加抖音用户链接
2. 在浏览器中登录抖音账号
3. 以管理员权限运行：python batch_config_cookie.py
4. 查看处理结果和日志

命令选项：
- python batch_config_cookie.py           # 批量配置Cookie
- python batch_config_cookie.py status    # 查看URLs配置状态
- python batch_config_cookie.py help      # 显示帮助

输出文件：
- {self.cookie_config_file}: Cookie配置文件
- {self.batch_result_file}: 批量处理结果
- {self.batch_log_file}: 批量处理日志

注意事项：
- Windows系统需要管理员权限运行
- 确保已安装 rookiepy 库: pip install rookiepy
- 需要先在浏览器中登录抖音账号
- 批量处理会在每个链接间添加延迟，避免请求过于频繁
"""
        print(help_text)


def main():
    """主函数"""
    manager = BatchDouyinCookieManager()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ["-h", "--help", "help"]:
            manager.show_help()
            return
        elif arg == "status":
            manager.show_urls_config_status()
            manager.show_config_status()  # 继承自父类的方法
            return
    
    # 执行批量配置
    try:
        success = manager.run_batch_config(delay_seconds=3)  # 设置3秒延迟
        
        if success:
            print("\n✅ 批量Cookie配置完成！")
            print(f"配置文件: {manager.cookie_config_file}")
            print(f"处理结果: {manager.batch_result_file}")
            print(f"日志文件: {manager.batch_log_file}")
        else:
            print("\n❌ 批量Cookie配置失败！")
            print("请检查:")
            print("1. urls_config.txt 文件是否包含有效链接")
            print("2. 是否在浏览器中登录了抖音账号")
            print("3. 是否以管理员权限运行程序")
            print("4. 是否安装了 rookiepy 库")
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了批量处理")
        manager.batch_log("用户中断了批量处理", "WARNING")
    except Exception as e:
        print(f"\n❌ 批量处理过程中发生错误: {e}")
        manager.batch_log(f"批量处理过程中发生错误: {e}", "ERROR")


if __name__ == "__main__":
    main()
