#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音用户作品URL获取工具
功能：根据抖音用户主页链接，获取该用户的所有作品视频URL
"""

import os
import sys
import json
import time
from datetime import datetime
from urllib.parse import urlparse, unquote
from typing import List, Dict, Optional

# 导入所需的模块
try:
    # 导入本地的抖音模块
    import douyin_request as request
    import douyin_cookies as cookies  
    import douyin_util as util
except ImportError:
    print("❌ 找不到所需的模块，尝试使用相对路径导入...")
    sys.path.insert(0, os.path.dirname(__file__))
    try:
        import douyin_request as request
        import douyin_cookies as cookies  
        import douyin_util as util
    except ImportError:
        print("❌ 导入模块失败，请确保文件存在")
        sys.exit(1)

# 导入所需函数
Request = request.Request
get_cookie_dict = cookies.get_cookie_dict
str_to_path = util.str_to_path
url_redirect = util.url_redirect


class DouyinVideoURLGetter:
    """抖音用户作品URL获取器"""
    
    def __init__(self, cookie: str = ''):
        """
        初始化获取器
        
        Args:
            cookie: Cookie字符串或配置
        """
        self.cookie = cookie
        self.request = Request(cookie)
        self.results = []
        self.has_more = True
        
    def extract_user_id_from_url(self, url: str) -> Optional[str]:
        """从抖音链接中提取用户ID"""
        try:
            # 处理短链接重定向
            if 'v.douyin.com' in url:
                url = url_redirect(url)
            
            # 提取sec_user_id
            if '/user/' in url:
                path = urlparse(url).path
                user_id = path.split('/user/')[-1].split('?')[0]
                return user_id
            else:
                print("❌ 无法从URL中提取用户ID，请检查链接格式")
                return None
                
        except Exception as e:
            print(f"❌ URL解析失败: {e}")
            return None
    
    def get_user_videos(self, sec_user_id: str, max_videos: int = 0) -> List[Dict]:
        """获取用户的所有视频作品URL"""
        print(f"📥 开始获取用户 {sec_user_id} 的视频作品...")
        
        max_cursor = 0
        retry_count = 0
        max_retry = 5
        all_videos = []
        
        while self.has_more:
            try:
                # 构造请求参数
                uri = '/aweme/v1/web/aweme/post/'
                params = {
                    "publish_video_strategy_type": 2,
                    "max_cursor": max_cursor,
                    "locate_query": False,
                    'show_live_replay_strategy': 1,
                    'need_time_list': 0,
                    'time_list_query': 0,
                    'whale_cut_token': '',
                    'count': 18,
                    "sec_user_id": sec_user_id
                }
                
                # 发送请求
                resp = self.request.getJSON(uri, params)
                if not resp:
                    retry_count += 1
                    print(f"⚠️ 请求失败，第 {retry_count}/{max_retry} 次重试...")
                    if retry_count >= max_retry:
                        print("❌ 达到最大重试次数，停止获取")
                        break
                    time.sleep(2)  # 等待2秒后重试
                    continue
                
                # 重置重试计数
                retry_count = 0
                
                # 获取下一页的cursor
                max_cursor = resp.get('max_cursor', 0)
                
                # 检查是否还有更多数据
                self.has_more = resp.get('has_more', 0)
                
                # 提取视频列表
                aweme_list = resp.get('aweme_list', [])
                if not aweme_list:
                    print("ℹ️ 未找到更多作品")
                    break
                
                # 处理视频信息
                for item in aweme_list:
                    # 提取视频信息
                    video_info = self.extract_video_info(item)
                    if video_info:
                        all_videos.append(video_info)
                        print(f"✅ 获取到视频: {video_info['desc']} [ID: {video_info['id']}]")
                
                # 显示进度
                print(f"🔄 已获取 {len(all_videos)} 个视频, 是否继续: {self.has_more}")
                
                # 检查是否达到上限
                if max_videos > 0 and len(all_videos) >= max_videos:
                    print(f"🛑 已达到设定的最大视频数量 {max_videos}")
                    break
                
                # 添加延迟，避免请求过快
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ 获取视频列表失败: {e}")
                retry_count += 1
                if retry_count >= max_retry:
                    print("❌ 达到最大重试次数，停止获取")
                    break
                time.sleep(2)
        
        print(f"✅ 获取完成，共获取到 {len(all_videos)} 个视频作品")
        self.results = all_videos
        return all_videos
    
    def extract_video_info(self, item: Dict) -> Optional[Dict]:
        """从作品数据中提取视频信息"""
        try:
            # 处理视频类型
            _type = item.get('aweme_type', item.get('awemeType'))
            
            # 只提取视频类型的作品
            if _type <= 66 or _type in [69, 107]:  # 视频类型
                video_info = {
                    'id': item.get('aweme_id', item.get('awemeId', '')),
                    'desc': item.get('desc', '无标题'),
                    'create_time': item.get('create_time', 0),
                    'type': _type
                }
                
                # 提取视频下载地址
                play_addr = item['video'].get('play_addr')
                if play_addr:
                    video_info['url'] = play_addr['url_list'][-1]
                else:
                    video_info['url'] = item['download']['urlList'][-1].replace('watermark=1', 'watermark=0')
                
                # 提取封面图
                cover = item['video'].get('cover')
                if isinstance(cover, dict):
                    video_info['cover'] = cover['url_list'][-1]
                else:
                    video_info['cover'] = f"https:{item['video']['dynamicCover']}"
                
                # 统计信息
                stats = item.get('statistics', {})
                video_info['play_count'] = stats.get('play_count', 0)
                video_info['digg_count'] = stats.get('digg_count', 0)
                video_info['comment_count'] = stats.get('comment_count', 0)
                
                return video_info
            else:
                # 不是视频类型，跳过
                return None
                
        except Exception as e:
            print(f"❌ 提取视频信息失败: {e}")
            return None
    
    def get_videos_from_user_url(self, user_url: str, max_videos: int = 0) -> List[Dict]:
        """根据用户主页URL获取视频作品列表"""
        print(f"🔍 分析用户链接: {user_url}")
        
        # 提取用户ID
        sec_user_id = self.extract_user_id_from_url(user_url)
        if not sec_user_id:
            return []
        
        print(f"✅ 提取到用户ID: {sec_user_id}")
        
        # 获取用户视频
        return self.get_user_videos(sec_user_id, max_videos)
    
    def save_to_file(self, filename: str = "video_urls.json"):
        """保存视频信息到文件"""
        if not self.results:
            print("❌ 没有视频数据可保存")
            return False
        
        try:
            # 准备输出数据
            output_data = {
                "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_videos": len(self.results),
                "videos": self.results
            }
            
            # 保存到文件
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 已保存视频信息到: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False


def load_cookie_from_config(cookie_config_file: str = 'config/cookie.json') -> str:
    """从配置文件加载Cookie"""
    try:
        if not os.path.exists(cookie_config_file):
            print(f"⚠️ Cookie配置文件 {cookie_config_file} 不存在")
            return ''
        
        with open(cookie_config_file, 'r', encoding='utf-8') as f:
            cookie_json = json.load(f)
            
        if isinstance(cookie_json, dict):
            # 如果是JSON对象，尝试提取cookie字段
            cookie = cookie_json.get('cookie', '')
        else:
            # 假设是直接的cookie字符串
            cookie = str(cookie_json)
            
        if cookie:
            print("✅ 从配置文件读取到cookie")
        else:
            print("⚠️ 配置文件中未找到有效的cookie")
            
        return cookie
            
    except Exception as e:
        print(f"❌ 读取cookie配置文件失败: {e}")
        return ''


def read_urls_from_config(config_file: str = 'urls_config.txt') -> List[str]:
    """从配置文件读取URL列表"""
    urls = []
    
    try:
        if not os.path.exists(config_file):
            print(f"❌ 配置文件 {config_file} 不存在")
            return urls
        
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            print(f"❌ 配置文件 {config_file} 为空")
            return urls
        
        # 支持多种分隔符
        lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):  # 跳过空行和注释行
                continue
            
            # 支持多个URL在一行（用逗号、分号、空格分隔）
            line_urls = []
            for sep in [',', ';', ' ', '\t']:
                if sep in line:
                    line_urls = [url.strip() for url in line.split(sep) if url.strip()]
                    break
            
            if not line_urls:
                line_urls = [line]
            
            for url in line_urls:
                if url and ('douyin.com' in url or 'v.douyin.com' in url):
                    urls.append(url)
                elif url:
                    print(f"⚠️ 跳过无效链接: {url}")
        
        print(f"✅ 从配置文件读取到 {len(urls)} 个有效链接")
        return urls
        
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return urls


def main():
    """主函数"""
    print("🎯 抖音用户作品URL获取工具")
    print("-" * 40)
    
    # 加载Cookie
    cookie = load_cookie_from_config()
    if not cookie:
        print("⚠️ 未找到cookie配置，可能会导致获取失败")
    
    # 读取URL配置
    urls = read_urls_from_config()
    if not urls:
        print("❌ 未找到有效的URL，程序退出")
        return
    
    # 创建视频URL获取器
    video_getter = DouyinVideoURLGetter(cookie)
    
    # 设置最大获取数量，0表示不限制
    max_videos = 0
    
    # 处理每个用户链接
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] 开始处理链接: {url}")
        print("-" * 40)
        
        # 获取视频列表
        videos = video_getter.get_videos_from_user_url(url, max_videos)
        
        if videos:
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"video_urls_{timestamp}_{i}.json"
            
            # 保存视频信息
            video_getter.save_to_file(filename)
            
            # 打印视频URL汇总
            print("\n📋 视频URL汇总:")
            for j, video in enumerate(videos, 1):
                print(f"{j}. {video['url']}")
        else:
            print("❌ 未获取到视频数据")
        
        # 添加延时，避免请求过快
        if i < len(urls):
            print("\n⏱️ 等待5秒后处理下一个链接...")
            time.sleep(5)
    
    print("\n✅ 所有链接处理完成!")


if __name__ == "__main__":
    main()
