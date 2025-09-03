# 抖音终极爬虫 - 快速使用指南

## 🎯 一键运行完整流程
**URL链接 → Cookie配置 → 用户信息抓取 → AI话术生成**

---

## 📋 系统要求

### Python版本
- **Python 3.12** （推荐）
- 最低支持：Python 3.8+

### 操作系统
- Windows 10/11 （主要支持）
- macOS / Linux （基础支持）

---

## 🔧 前置条件

### 1. 浏览器要求
- **Chrome** 或 **Edge** 浏览器
- **必须在浏览器中登录抖音账号**: https://www.douyin.com/
- 确保能看到个人头像和推荐视频

### 2. Coze AI账号
- 注册Coze账号: https://www.coze.cn/
- 创建Bot并获取API Token
- 创建个人访问令牌

---

## 📦 依赖安装

```bash
# 一键安装所有依赖（推荐）
pip install -r requirements.txt

# 或手动安装
pip install rookiepy>=0.4.0
pip install cozepy>=0.1.0
pip install requests>=2.25.0
pip install ujson>=4.0.0
pip install loguru>=0.5.0
pip install PyExecJS>=1.5.1
```

---

## ⚙️ 初始配置

### 1. 创建URLs配置文件
创建 `urls_config.txt` 文件：
```
# 抖音用户链接配置文件
# 每行一个链接，支持短链接和完整链接

https://v.douyin.com/iSNbMea7/
https://www.douyin.com/user/MS4wLjABAAAAk9ajo7ujVMAdMy8gTPNpFtxemAX9XiTFs_oVIzosg8PuREt0dm3gATQ17yhEP48C
https://v.douyin.com/iJsAmXXr/

# 注释行会被忽略
# 支持逗号分隔多个链接在同一行
```

### 2. 创建Coze API配置文件
创建 `coze_config.json` 文件：
```json
{
  "coze_api_token": "你的Coze API Token",
  "bot_id": "你的Bot ID",
  "user_id": "123456789"
}
```

**获取API配置步骤：**
1. 登录 https://www.coze.cn/
2. 进入开发者设置 → 创建个人访问令牌
3. 复制Token（格式：`cztei_xxx...`）
4. 创建Bot，从URL复制Bot ID（最后一串数字）

### 3. 创建必要目录
```bash
mkdir config
mkdir integrated_output  
mkdir Talk_output
```

---

## 📁 必需文件结构

```
douyintalk/
├── ultimate_crawler.py          # 主脚本（必需）
├── batch_config_cookie.py       # Cookie管理器（必需）
├── douyin_request.py            # 抖音请求模块（自动生成）
├── douyin_cookies.py            # Cookie管理模块（自动生成）
├── douyin_util.py               # 工具函数模块（自动生成）
├── douyin_execjs_fix.py         # JS执行修复（自动生成）
├── douyin_get_user_info.py      # 用户信息获取（自动生成）
├── urls_config.txt              # 用户链接配置（必需）
├── coze_config.json             # API配置（必需）  
├── requirements.txt             # 依赖文件
├── js/                          # JS文件目录（自动生成）
│   └── douyin.js                # 签名算法JS文件
├── config/                      # 配置目录（自动创建）
├── integrated_output/           # 用户信息输出（自动创建）
└── Talk_output/                 # 话术输出（自动创建）
```

**🎉 现在所有文件都在douyintalk目录内，无需外部依赖！**

---

## 🚀 运行步骤

### 第一次运行

```bash
# 1. 确保浏览器中已登录抖音
# 打开 https://www.douyin.com/ 并登录

# 2. 检查配置文件
notepad urls_config.txt          # 添加用户链接
notepad coze_config.json         # 配置API信息

# 3. 以管理员身份运行PowerShell（Windows）
# 右键开始菜单 → Windows PowerShell (管理员)

# 4. 进入项目目录
cd E:\wude\soft\git\repo\douyinTalk\douyintalk

# 5. 执行脚本
python ultimate_crawler.py
```

### 日常使用
```bash
# 更新链接配置
notepad urls_config.txt

# 一键运行
python ultimate_crawler.py
```

---

## 📊 输出文件说明

### 用户信息文件
- 位置：`integrated_output/`
- 格式：`20240120_103001_001_用户昵称.json`
- 内容：完整的用户信息数据

### AI话术文件  
- 位置：`Talk_output/`
- 格式：`20240120_103001_001_用户昵称.txt`
- 内容：个性化打招呼话术

### 处理报告
- 位置：`integrated_output/`
- 格式：`ultimate_crawler_report_20240120_103001.json`
- 内容：完整的处理统计和结果

### 日志文件
- 位置：`ultimate_crawler_log.txt`
- 内容：详细的执行日志

---

## ✅ 成功运行标志

看到以下日志说明运行成功：
```
[2024-01-20 10:30:15] [INFO] === 抖音用户终极爬虫启动 ===
[2024-01-20 10:30:16] [INFO] [1/3] ✅ Cookie配置成功
[2024-01-20 10:30:18] [INFO] [1/3] ✅ 用户信息提取成功: 用户昵称
[2024-01-20 10:30:20] [INFO] [1/3] ✅ AI话术生成成功，长度: 67 字
[2024-01-20 10:30:20] [INFO] [1/3] ✅ 完整流程成功完成
```

最终统计报告：
```
完整流程成功: 3 ✅
处理失败: 0 ❌  
完整成功率: 100.0%
```

---

## 🚨 常见问题

### 问题1: "Cookie有效，但未登录状态"
**解决**: 在浏览器中登录抖音账号

### 问题2: "无法导入 batch_config_cookie 模块"  
**解决**: 确保 `batch_config_cookie.py` 文件存在

### 问题3: "无法导入抖音模块"
**解决**: 确保 `douyin_*.py` 模块文件存在于当前目录

### 问题4: "code: 4101, Token错误"
**解决**: 更新 `coze_config.json` 中的API Token

### 问题5: 需要管理员权限
**解决**: Windows用户需要以管理员身份运行PowerShell

---

## 🎯 快速检查清单

运行前请确认：
- [ ] Python 3.12 已安装
- [ ] 依赖库已安装（运行 `pip install -r requirements.txt`）
- [ ] 浏览器中已登录抖音
- [ ] `urls_config.txt` 包含有效链接
- [ ] `coze_config.json` 配置正确
- [ ] 所有 `douyin_*.py` 模块文件存在
- [ ] `js/douyin.js` 文件存在
- [ ] 以管理员身份运行（Windows）

全部确认后运行：`python ultimate_crawler.py` 🚀
