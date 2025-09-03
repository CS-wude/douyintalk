#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音用户终极爬虫工具 - Ultimate Crawler
整合Cookie配置、用户信息抓取和AI话术生成的完整解决方案
实现流程：URL -> Cookie配置 -> 用户信息抓取 -> AI话术生成 -> 下一个URL
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Union

# Coze SDK导入
try:
    from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL
except ImportError:
    print("❌ 请先安装 cozepy 库: pip install cozepy")
    exit(1)

# 导入Cookie配置管理器
try:
    from batch_config_cookie import BatchDouyinCookieManager
except ImportError:
    print("❌ 无法导入 batch_config_cookie 模块，请确保文件存在")
    sys.exit(1)

# 导入本地的抖音用户信息获取模块
try:
    import douyin_request as request
    import douyin_cookies as cookies  
    import douyin_util as util
    from douyin_get_user_info import DouyinUserInfo
    
    # 导入所需函数
    Request = request.Request
    get_cookie_dict = cookies.get_cookie_dict
    str_to_path = util.str_to_path
    url_redirect = util.url_redirect
    
except ImportError as e:
    print(f"❌ 无法导入抖音模块: {e}")
    print("请确保所有必需的模块文件存在于当前目录")
    sys.exit(1)


class UltimateCrawler:
    """抖音用户终极爬虫 - 一站式完整解决方案"""
    
    def __init__(self, coze_api_token: str, bot_id: str):
        # Coze API配置
        self.coze_api_token = coze_api_token
        self.bot_id = bot_id
        self.user_id = '123456789'
        
        # 初始化Coze客户端
        self.coze = Coze(
            auth=TokenAuth(token=self.coze_api_token), 
            base_url=COZE_CN_BASE_URL
        )
        
        # 文件和目录配置
        self.urls_config_file = "urls_config.txt"
        self.cookie_config_file = os.path.join("config", "cookie_config.txt")
        self.user_output_dir = "integrated_output"
        self.talk_output_dir = "Talk_output"
        self.log_file = "ultimate_crawler_log.txt"
        
        # 创建输出目录
        os.makedirs(self.user_output_dir, exist_ok=True)
        os.makedirs(self.talk_output_dir, exist_ok=True)
        os.makedirs("config", exist_ok=True)
        
        # 初始化Cookie管理器
        self.cookie_manager = BatchDouyinCookieManager()
        
        # 统计信息
        self.stats = {
            "total_urls": 0,
            "success_count": 0,
            "failed_count": 0,
            "cookie_success": 0,
            "crawl_success": 0,
            "ai_success": 0,
            "start_time": None,
            "end_time": None,
            "results": []
        }
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        # 写入日志文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def read_urls_config(self) -> List[str]:
        """读取URLs配置文件"""
        if not os.path.exists(self.urls_config_file):
            self.log(f"配置文件不存在: {self.urls_config_file}", "ERROR")
            return []
        
        urls = []
        try:
            with open(self.urls_config_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # 跳过空行和注释行
                    if not line or line.startswith('#'):
                        continue
                    
                    # 处理逗号分隔的多个链接
                    if ',' in line:
                        line_urls = [url.strip() for url in line.split(',') if url.strip()]
                        urls.extend(line_urls)
                    else:
                        urls.append(line)
            
            self.log(f"从配置文件读取到 {len(urls)} 个链接")
            return urls
            
        except Exception as e:
            self.log(f"读取配置文件失败: {e}", "ERROR")
            return []
    
    def configure_cookie_for_url(self, url: str, index: int) -> bool:
        """为指定URL配置Cookie"""
        try:
            self.log(f"开始配置Cookie: {url}")
            
            # 使用Cookie管理器配置单个URL
            success = self.cookie_manager.process_single_url(url, index, self.stats["total_urls"])
            
            if success:
                self.log("✅ Cookie配置成功")
                return True
            else:
                self.log("❌ Cookie配置失败", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"Cookie配置异常: {e}", "ERROR")
            return False
    
    def load_cookie_from_config(self) -> Optional[str]:
        """从配置文件加载Cookie"""
        try:
            if not os.path.exists(self.cookie_config_file):
                self.log("Cookie配置文件不存在", "ERROR")
                return None
            
            with open(self.cookie_config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('cookie='):
                        cookie = line[7:]  # 移除 'cookie=' 前缀
                        return cookie
            
            self.log("在配置文件中未找到cookie配置", "ERROR")
            return None
            
        except Exception as e:
            self.log(f"加载Cookie失败: {e}", "ERROR")
            return None
    
    def extract_user_info(self, url: str, index: int) -> Optional[Dict]:
        """提取用户信息"""
        try:
            self.log(f"开始提取用户信息: {url}")
            
            # 加载Cookie
            cookie_str = self.load_cookie_from_config()
            if not cookie_str:
                self.log("无法获取Cookie，跳过用户信息提取", "ERROR")
                return None
            
            # 创建用户信息提取器
            user_info_getter = DouyinUserInfo(cookie_str)
            
            # 提取用户信息
            user_info = user_info_getter.get_user_info_from_url(url)
            
            if user_info and user_info.get('nickname'):
                self.log(f"✅ 用户信息提取成功: {user_info.get('nickname')}")
                
                # 保存用户信息到JSON文件
                self.save_user_info(user_info, url, index)
                return user_info
            else:
                self.log("❌ 用户信息提取失败或为空", "WARNING")
                return None
                
        except Exception as e:
            self.log(f"用户信息提取异常: {e}", "ERROR")
            return None
    
    def save_user_info(self, user_info: Dict, url: str, index: int):
        """保存用户信息到JSON文件"""
        try:
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nickname = user_info.get('nickname', 'unknown')
            safe_nickname = str_to_path(nickname)
            filename = f"{timestamp}_{index:03d}_{safe_nickname}.json"
            filepath = os.path.join(self.user_output_dir, filename)
            
            # 构建完整的用户信息数据
            output_data = {
                "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_url": url,
                "processing_index": index,
                "user_info": user_info
            }
            
            # 保存到文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            self.log(f"✅ 用户信息已保存: {filename}")
            return filepath
            
        except Exception as e:
            self.log(f"保存用户信息失败: {e}", "ERROR")
            return None
    
    def clean_user_info_for_json(self, user_info: Dict) -> Dict:
        """清理用户信息中的特殊字符，确保JSON解析正常"""
        cleaned_info = {}
        
        for key, value in user_info.items():
            if isinstance(value, str):
                # 移除或替换控制字符，但保留常见的可见字符
                cleaned_value = ""
                for char in value:
                    char_code = ord(char)
                    if char_code >= 32:  # 可见字符
                        cleaned_value += char
                    elif char in ['\n', '\r', '\t']:  # 保留常见的格式字符，但转为空格或标记
                        if char == '\n':
                            cleaned_value += ' '  # 换行转为空格
                        elif char == '\r':
                            cleaned_value += ' '  # 回车转为空格
                        elif char == '\t':
                            cleaned_value += ' '  # 制表符转为空格
                    # 其他控制字符直接忽略
                
                # 清理多余的空格
                cleaned_value = ' '.join(cleaned_value.split())
                cleaned_info[key] = cleaned_value
            else:
                cleaned_info[key] = value
                
        return cleaned_info
    
    def generate_ai_talk(self, user_info: Dict, index: int, url: str) -> Optional[str]:
        """生成AI话术"""
        try:
            nickname = user_info.get('nickname', '未知用户')
            self.log(f"开始生成AI话术: {nickname}")
            
            # 清理用户信息中的特殊字符
            cleaned_user_info = self.clean_user_info_for_json(user_info)
            
            # 构建完整的JSON字符串作为输入（包含所有字段）
            complete_json_data = {
                "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_url": url,
                "processing_index": index,
                "user_info": cleaned_user_info
            }
            
            # 将完整JSON转换为字符串
            json_input = json.dumps(complete_json_data, ensure_ascii=False, indent=2)
            
            # 验证生成的JSON是否有效
            try:
                json.loads(json_input)  # 测试解析
                self.log(f"✅ JSON验证成功，发送给Coze的内容长度: {len(json_input)} 字符")
            except json.JSONDecodeError as e:
                self.log(f"❌ JSON验证失败: {e}", "ERROR")
                return None
            
            # 调用Coze API
            talk_content = ""
            
            for event in self.coze.chat.stream(
                bot_id=self.bot_id,
                user_id=self.user_id,
                additional_messages=[
                    Message.build_user_question_text(json_input),
                ],
            ):
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    talk_content += event.message.content
                
                if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                    self.log(f"API调用完成，token使用量: {event.chat.usage.token_count if event.chat.usage else '未知'}")
                    break
            
            # 清理生成的内容
            talk_content = talk_content.strip()
            
            if talk_content:
                self.log(f"✅ AI话术生成成功，长度: {len(talk_content)} 字")
                
                # 保存话术到文件
                self.save_ai_talk(talk_content, user_info, index)
                return talk_content
            else:
                self.log("❌ 生成的话术为空", "WARNING")
                return None
                
        except Exception as e:
            self.log(f"AI话术生成失败: {e}", "ERROR")
            return None
    
    def save_ai_talk(self, talk_content: str, user_info: Dict, index: int):
        """保存AI话术到文件"""
        try:
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nickname = user_info.get('nickname', 'unknown')
            safe_nickname = str_to_path(nickname)
            filename = f"{timestamp}_{index:03d}_{safe_nickname}.txt"
            filepath = os.path.join(self.talk_output_dir, filename)
            
            # 准备输出内容
            output_content = f"""# 抖音用户AI打招呼话术
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 用户昵称: {nickname}
# 处理序号: {index}

{talk_content}
"""
            
            # 保存到文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            self.log(f"✅ AI话术已保存: {filename}")
            
        except Exception as e:
            self.log(f"保存AI话术失败: {e}", "ERROR")
    
    def process_single_url(self, url: str, index: int) -> Dict:
        """处理单个URL的完整流程"""
        result = {
            "url": url,
            "index": index,
            "timestamp": datetime.now().isoformat(),
            "cookie_success": False,
            "crawl_success": False,
            "ai_success": False,
            "user_info": None,
            "ai_talk": None,
            "error_message": None
        }
        
        try:
            self.log(f"\n{'='*60}")
            self.log(f"[{index}/{self.stats['total_urls']}] 开始处理URL: {url}")
            self.log(f"{'='*60}")
            
            # 步骤1: 配置Cookie
            self.log(f"[{index}/{self.stats['total_urls']}] 步骤1: 配置Cookie")
            cookie_success = self.configure_cookie_for_url(url, index)
            result["cookie_success"] = cookie_success
            
            if not cookie_success:
                result["error_message"] = "Cookie配置失败"
                self.log(f"[{index}/{self.stats['total_urls']}] ❌ Cookie配置失败，跳过后续步骤")
                return result
            
            self.stats["cookie_success"] += 1
            
            # 延迟避免请求过频
            time.sleep(3)
            
            # 步骤2: 提取用户信息
            self.log(f"[{index}/{self.stats['total_urls']}] 步骤2: 提取用户信息")
            user_info = self.extract_user_info(url, index)
            result["user_info"] = user_info
            
            if not user_info:
                result["error_message"] = "用户信息提取失败"
                self.log(f"[{index}/{self.stats['total_urls']}] ❌ 用户信息提取失败，跳过AI话术生成")
                return result
            
            result["crawl_success"] = True
            self.stats["crawl_success"] += 1
            
            # 延迟避免API调用过频
            time.sleep(2)
            
            # 步骤3: 生成AI话术
            self.log(f"[{index}/{self.stats['total_urls']}] 步骤3: 生成AI话术")
            ai_talk = self.generate_ai_talk(user_info, index, url)
            result["ai_talk"] = ai_talk
            
            if ai_talk:
                result["ai_success"] = True
                self.stats["ai_success"] += 1
                self.log(f"[{index}/{self.stats['total_urls']}] ✅ 完整流程成功完成")
            else:
                result["error_message"] = "AI话术生成失败"
                self.log(f"[{index}/{self.stats['total_urls']}] ⚠️ AI话术生成失败，但用户信息已获取")
            
            return result
            
        except Exception as e:
            result["error_message"] = f"处理异常: {str(e)}"
            self.log(f"[{index}/{self.stats['total_urls']}] ❌ 处理异常: {e}", "ERROR")
            return result
    
    def process_all_urls(self) -> bool:
        """处理所有URL"""
        self.log("=== 抖音用户终极爬虫启动 ===")
        
        # 读取URL配置
        urls = self.read_urls_config()
        if not urls:
            self.log("未找到有效的URL配置", "ERROR")
            return False
        
        # 初始化统计
        self.stats["total_urls"] = len(urls)
        self.stats["start_time"] = datetime.now().isoformat()
        
        self.log(f"找到 {len(urls)} 个待处理的URL")
        
        # 逐个处理URL
        for i, url in enumerate(urls, 1):
            try:
                result = self.process_single_url(url, i)
                self.stats["results"].append(result)
                
                # 更新成功计数
                if result["ai_success"]:
                    self.stats["success_count"] += 1
                else:
                    self.stats["failed_count"] += 1
                
                # 处理间隔
                if i < len(urls):
                    self.log(f"等待5秒后处理下一个URL...")
                    time.sleep(5)
                    
            except KeyboardInterrupt:
                self.log("用户中断了处理过程", "WARNING")
                break
            except Exception as e:
                self.log(f"处理URL异常: {e}", "ERROR")
                self.stats["failed_count"] += 1
        
        # 完成处理
        self.stats["end_time"] = datetime.now().isoformat()
        
        # 生成最终报告
        self.generate_final_report()
        
        return self.stats["success_count"] > 0
    
    def generate_final_report(self):
        """生成最终统计报告"""
        stats = self.stats
        duration = 0
        
        if stats["start_time"] and stats["end_time"]:
            start = datetime.fromisoformat(stats["start_time"])
            end = datetime.fromisoformat(stats["end_time"])
            duration = (end - start).total_seconds()
        
        # 生成报告文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"ultimate_crawler_report_{timestamp}.json"
        report_path = os.path.join(self.user_output_dir, report_filename)
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "summary": {
                        "total_urls": stats["total_urls"],
                        "success_count": stats["success_count"],
                        "failed_count": stats["failed_count"],
                        "cookie_success": stats["cookie_success"],
                        "crawl_success": stats["crawl_success"],
                        "ai_success": stats["ai_success"],
                        "processing_time_seconds": round(duration, 2),
                        "start_time": stats["start_time"],
                        "end_time": stats["end_time"]
                    },
                    "results": stats["results"]
                }, f, ensure_ascii=False, indent=2)
            
            self.log(f"✅ 处理报告已保存: {report_filename}")
            
        except Exception as e:
            self.log(f"保存处理报告失败: {e}", "ERROR")
        
        # 打印统计信息
        self.log("\n" + "="*60)
        self.log("终极爬虫处理完成统计报告")
        self.log("="*60)
        self.log(f"总URL数: {stats['total_urls']}")
        self.log(f"Cookie成功: {stats['cookie_success']} ✅")
        self.log(f"信息抓取成功: {stats['crawl_success']} ✅")
        self.log(f"AI话术成功: {stats['ai_success']} ✅")
        self.log(f"完整流程成功: {stats['success_count']} ✅")
        self.log(f"处理失败: {stats['failed_count']} ❌")
        self.log(f"总处理时长: {duration:.2f} 秒")
        
        if stats["total_urls"] > 0:
            success_rate = (stats["success_count"] / stats["total_urls"] * 100)
            self.log(f"完整成功率: {success_rate:.1f}%")
        
        self.log(f"用户信息输出: {self.user_output_dir}")
        self.log(f"AI话术输出: {self.talk_output_dir}")
        self.log("="*60)


def load_coze_config():
    """加载Coze API配置"""
    config_file = "coze_config.json"
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('coze_api_token'), config.get('bot_id')
    except FileNotFoundError:
        print(f"❌ 配置文件 {config_file} 不存在")
        print("请先创建配置文件或直接在代码中配置API信息")
        return None, None
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return None, None


def main():
    """主函数"""
    # 尝试从配置文件加载
    coze_api_token, bot_id = load_coze_config()
    
    # 如果配置文件加载失败，使用默认配置
    if not coze_api_token or not bot_id:
        print("使用代码中的默认配置...")
        # Coze API配置 - 请替换为你的有效token
        coze_api_token = 'your_coze_api_token_here'  # 替换为你的新token
        bot_id = '7544946933597732864'  # 替换为你的Bot ID
    
    # 验证配置
    if coze_api_token == 'your_coze_api_token_here':
        print("❌ 请配置有效的 Coze API Token！")
        print("\n配置方法：")
        print("1. 编辑 coze_config.json 文件")
        print("2. 或直接修改 ultimate_crawler.py 中的token")
        return
    
    # 创建终极爬虫实例
    crawler = UltimateCrawler(coze_api_token, bot_id)
    
    try:
        # 处理所有URL
        success = crawler.process_all_urls()
        
        if success:
            print(f"\n✅ 终极爬虫处理完成！")
            print(f"用户信息输出: {crawler.user_output_dir}")
            print(f"AI话术输出: {crawler.talk_output_dir}")
            print(f"日志文件: {crawler.log_file}")
        else:
            print(f"\n❌ 终极爬虫处理失败！")
            print("请检查:")
            print("1. urls_config.txt 是否包含有效的抖音用户链接")
            print("2. Coze API token 是否有效")
            print("3. Bot ID 是否正确")
            print("4. 网络连接是否正常")
            print("5. 浏览器中是否已登录抖音账号")
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了处理过程")
        crawler.log("用户中断了处理过程", "WARNING")
    except Exception as e:
        print(f"\n❌ 处理过程中发生错误: {e}")
        crawler.log(f"处理过程中发生错误: {e}", "ERROR")


if __name__ == "__main__":
    main()
