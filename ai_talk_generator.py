#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音用户AI打招呼话术生成器
基于Coze API，读取用户信息JSON文件，生成个性化打招呼话术
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# Coze SDK导入
try:
    from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL
except ImportError:
    print("❌ 请先安装 cozepy 库: pip install cozepy")
    exit(1)


class AITalkGenerator:
    """AI打招呼话术生成器"""
    
    def __init__(self, coze_api_token: str, bot_id: str):
        # Coze API配置
        self.coze_api_token = coze_api_token
        self.bot_id = bot_id
        self.user_id = '123456789'  # 可以自定义
        
        # 初始化Coze客户端
        self.coze = Coze(
            auth=TokenAuth(token=self.coze_api_token), 
            base_url=COZE_CN_BASE_URL
        )
        
        # 目录配置
        self.input_dir = "integrated_output"
        self.output_dir = "Talk_output"
        self.log_file = "ai_talk_generator_log.txt"
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 统计信息
        self.stats = {
            "total_files": 0,
            "success_count": 0,
            "failed_count": 0,
            "start_time": None,
            "end_time": None
        }
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        # 写入日志文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def read_user_info_json(self, json_file: str) -> Optional[str]:
        """读取用户信息JSON文件内容"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_content = f.read()
            
            return json_content
        except Exception as e:
            self.log(f"读取JSON文件失败 {json_file}: {e}", "ERROR")
            return None
    
    def build_prompt(self, json_content: str) -> str:
        """构建AI提示词"""
        # 直接返回JSON内容，不添加任何其他提示词
        return json_content
    
    def generate_talk_text(self, json_content: str, nickname: str = "未知用户") -> Optional[str]:
        """使用Coze API生成打招呼话术"""
        try:
            # 构建提示词
            prompt = self.build_prompt(json_content)
            
            self.log(f"正在为用户 {nickname} 生成话术...")
            
            # 调用Coze API
            talk_content = ""
            
            for event in self.coze.chat.stream(
                bot_id=self.bot_id,
                user_id=self.user_id,
                additional_messages=[
                    Message.build_user_question_text(prompt),
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
                self.log(f"✅ 话术生成成功，长度: {len(talk_content)} 字")
                return talk_content
            else:
                self.log("❌ 生成的话术为空", "WARNING")
                return None
                
        except Exception as e:
            self.log(f"调用Coze API失败: {e}", "ERROR")
            return None
    
    def save_talk_text(self, talk_content: str, original_filename: str) -> bool:
        """保存话术到文件"""
        try:
            # 生成输出文件名（与原JSON文件名一致，但扩展名为.txt）
            base_name = os.path.splitext(original_filename)[0]
            output_filename = f"{base_name}.txt"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # 准备输出内容
            output_content = f"""# 抖音用户打招呼话术
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 原始文件: {original_filename}

{talk_content}
"""
            
            # 保存到文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            self.log(f"✅ 话术已保存: {output_filename}")
            return True
            
        except Exception as e:
            self.log(f"保存话术失败: {e}", "ERROR")
            return False
    
    def process_single_file(self, json_filename: str) -> bool:
        """处理单个JSON文件"""
        json_path = os.path.join(self.input_dir, json_filename)
        
        self.log(f"\n--- 处理文件: {json_filename} ---")
        
        # 读取JSON文件内容
        json_content = self.read_user_info_json(json_path)
        if not json_content:
            return False
        
        # 尝试解析用户昵称用于日志显示
        try:
            user_data = json.loads(json_content)
            nickname = user_data.get('user_info', {}).get('nickname', '未知用户')
        except:
            nickname = '未知用户'
        
        # 生成话术
        talk_content = self.generate_talk_text(json_content, nickname)
        if not talk_content:
            return False
        
        # 保存话术
        success = self.save_talk_text(talk_content, json_filename)
        
        # 添加延迟，避免API调用过频
        time.sleep(2)
        
        return success
    
    def get_user_json_files(self) -> List[str]:
        """获取所有用户信息JSON文件"""
        if not os.path.exists(self.input_dir):
            self.log(f"输入目录不存在: {self.input_dir}", "ERROR")
            return []
        
        json_files = []
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.json') and not filename.startswith('integrated_report_'):
                json_files.append(filename)
        
        json_files.sort()  # 按文件名排序
        return json_files
    
    def process_all_files(self) -> bool:
        """处理所有用户信息JSON文件"""
        self.log("=== 抖音用户AI打招呼话术生成器启动 ===")
        
        # 获取所有JSON文件
        json_files = self.get_user_json_files()
        
        if not json_files:
            self.log("未找到用户信息JSON文件", "ERROR")
            return False
        
        # 初始化统计
        self.stats["total_files"] = len(json_files)
        self.stats["start_time"] = datetime.now().isoformat()
        
        self.log(f"找到 {len(json_files)} 个用户信息文件")
        
        # 逐个处理文件
        for i, json_filename in enumerate(json_files, 1):
            self.log(f"\n[{i}/{len(json_files)}] 开始处理: {json_filename}")
            
            success = self.process_single_file(json_filename)
            
            if success:
                self.stats["success_count"] += 1
            else:
                self.stats["failed_count"] += 1
        
        # 完成处理
        self.stats["end_time"] = datetime.now().isoformat()
        
        # 生成统计报告
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
        
        self.log("\n" + "="*60)
        self.log("AI话术生成完成统计报告")
        self.log("="*60)
        self.log(f"总文件数: {stats['total_files']}")
        self.log(f"生成成功: {stats['success_count']} ✅")
        self.log(f"生成失败: {stats['failed_count']} ❌")
        self.log(f"总处理时长: {duration:.2f} 秒")
        
        if stats["total_files"] > 0:
            success_rate = (stats["success_count"] / stats["total_files"] * 100)
            self.log(f"成功率: {success_rate:.1f}%")
        
        self.log(f"输出目录: {self.output_dir}")
        self.log("="*60)


def create_base_talk_template():
    """创建基础话术模板文件"""
    template_content = """# 抖音打招呼话术模板

## 通用话术模板：

### 简洁型：
你好！看到你的作品很棒，想和你交流一下～

### 赞美型：
你好！你的内容很有意思，关注你很久了，能认识一下吗？

### 兴趣型：
你好！我们好像有共同的兴趣爱好，可以聊聊吗？

### 地域型：
你好！看到你也是[地区]的，老乡见老乡～

### 专业型：
你好！你在[领域]方面很专业，想请教一些问题～

## 注意事项：
1. 话术要真诚自然，避免过于商业化
2. 可以适当提及对方的特点或作品
3. 保持礼貌和尊重
4. 根据对方的内容风格调整语气
"""
    
    os.makedirs("Talk_output", exist_ok=True)
    with open("Talk_output/话术模板.txt", "w", encoding="utf-8") as f:
        f.write(template_content)


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
        print("2. 或直接修改 ai_talk_generator.py 中的token")
        return
    
    # 创建生成器实例
    generator = AITalkGenerator(coze_api_token, bot_id)
    
    try:
        # 创建基础模板文件
        create_base_talk_template()
        generator.log("✅ 话术模板文件已创建")
        
        # 处理所有文件
        success = generator.process_all_files()
        
        if success:
            print(f"\n✅ AI话术生成完成！")
            print(f"输出目录: {generator.output_dir}")
            print(f"日志文件: {generator.log_file}")
        else:
            print(f"\n❌ AI话术生成失败！")
            print("请检查:")
            print("1. Coze API token是否有效")
            print("2. Bot ID是否正确")
            print("3. 网络连接是否正常")
            print("4. integrated_output目录是否包含用户信息JSON文件")
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了处理过程")
        generator.log("用户中断了处理过程", "WARNING")
    except Exception as e:
        print(f"\n❌ 处理过程中发生错误: {e}")
        generator.log(f"处理过程中发生错误: {e}", "ERROR")


if __name__ == "__main__":
    main()
