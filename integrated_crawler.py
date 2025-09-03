#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音用户信息整合抓取工具
功能：顺序处理urls_config.txt中的链接，先配置Cookie，再抓取用户信息
实现流程：
1. 提取第一条链接 -> 配置Cookie -> 抓取用户信息
2. 提取第二条链接 -> 配置Cookie -> 抓取用户信息
3. 以此类推...
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Union

# 导入Cookie配置管理器
try:
    from batch_config_cookie import BatchDouyinCookieManager
except ImportError:
    print("❌ 无法导入 batch_config_cookie 模块，请确保文件存在")
    sys.exit(1)

# 导入douyin-4的用户信息获取模块
try:
    # 添加douyin-4的lib目录到系统路径
    douyin4_lib_path = os.path.join(os.path.dirname(__file__), '..', 'douyin-4', 'lib')
    douyin4_path = os.path.join(os.path.dirname(__file__), '..', 'douyin-4')
    sys.path.insert(0, douyin4_lib_path)
    sys.path.insert(0, douyin4_path)
    
    import request
    import cookies  
    import util
    from get_user_info import DouyinUserInfo
    
    # 导入所需函数
    Request = request.Request
    get_cookie_dict = cookies.get_cookie_dict
    str_to_path = util.str_to_path
    url_redirect = util.url_redirect
    
except ImportError as e:
    print(f"❌ 无法导入douyin-4模块: {e}")
    print("请确保douyin-4目录存在且包含所需文件")
    sys.exit(1)


class IntegratedDouyinCrawler:
    """整合的抖音爬虫 - 先配置Cookie，再抓取用户信息"""
    
    def __init__(self):
        # 初始化Cookie配置管理器
        self.cookie_manager = BatchDouyinCookieManager()
        
        # 配置文件路径
        self.urls_config_file = os.path.join(os.path.dirname(__file__), "urls_config.txt")
        self.output_dir = "integrated_output"
        self.log_file = "integrated_crawler_log.txt"
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 处理统计
        self.stats = {
            "total_urls": 0,
            "cookie_success": 0,
            "cookie_failed": 0,
            "crawl_success": 0,
            "crawl_failed": 0,
            "start_time": None,
            "end_time": None,
            "results": []
        }
        
        # 当前使用的用户信息获取器
        self.user_getter = None
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] [INTEGRATED] {message}"
        print(log_entry)
        
        # 写入日志文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def read_urls_config(self) -> List[str]:
        """读取URLs配置文件"""
        if not os.path.exists(self.urls_config_file):
            self.log(f"URLs配置文件不存在: {self.urls_config_file}", "ERROR")
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
                    split_urls = re.split(r'[,;]', line)
                    for url in split_urls:
                        url = url.strip()
                        if url and self.cookie_manager.validate_douyin_url(url):
                            urls.append(url)
                        elif url:
                            self.log(f"第{line_num}行发现无效链接: {url}", "WARNING")
                else:
                    # 单个链接
                    if self.cookie_manager.validate_douyin_url(line):
                        urls.append(line)
                    else:
                        self.log(f"第{line_num}行发现无效链接: {line}", "WARNING")
            
            self.log(f"从配置文件读取到 {len(urls)} 个有效链接")
            return urls
            
        except Exception as e:
            self.log(f"读取URLs配置文件失败: {e}", "ERROR")
            return []
    
    def configure_cookie_for_url(self, url: str, index: int, total: int) -> bool:
        """为指定URL配置Cookie"""
        self.log(f"[{index}/{total}] 开始为链接配置Cookie: {url}")
        
        try:
            # 使用Cookie管理器的单个URL处理方法
            result = self.cookie_manager.process_single_url(url, index, total)
            
            if result["success"]:
                self.log(f"[{index}/{total}] ✅ Cookie配置成功")
                self.stats["cookie_success"] += 1
                return True
            else:
                self.log(f"[{index}/{total}] ❌ Cookie配置失败: {result['message']}", "ERROR")
                self.stats["cookie_failed"] += 1
                return False
                
        except Exception as e:
            self.log(f"[{index}/{total}] ❌ Cookie配置异常: {e}", "ERROR")
            self.stats["cookie_failed"] += 1
            return False
    
    def load_cookie_from_config(self):
        """从配置文件加载Cookie字符串"""
        cookie_config_file = self.cookie_manager.cookie_config_file
        
        if not os.path.exists(cookie_config_file):
            self.log(f"Cookie配置文件不存在: {cookie_config_file}", "ERROR")
            return None
        
        try:
            with open(cookie_config_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # 解析cookie配置
                if line.startswith('cookie='):
                    cookie = line[7:].strip()  # 移除'cookie='前缀
                    if cookie and cookie != "your_cookie_string_here":
                        self.log("✅ 从配置文件读取到有效Cookie")
                        return cookie
                
                elif line.startswith('browser='):
                    browser = line[8:].strip()  # 移除'browser='前缀
                    if browser in ['chrome', 'edge']:
                        self.log(f"⚠️ 发现浏览器配置，但需要具体的Cookie字符串: {browser}")
            
            self.log("❌ 配置文件中未找到有效的Cookie字符串", "ERROR")
            return None
            
        except Exception as e:
            self.log(f"读取Cookie配置文件失败: {e}", "ERROR")
            return None
    
    def crawl_user_info(self, url: str, index: int, total: int) -> Optional[Dict]:
        """抓取用户信息"""
        self.log(f"[{index}/{total}] 开始抓取用户信息: {url}")
        
        try:
            # 获取当前Cookie
            cookie = self.load_cookie_from_config()
            if not cookie:
                self.log(f"[{index}/{total}] ❌ 无法获取有效Cookie，跳过抓取", "ERROR")
                return None
            
            # 初始化或重新初始化用户信息获取器
            self.user_getter = DouyinUserInfo(cookie)
            
            # 获取用户信息
            user_info = self.user_getter.get_user_info_from_url(url)
            
            if user_info:
                self.log(f"[{index}/{total}] ✅ 用户信息获取成功")
                self.log(f"[{index}/{total}]    👤 昵称: {user_info.get('nickname', '未知')}")
                self.log(f"[{index}/{total}]    📝 签名: {user_info.get('signature', '无')}")
                self.log(f"[{index}/{total}]    🌍 地区: {user_info.get('ip_location', '未知')}")
                self.log(f"[{index}/{total}]    👥 粉丝: {user_info.get('follower_count', 0)}")
                
                self.stats["crawl_success"] += 1
                return user_info
            else:
                self.log(f"[{index}/{total}] ❌ 用户信息获取失败", "ERROR")
                self.stats["crawl_failed"] += 1
                return None
                
        except Exception as e:
            self.log(f"[{index}/{total}] ❌ 抓取用户信息异常: {e}", "ERROR")
            self.stats["crawl_failed"] += 1
            return None
    
    def save_user_info(self, user_info: Dict, url: str, index: int) -> Optional[str]:
        """保存用户信息到文件"""
        try:
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nickname = user_info.get('nickname', '未知用户')
            safe_nickname = str_to_path(nickname)  # 转换为安全的文件名
            
            # 限制昵称长度
            if len(safe_nickname) > 20:
                safe_nickname = safe_nickname[:20]
            
            filename = f"{timestamp}_{index:03d}_{safe_nickname}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            # 准备输出数据
            output_data = {
                'extraction_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source_url': url,
                'processing_index': index,
                'user_info': user_info
            }
            
            # 保存到文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            self.log(f"✅ 用户信息已保存: {filename}")
            return filepath
            
        except Exception as e:
            self.log(f"❌ 保存用户信息失败: {e}", "ERROR")
            return None
    
    def process_single_url(self, url: str, index: int, total: int) -> Dict:
        """处理单个URL的完整流程：配置Cookie -> 抓取用户信息"""
        result = {
            "url": url,
            "index": index,
            "timestamp": datetime.now().isoformat(),
            "cookie_success": False,
            "crawl_success": False,
            "user_info": None,
            "filepath": None,
            "error_message": None
        }
        
        self.log(f"\n{'='*60}")
        self.log(f"[{index}/{total}] 开始处理链接: {url}")
        self.log(f"{'='*60}")
        
        # 第一步：配置Cookie
        self.log(f"[{index}/{total}] 步骤1: 配置Cookie")
        cookie_success = self.configure_cookie_for_url(url, index, total)
        result["cookie_success"] = cookie_success
        
        if not cookie_success:
            result["error_message"] = "Cookie配置失败"
            self.log(f"[{index}/{total}] ❌ 由于Cookie配置失败，跳过用户信息抓取")
            return result
        
        # 添加延迟，确保Cookie配置生效
        self.log(f"[{index}/{total}] 等待2秒，确保Cookie配置生效...")
        time.sleep(2)
        
        # 第二步：抓取用户信息
        self.log(f"[{index}/{total}] 步骤2: 抓取用户信息")
        user_info = self.crawl_user_info(url, index, total)
        
        if user_info:
            result["crawl_success"] = True
            result["user_info"] = user_info
            
            # 第三步：保存用户信息
            self.log(f"[{index}/{total}] 步骤3: 保存用户信息")
            filepath = self.save_user_info(user_info, url, index)
            result["filepath"] = filepath
            
            if filepath:
                self.log(f"[{index}/{total}] ✅ 链接处理完成")
            else:
                result["error_message"] = "保存文件失败"
                self.log(f"[{index}/{total}] ⚠️ 抓取成功但保存失败")
        else:
            result["error_message"] = "用户信息抓取失败"
            self.log(f"[{index}/{total}] ❌ 用户信息抓取失败")
        
        return result
    
    def run_integrated_crawl(self, delay_seconds: int = 5) -> bool:
        """运行整合爬虫的主流程"""
        self.log("=== 抖音用户信息整合抓取工具启动 ===")
        
        # 读取URLs
        urls = self.read_urls_config()
        if not urls:
            self.log("未找到有效的抖音链接，请检查 urls_config.txt 文件", "ERROR")
            return False
        
        # 初始化统计
        self.stats["total_urls"] = len(urls)
        self.stats["start_time"] = datetime.now().isoformat()
        
        self.log(f"准备按顺序处理 {len(urls)} 个链接")
        
        # 顺序处理每个URL
        for index, url in enumerate(urls, 1):
            result = self.process_single_url(url, index, len(urls))
            self.stats["results"].append(result)
            
            # 如果不是最后一个URL，添加延迟
            if index < len(urls):
                self.log(f"等待 {delay_seconds} 秒后处理下一个链接...")
                time.sleep(delay_seconds)
        
        # 完成处理
        self.stats["end_time"] = datetime.now().isoformat()
        
        # 生成统计报告
        self.generate_final_report()
        
        return self.stats["crawl_success"] > 0
    
    def generate_final_report(self):
        """生成最终统计报告"""
        stats = self.stats
        duration = 0
        
        if stats["start_time"] and stats["end_time"]:
            start = datetime.fromisoformat(stats["start_time"])
            end = datetime.fromisoformat(stats["end_time"])
            duration = (end - start).total_seconds()
        
        self.log("\n" + "="*70)
        self.log("整合抓取完成统计报告")
        self.log("="*70)
        self.log(f"总链接数: {stats['total_urls']}")
        self.log(f"Cookie配置成功: {stats['cookie_success']} ✅")
        self.log(f"Cookie配置失败: {stats['cookie_failed']} ❌")
        self.log(f"用户信息抓取成功: {stats['crawl_success']} ✅")
        self.log(f"用户信息抓取失败: {stats['crawl_failed']} ❌")
        self.log(f"总处理时长: {duration:.2f} 秒")
        
        if stats["total_urls"] > 0:
            cookie_rate = (stats["cookie_success"] / stats["total_urls"] * 100)
            crawl_rate = (stats["crawl_success"] / stats["total_urls"] * 100)
            self.log(f"Cookie配置成功率: {cookie_rate:.1f}%")
            self.log(f"信息抓取成功率: {crawl_rate:.1f}%")
        
        # 显示成功抓取的用户
        successful_results = [r for r in stats["results"] if r["crawl_success"]]
        if successful_results:
            self.log("\n成功抓取的用户:")
            for result in successful_results:
                user_info = result.get("user_info", {})
                nickname = user_info.get("nickname", "未知")
                follower_count = user_info.get("follower_count", 0)
                filepath = result.get("filepath", "未保存")
                self.log(f"  - {nickname} (粉丝: {follower_count}, 文件: {os.path.basename(filepath)})")
        
        # 显示失败的链接
        failed_results = [r for r in stats["results"] if not r["crawl_success"]]
        if failed_results:
            self.log("\n处理失败的链接:")
            for result in failed_results:
                error_msg = result.get("error_message", "未知错误")
                self.log(f"  - {result['url']}: {error_msg}")
        
        # 保存详细报告
        report_data = {
            'summary': {
                'total_urls': stats['total_urls'],
                'cookie_success': stats['cookie_success'],
                'cookie_failed': stats['cookie_failed'],
                'crawl_success': stats['crawl_success'],
                'crawl_failed': stats['crawl_failed'],
                'processing_time_seconds': round(duration, 2),
                'start_time': stats['start_time'],
                'end_time': stats['end_time']
            },
            'results': stats['results']
        }
        
        report_filename = f"integrated_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_filepath = os.path.join(self.output_dir, report_filename)
        
        try:
            with open(report_filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            self.log(f"📋 详细报告已保存: {report_filename}")
        except Exception as e:
            self.log(f"⚠️ 保存报告失败: {e}", "WARNING")
        
        self.log("="*70)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = f"""
=== 抖音用户信息整合抓取工具使用说明 ===

功能：
- 从 {self.urls_config_file} 顺序读取抖音用户链接
- 对每个链接依次执行：
  1. 配置Cookie
  2. 抓取用户信息
  3. 保存到文件
- 确保每个链接都有最新的Cookie

使用方法：
1. 编辑 {self.urls_config_file} 文件，添加抖音用户链接
2. 在浏览器中登录抖音账号
3. 以管理员权限运行：python integrated_crawler.py
4. 查看输出目录中的结果文件

输出文件：
- {self.output_dir}/: 用户信息JSON文件
- integrated_report_*.json: 处理统计报告
- {self.log_file}: 运行日志

注意事项：
- Windows系统需要管理员权限运行
- 确保已安装 rookiepy 库
- 需要先在浏览器中登录抖音账号
- 程序会在每个链接间添加延迟，避免请求过于频繁
"""
        print(help_text)


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ["-h", "--help", "help"]:
            crawler = IntegratedDouyinCrawler()
            crawler.show_help()
            return
    
    # 创建爬虫实例
    crawler = IntegratedDouyinCrawler()
    
    try:
        # 运行整合爬虫
        success = crawler.run_integrated_crawl(delay_seconds=5)  # 设置5秒延迟
        
        if success:
            print("\n✅ 整合抓取完成！")
            print(f"输出目录: {crawler.output_dir}")
            print(f"日志文件: {crawler.log_file}")
        else:
            print("\n❌ 整合抓取失败！")
            print("请检查:")
            print("1. urls_config.txt 文件是否包含有效链接")
            print("2. 是否在浏览器中登录了抖音账号")
            print("3. 是否以管理员权限运行程序")
            print("4. 是否安装了 rookiepy 库")
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了处理过程")
        crawler.log("用户中断了处理过程", "WARNING")
    except Exception as e:
        print(f"\n❌ 处理过程中发生错误: {e}")
        crawler.log(f"处理过程中发生错误: {e}", "ERROR")


if __name__ == "__main__":
    main()
