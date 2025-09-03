# -*- encoding: utf-8 -*-
"""
抖音用户信息获取工具
功能：输入抖音主页链接，获取头像、IP地区、个性签名
使用方法：python douyin_get_user_info.py
"""

import os
import re
import sys
import json
from urllib.parse import urlparse, unquote

# 导入本地模块
import douyin_request as request
import douyin_cookies as cookies  
import douyin_util as util

Request = request.Request
get_cookie_dict = cookies.get_cookie_dict
str_to_path = util.str_to_path
url_redirect = util.url_redirect


class DouyinUserInfo:
    def __init__(self, cookie=''):
        """初始化用户信息获取器"""
        self.request = Request(cookie)
        self.user_info = {}
        
    def extract_user_id_from_url(self, url):
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
    
    def get_user_profile(self, sec_user_id):
        """获取用户详细信息"""
        try:
            # 方法1: 使用官方API
            params = {
                "publish_video_strategy_type": 2,
                "sec_user_id": sec_user_id, 
                "personal_center_strategy": 1
            }
            resp = self.request.getJSON('/aweme/v1/web/user/profile/other/', params)
            
            if resp and 'user' in resp:
                user_data = resp['user']
                return self._extract_user_info(user_data)
            
            # 方法2: 备用API
            print("🔄 尝试备用API...")
            params2 = {"sec_uid": sec_user_id}
            resp2 = self.request.getJSON('/web/api/v2/user/info/', params2)
            
            if resp2 and 'user_info' in resp2:
                user_data = resp2['user_info']
                return self._extract_user_info(user_data)
                
            print("❌ 无法获取用户信息，可能是cookie无效或用户不存在")
            return None
            
        except Exception as e:
            print(f"❌ 获取用户信息失败: {e}")
            return None
    
    def _extract_user_info(self, user_data):
        """提取关键用户信息"""
        try:
            # 基本信息
            info = {
                'nickname': user_data.get('nickname', ''),
                'signature': user_data.get('signature', ''),
                'sec_user_id': user_data.get('sec_user_id', ''),
                'uid': user_data.get('uid', ''),
                'unique_id': user_data.get('unique_id', ''),
            }
            
            # 头像信息
            avatar_thumb = user_data.get('avatar_thumb', {})
            if avatar_thumb and 'url_list' in avatar_thumb:
                info['avatar'] = avatar_thumb['url_list'][-1]  # 获取最高清的头像
            elif 'avatar_larger' in user_data:
                avatar_larger = user_data.get('avatar_larger', {})
                if 'url_list' in avatar_larger:
                    info['avatar'] = avatar_larger['url_list'][-1]
            else:
                info['avatar'] = ''
            
            # IP地区信息（尝试多个可能的字段）
            location_fields = ['ip_location', 'city', 'province', 'region', 'location', 'region_name']
            info['ip_location'] = ''
            
            for field in location_fields:
                if field in user_data and user_data[field]:
                    info['ip_location'] = user_data[field]
                    break
            
            # 如果没有直接的地区字段，尝试从其他信息推断
            if not info['ip_location']:
                # 检查是否有地区相关的认证信息
                enterprise_verify_reason = user_data.get('enterprise_verify_reason', '')
                if enterprise_verify_reason and ('·' in enterprise_verify_reason or '地区' in enterprise_verify_reason):
                    info['ip_location'] = enterprise_verify_reason.split('·')[-1] if '·' in enterprise_verify_reason else enterprise_verify_reason
            
            # 其他有用信息
            info['follower_count'] = user_data.get('follower_count', 0)  # 粉丝数
            info['following_count'] = user_data.get('following_count', 0)  # 关注数
            info['aweme_count'] = user_data.get('aweme_count', 0)  # 作品数
            info['total_favorited'] = user_data.get('total_favorited', 0)  # 获赞数
            
            return info
            
        except Exception as e:
            print(f"❌ 信息提取失败: {e}")
            return None
    
    def get_user_info_from_url(self, douyin_url):
        """从抖音主页链接获取用户信息"""
        print(f"🔍 开始解析链接: {douyin_url}")
        
        # 提取用户ID
        sec_user_id = self.extract_user_id_from_url(douyin_url)
        if not sec_user_id:
            return None
        
        print(f"✅ 用户ID: {sec_user_id}")
        
        # 获取用户信息
        user_info = self.get_user_profile(sec_user_id)
        if user_info:
            self.user_info = user_info
            return user_info
        
        return None
    
    def print_user_info(self):
        """格式化打印用户信息"""
        if not self.user_info:
            print("❌ 没有用户信息可显示")
            return
        
        print("\n" + "="*50)
        print("📱 抖音用户信息")
        print("="*50)
        print(f"👤 昵称: {self.user_info.get('nickname', '未知')}")
        print(f"📝 个性签名: {self.user_info.get('signature', '无')}")
        print(f"🌍 IP地区: {self.user_info.get('ip_location', '未知')}")
        print(f"🖼️ 头像链接: {self.user_info.get('avatar', '无')}")
        print(f"👥 粉丝数: {self.user_info.get('follower_count', 0)}")
        print(f"🤝 关注数: {self.user_info.get('following_count', 0)}")
        print(f"🎬 作品数: {self.user_info.get('aweme_count', 0)}")
        print(f"❤️ 获赞数: {self.user_info.get('total_favorited', 0)}")
        print("="*50)
    
    def save_to_file(self, filename='user_info.json'):
        """保存用户信息到文件"""
        if not self.user_info:
            print("❌ 没有用户信息可保存")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.user_info, f, ensure_ascii=False, indent=2)
            print(f"✅ 用户信息已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")


def main():
    """主函数"""
    print("🎯 抖音用户信息获取工具")
    print("-" * 30)
    
    # 获取cookie
    cookie = ''
    cookie_config_file = 'config/cookie_config.txt'
    
    # 优先从新的配置文件读取
    if os.path.exists(cookie_config_file):
        print("✅ 发现Cookie配置文件")
        try:
            with open(cookie_config_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if line.startswith('cookie='):
                    cookie = line[7:].strip()
                    if cookie:
                        print("✅ 从配置文件读取到cookie")
                        break
                elif line.startswith('browser='):
                    browser = line[8:].strip()
                    if browser in ['chrome', 'edge']:
                        cookie = browser
                        print(f"✅ 将使用{browser}浏览器自动获取cookie")
                        break
        except Exception as e:
            print(f"❌ 读取Cookie配置文件失败: {e}")
    
    # 兼容旧版本：如果没有新配置文件，尝试读取旧的cookie.txt
    if not cookie and os.path.exists('config/cookie.txt'):
        print("✅ 发现旧版cookie文件")
        with open('config/cookie.txt', 'r', encoding='utf-8') as f:
            cookie = f.read().strip()
    
    # 如果仍然没有cookie，提示用户输入
    if not cookie:
        print("⚠️ 未发现有效的Cookie配置")
        print("提示：您可以使用 'python cookie管理器.py' 来配置Cookie")
        choice = input("是否使用浏览器自动获取cookie？(chrome/edge/manual): ").lower()
        if choice in ['chrome', 'edge']:
            cookie = choice
        elif choice == 'manual':
            cookie = input("请输入cookie: ").strip()
    
    # 创建用户信息获取器
    user_info_getter = DouyinUserInfo(cookie)
    
    # 获取用户输入的链接
    while True:
        douyin_url = input("\n请输入抖音主页链接 (输入 'q' 退出): ").strip()
        
        if douyin_url.lower() == 'q':
            print("👋 再见！")
            break
        
        if not douyin_url:
            print("❌ 请输入有效的链接")
            continue
        
        # 获取用户信息
        user_info = user_info_getter.get_user_info_from_url(douyin_url)
        
        if user_info:
            # 显示信息
            user_info_getter.print_user_info()
            
            # 询问是否保存
            save_choice = input("\n是否保存到文件？(y/n): ").lower()
            if save_choice == 'y':
                filename = input("请输入文件名 (默认: user_info.json): ").strip()
                if not filename:
                    filename = 'user_info.json'
                user_info_getter.save_to_file(filename)
        else:
            print("❌ 获取用户信息失败，请检查链接或cookie是否有效")


if __name__ == "__main__":
    main()
