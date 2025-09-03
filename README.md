# 抖音Cookie自动获取与配置工具

## 项目简介

这是一个基于TikTokDownloader项目实现的抖音Cookie自动获取和配置工具套件，包含六个核心脚本：

1. 
2. **`integrated_crawler.py`** - 整合抓取工具（Cookie配置+用户信息抓取）
3. **`ai_talk_generator.py`** - AI打招呼话术生成器
4. **`batch_config_cookie.py`** - 批量Cookie自动配置工具
5. **`auto_config_cookie.py`** - Cookie自动配置工具
6. **`auto_cookie_douyin.py`** - Cookie自动获取工具

## 核心功能

- ✅ 自动从浏览器获取抖音Cookie
- ✅ 验证Cookie有效性和登录状态  
- ✅ 支持多种主流浏览器
- ✅ 自动保存Cookie到本地文件
- ✅ **自动配置Cookie到指定配置文件**
- ✅ **批量处理多个用户链接**
- ✅ **整合工具：Cookie配置+用户信息抓取**
- ✅ 
- ✅ **终极爬虫：完整的一站式解决方案（最新）**
- ✅ 配置文件自动备份功能
- ✅ 详细的日志记录和处理统计
- ✅ 抖音用户链接格式验证

## 支持的浏览器

- Chrome
- Edge
- Firefox
- Opera
- Brave
- Arc
- Vivaldi
- Chromium

## 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install rookiepy cozepy
```

## 使用方法

### 🚀 方法一：终极爬虫工具（最强推荐）

`ultimate_crawler.py` - 完整的一站式解决方案，集成所有功能

#### 🌟 终极特色
- **完整流程**：URL → Cookie配置 → 用户信息抓取 
- **逐条处理**：
- **智能延迟**：自动控制处理间隔，避免被封禁
- **全程日志**：详细记录每个步骤的执行情况

#### 使用方法
```bash
# 一键完成所有功能
python ultimate_crawler.py
```

#### 核心流程
1. **读取配置**: 从 `urls_config.txt` 读取所有用户链接
2. **逐条处理**: 对每个链接依次执行：
   - 配置最新Cookie到 `config/cookie_config.txt`
   - 使用新Cookie抓取用户信息并保存JSON
  
3. **智能延迟**: 每个用户处理完成后自动等待5秒
4. **完整报告**: 生成详细的处理统计报告

#### 输出文件
- `integrated_output/` - 用户信息JSON文件
- `Talk_output/` - AI生成的打招呼话术文件
- `ultimate_crawler_report_*.json` - 完整处理报告
- `ultimate_crawler_log.txt` - 详细执行日志

### 🎯 方法二：整合抓取工具

`integrated_crawler.py` - 顺序处理：Cookie配置 + 用户信息抓取

#### 核心特点
- **一站式解决方案**：自动配置Cookie + 抓取用户信息
- **顺序处理**：确保每个链接都使用最新Cookie
- **完整流程**：提取链接 → 配置Cookie → 抓取信息 → 保存文件

#### 使用方法
```bash
# 整合抓取（推荐）
python integrated_crawler.py

# 查看帮助
python integrated_crawler.py help
```

#### 处理流程
```
[1/3] 开始处理链接: https://v.douyin.com/xxx/
[1/3] 步骤1: 配置Cookie ✅
[1/3] 步骤2: 抓取用户信息 ✅  
[1/3] 步骤3: 保存用户信息 ✅

[2/3] 开始处理链接: https://www.douyin.com/user/xxx
[2/3] 步骤1: 配置Cookie ✅
[2/3] 步骤2: 抓取用户信息 ✅
[2/3] 步骤3: 保存用户信息 ✅
...
```

#### 输出文件
- `integrated_output/` - 用户信息JSON文件
- `integrated_report_*.json` - 处理统计报告
- `integrated_crawler_log.txt` - 运行日志

### 🤖 方法三：AI话术生成工具（推荐配合使用）

`ai_talk_generator.py` - 基于Coze API，读取用户信息生成个性化打招呼话术

#### 核心特点
- **AI驱动**：使用Coze API智能生成话术
- **个性化**：基于用户昵称、签名、粉丝数等信息
- **批量处理**：自动处理所有用户信息文件
- **自然语言**：生成真诚、自然的打招呼内容

#### 使用方法
```bash
# 先运行整合抓取，获取用户信息
python integrated_crawler.py

# 再生成AI话术
python ai_talk_generator.py
```

#### 配置说明

**Coze API配置是使用AI话术生成器的前提条件！**

##### 方法1：配置文件方式（推荐）

1. **编辑配置文件**：
   ```bash
   notepad coze_config.json
   ```

2. **填入你的API信息**：
   ```json
   {
     "coze_api_token": "你的Coze API Token",
     "bot_id": "你的Bot ID",
     "user_id": "123456789"
   }
   ```

##### 方法2：直接修改代码
在 `ai_talk_generator.py` 中配置：
```python
coze_api_token = 'your_coze_api_token'  # 你的Coze API Token
bot_id = 'your_bot_id'                  # 你的Bot ID
```

##### 🔑 获取Coze API配置步骤

1. **访问Coze平台**: https://www.coze.cn/
2. **登录账号**: 使用你的账号登录
3. **进入开发者设置**: 点击头像 → 开发者设置
4. **创建API密钥**: 点击"创建新密钥"，复制生成的token
5. **获取Bot ID**: 从Bot管理页面URL复制最后的数字ID

**示例**：
- Token格式：`cztei_abcdefg123456...` 
- Bot ID格式：`7544946933597732864`

##### ⚠️ 常见问题解决

**问题1**: `code: 4101, msg: The token you entered is incorrect`
- **原因**: API Token无效或过期
- **解决**: 重新获取新的token并更新配置

**问题2**: 找不到Bot ID  
- **解决**: Bot管理页面URL最后一串数字就是Bot ID

**问题3**: 配置后仍然失败
- **检查**: token格式是否完整，没有多余空格或换行

#### 输出文件
- `Talk_output/` - AI生成的打招呼话术文件
- `Talk_output/话术模板.txt` - 通用话术模板
- `ai_talk_generator_log.txt` - 生成日志
- `coze_config.json` - API配置文件

#### 🎨 AI话术生成特色

##### 智能个性化生成
- **基于用户特征**: 根据昵称、签名、粉丝数、地区等信息定制话术
- **内容类型识别**: 自动识别电影、美食、脱口秀等内容方向
- **数字智能格式化**: 大数字自动转换为"万"单位显示
- **地域亲近感**: 基于IP属地生成亲切的问候

##### 自然语言优化
- **真诚友好**: AI生成自然、真诚的打招呼内容
- **长度控制**: 每个话术控制在50-100字的合适范围
- **避免商业化**: 拒绝生硬的商业推广语言
- **个性化程度高**: 每个用户都有独特的专属话术

##### 批量高效处理
- **自动识别文件**: 自动处理所有用户信息JSON文件
- **智能延迟**: 自动控制API调用频率，避免限流
- **错误容错**: 单个失败不影响其他用户处理
- **详细统计**: 完整的成功率和处理时长报告

#### 🔍 AI话术生成示例

基于真实用户数据，AI会生成个性化话术：

**示例1 - 电影博主**：
```
输入用户: 秋琳说电影 (签名: 招高水平代剪文案, 粉丝: 31万)
生成话术: 你好！看到你是专业做电影解说的，作品质量很高呢！我也很喜欢看电影，特别是战争题材的，你的解说很有深度，想和你交流一下电影心得～
```

**示例2 - 脱口秀博主**：
```
输入用户: 一支麦二狗脱口秀 (地区: 广东, 粉丝: 34.9万)
生成话术: 你好！看到你是做脱口秀的，很有趣呢！34万粉丝的账号已经很厉害了，作为广东老乡想和你交流一下，你的脱口秀内容很有意思～
```

**示例3 - 美食博主**：
```
输入用户: 美食小当家 (签名: 分享家常菜做法, 地区: 四川)
生成话术: 你好！看到你经常分享家常菜做法，作为四川老乡很有共鸣！你的菜品看起来都很香，想请教几个川菜的小窍门～
```

### 🚀 方法四：批量Cookie自动配置工具

`batch_config_cookie.py` - 从 `urls_config.txt` 批量读取链接并自动配置Cookie

#### 使用步骤
1. **编辑URLs配置文件**
   ```bash
   # 编辑 urls_config.txt 文件，添加抖音用户链接
   notepad urls_config.txt
   ```

2. **运行批量配置**
   ```bash
   # 批量自动配置所有链接
   python batch_config_cookie.py
   
   # 查看URLs配置状态
   python batch_config_cookie.py status
   
   # 查看帮助信息
   python batch_config_cookie.py help
   ```

#### URLs配置文件格式
```
# 抖音用户链接配置文件
# 每行一个链接，或用逗号分隔多个链接
# 以 # 开头的行为注释

https://v.douyin.com/iSNbMea7/
https://www.douyin.com/user/MS4wLjABAAAAk9ajo7ujVMAdMy8gTPNpFtxemAX9XiTFs_oVIzosg8PuREt0dm3gATQ17yhEP48C

# 一行多个链接（逗号分隔）
# https://v.douyin.com/link1/, https://v.douyin.com/link2/
```

#### 输出文件
- `config/cookie_config.txt` - 主配置文件（新配置覆盖原配置）
- `config/batch_results.json` - 批量处理结果统计
- `batch_cookie_config_log.txt` - 批量处理日志

### 🔧 方法五：Cookie自动配置工具

`auto_config_cookie.py` - 单个链接直接配置到 `config/cookie_config.txt` 文件中

#### 命令行方式
```bash
# 直接配置Cookie到配置文件
python auto_config_cookie.py "https://www.douyin.com/user/MS4wLjABAAAA..."

# 查看配置状态
python auto_config_cookie.py status

# 查看帮助信息
python auto_config_cookie.py help
```

#### 交互式方式
```bash
python auto_config_cookie.py
```
然后按提示输入抖音用户主页链接。

#### 输出文件
- `config/cookie_config.txt` - 主配置文件
- `config/cookie_backup.json` - 配置备份文件  
- `config/cookie_info.json` - Cookie详细信息
- `cookie_config_log.txt` - 运行日志

### 📁 方法六：Cookie获取工具

`auto_cookie_douyin.py` - 获取Cookie并保存到独立JSON文件

#### 命令行方式
```bash
python auto_cookie_douyin.py "https://www.douyin.com/user/MS4wLjABAAAA..."
```

#### 交互式方式
```bash
python auto_cookie_douyin.py
```

#### 查看帮助
```bash
python auto_cookie_douyin.py help
```

#### 输出文件
- `douyin_cookies.json` - Cookie数据文件
- `cookie_log.txt` - 运行日志

## 支持的链接格式

- `https://www.douyin.com/user/MS4wLjABAAAA...`
- `https://v.douyin.com/iJsAmXXr/`
- `https://www.iesdouyin.com/share/user/123456789`

## 文件结构

```
douyintalk/
├── integrated_crawler.py         # 整合抓取工具（最强推荐）
├── ai_talk_generator.py          # AI话术生成器（推荐配合使用）
├── batch_config_cookie.py        # 批量Cookie配置工具
├── auto_config_cookie.py         # 单个Cookie配置工具
├── auto_cookie_douyin.py         # Cookie获取工具
├── coze_config.json              # Coze API配置文件
├── talkBase.txt                  # 话术基础模板
├── urls_config.txt               # URLs配置文件
├── requirements.txt              # 依赖文件
├── README.md                    # 说明文档
├── config/                      # 配置目录
│   ├── cookie_config.txt        # Cookie配置文件
│   ├── cookie_backup.json       # 配置备份
│   ├── cookie_info.json         # Cookie详细信息
│   └── batch_results.json       # 批量处理结果
├── integrated_output/           # 整合抓取输出目录
│   ├── 20240120_103001_001_用户1.json  # 用户信息文件
│   └── integrated_report_*.json       # 处理报告
├── Talk_output/                 # AI话术输出目录
│   ├── 20240120_103001_001_用户1.txt   # 生成的话术文件
│   └── 话术模板.txt                    # 通用话术模板
├── douyin_cookies.json          # Cookie数据文件
├── integrated_crawler_log.txt   # 整合抓取日志
├── ai_talk_generator_log.txt    # AI话术生成日志
├── batch_cookie_config_log.txt  # 批量配置日志
├── cookie_config_log.txt        # 单个配置日志
└── cookie_log.txt               # 获取工具日志
```

## 注意事项

### Windows用户

- **必须以管理员身份运行**：Windows系统需要管理员权限才能读取Chrome、Edge等浏览器的Cookie
- 右键点击命令提示符/PowerShell，选择"以管理员身份运行"

### 使用前准备

1. 在浏览器中登录抖音账号
2. 确保已安装 `rookiepy` 库
3. Windows系统以管理员权限运行

### Cookie有效性

程序会自动验证Cookie是否包含必需的字段：
- `odin_tt`: 抖音基础验证字段
- `passport_csrf_token`: CSRF保护字段
- `sessionid_ss`: 登录状态字段（可选）

## 使用示例

### 🎯 整合抓取工具示例（最强推荐）

```bash
# 一键完成：Cookie配置 + 用户信息抓取
python integrated_crawler.py

# 查看帮助
python integrated_crawler.py help
```

**先编辑 urls_config.txt 文件：**
```
# 抖音用户链接配置文件
https://www.douyin.com/user/MS4wLjABAAAAk9ajo7ujVMAdMy8gTPNpFtxemAX9XiTFs_oVIzosg8PuREt0dm3gATQ17yhEP48C?from_tab_name=main
https://www.douyin.com/user/MS4wLjABAAAAqvvLjQbwVfb8E8kgNyrAHRJgX6lFwMTzg2-7Bk2PjlHtknUYbkVig-LR-e1UMMO7?from_tab_name=main&vid=7531693148620328244
https://v.douyin.com/iSNbMea7/
```

**运行整合抓取后会看到类似输出：**

```
=== 抖音用户信息整合抓取工具启动 ===
[2024-01-20 10:30:15] [INFO] [INTEGRATED] 从配置文件读取到 3 个有效链接
[2024-01-20 10:30:15] [INFO] [INTEGRATED] 准备按顺序处理 3 个链接

============================================================
[2024-01-20 10:30:16] [INFO] [INTEGRATED] [1/3] 开始处理链接: https://www.douyin.com/user/MS4wLjABAAAAk9ajo7ujVMAdMy8gTPNpFtxemAX9XiTFs_oVIzosg8PuREt0dm3gATQ17yhEP48C
============================================================
[2024-01-20 10:30:16] [INFO] [INTEGRATED] [1/3] 步骤1: 配置Cookie
[2024-01-20 10:30:17] [INFO] [INTEGRATED] [1/3] ✅ Cookie配置成功
[2024-01-20 10:30:19] [INFO] [INTEGRATED] [1/3] 步骤2: 抓取用户信息
[2024-01-20 10:30:20] [INFO] [INTEGRATED] [1/3] ✅ 用户信息获取成功
[2024-01-20 10:30:20] [INFO] [INTEGRATED] [1/3]    👤 昵称: 测试用户1
[2024-01-20 10:30:20] [INFO] [INTEGRATED] [1/3]    📝 签名: 这是个性签名
[2024-01-20 10:30:20] [INFO] [INTEGRATED] [1/3]    🌍 地区: 北京
[2024-01-20 10:30:20] [INFO] [INTEGRATED] [1/3]    👥 粉丝: 12345
[2024-01-20 10:30:20] [INFO] [INTEGRATED] [1/3] 步骤3: 保存用户信息
[2024-01-20 10:30:20] [INFO] [INTEGRATED] ✅ 用户信息已保存: 20240120_103020_001_测试用户1.json
[2024-01-20 10:30:20] [INFO] [INTEGRATED] [1/3] ✅ 链接处理完成

======================================================================
整合抓取完成统计报告
======================================================================
总链接数: 3
Cookie配置成功: 2 ✅
用户信息抓取成功: 2 ✅
总处理时长: 45.30 秒
信息抓取成功率: 66.7%

成功抓取的用户:
  - 测试用户1 (粉丝: 12345, 文件: 20240120_103020_001_测试用户1.json)
  - 测试用户2 (粉丝: 5678, 文件: 20240120_103025_002_测试用户2.json)

✅ 整合抓取完成！
```

### 🤖 AI话术生成工具示例

```bash
# 先运行整合抓取获取用户信息
python integrated_crawler.py

# 再生成个性化话术
python ai_talk_generator.py
```

**AI话术生成输出示例：**

```
=== 抖音用户AI打招呼话术生成器启动 ===
[2024-01-20 14:30:15] [INFO] 找到 3 个用户信息文件

[2024-01-20 14:30:16] [INFO] [1/3] 开始处理: 20250901_133818_002_秋琳说电影.json
[2024-01-20 14:30:16] [INFO] 正在为用户 秋琳说电影 生成话术...
[2024-01-20 14:30:18] [INFO] API调用完成，token使用量: 245
[2024-01-20 14:30:18] [INFO] ✅ 话术生成成功，长度: 87 字
[2024-01-20 14:30:18] [INFO] ✅ 话术已保存: 20250901_133818_002_秋琳说电影.txt

============================================================
AI话术生成完成统计报告
============================================================
总文件数: 3
生成成功: 3 ✅
生成失败: 0 ❌
成功率: 100.0%
输出目录: Talk_output
```

**生成的话术文件内容示例：**

```
# 抖音用户打招呼话术
# 生成时间: 2024-01-20 14:30:18
# 原始文件: 20250901_133818_002_秋琳说电影.json

你好！看到你是专业做电影解说的，作品质量很高呢！我也很喜欢看电影，特别是战争题材的，你的解说很有深度，想和你交流一下电影心得～
```

### 🚀 批量Cookie配置工具示例

```bash
# 方式1：批量配置所有链接
python batch_config_cookie.py

# 方式2：查看URLs配置状态
python batch_config_cookie.py status

# 方式3：查看帮助
python batch_config_cookie.py help
```

### 📋 单个Cookie自动配置工具示例

```bash
# 方式1：命令行直接配置
python auto_config_cookie.py "https://www.douyin.com/user/MS4wLjABAAAAk9ajo7ujVMAdMy8gTPNpFtxemAX9XiTFs_oVIzosg8PuREt0dm3gATQ17yhEP48C?from_tab_name=main"

# 方式2：查看当前配置状态
python auto_config_cookie.py status

# 方式3：交互式配置
python auto_config_cookie.py
```

**运行成功后会看到类似输出：**

```
=== 抖音Cookie自动配置工具 ===
[2024-01-20 10:30:15] [INFO] 检测到用户ID: MS4wLjABAAAATuSDlIwCjhVR-DDFl6s1hZrWxTb-x1BNO_2jPBJgXvs
[2024-01-20 10:30:15] [INFO] 正在检查可用的浏览器...
[2024-01-20 10:30:16] [INFO] 找到可用浏览器: Chrome, Edge
[2024-01-20 10:30:16] [INFO] 正在从 Chrome 浏览器获取Cookie...
[2024-01-20 10:30:17] [INFO] 成功从 Chrome 获取到 25 个Cookie字段
[2024-01-20 10:30:17] [INFO] ✅ Cookie验证成功: Cookie有效，已登录状态
[2024-01-20 10:30:17] [INFO] 配置文件已备份到: config\cookie_backup.json
[2024-01-20 10:30:17] [INFO] ✅ Cookie已更新到配置文件: config\cookie_config.txt

✅ Cookie配置成功！
配置文件: config\cookie_config.txt
现在可以使用配置文件中的Cookie进行抖音数据获取了！
```

**查看配置状态示例：**

```bash
python auto_config_cookie.py status
```

输出：
```
=== 当前配置状态 ===
[2024-01-20 10:35:20] [INFO] ✅ 配置文件存在: config\cookie_config.txt
[2024-01-20 10:35:20] [INFO] ✅ 发现Cookie配置（长度: 2048）
[2024-01-20 10:35:20] [INFO] 浏览器设置: chrome
[2024-01-20 10:35:20] [INFO] ✅ 备份文件存在: config\cookie_backup.json
```

### 📄 Cookie获取工具示例

```bash
# 直接指定链接
python auto_cookie_douyin.py "https://www.douyin.com/user/MS4wLjABAAAATuSDlIwCjhVR-DDFl6s1hZrWxTb-x1BNO_2jPBJgXvs"

# 交互式输入
python auto_cookie_douyin.py
```

运行成功后会看到类似输出：

```
=== 抖音Cookie自动获取工具 ===
[2024-01-20 10:30:15] [INFO] 检测到用户ID: MS4wLjABAAAATuSDlIwCjhVR-DDFl6s1hZrWxTb-x1BNO_2jPBJgXvs
[2024-01-20 10:30:15] [INFO] 正在检查可用的浏览器...
[2024-01-20 10:30:16] [INFO] 找到可用浏览器: Chrome, Edge
[2024-01-20 10:30:16] [INFO] 正在从 Chrome 浏览器获取Cookie...
[2024-01-20 10:30:17] [INFO] 成功从 Chrome 获取到 25 个Cookie字段
[2024-01-20 10:30:17] [INFO] ✅ Cookie验证成功: Cookie有效，已登录状态
[2024-01-20 10:30:17] [INFO] Cookie已保存到文件: douyin_cookies.json

✅ Cookie获取成功！
```

## 故障排除

### 常见问题

1. **权限错误**
   - Windows用户确保以管理员身份运行
   - macOS用户可能需要授权访问浏览器数据

2. **未找到Cookie**
   - 确保在浏览器中已登录抖音账号
   - 尝试访问一次抖音网站后再运行脚本

3. **导入错误**
   - 确保已安装 `rookiepy` 库：`pip install rookiepy`

4. **Cookie验证失败**
   - Cookie可能已过期，重新登录抖音账号
   - 尝试清除浏览器缓存后重新登录

5. **配置文件问题**
   - 如果配置文件损坏，程序会自动创建默认配置
   - 可以从 `config/cookie_backup.json` 恢复配置
   - 使用 `python auto_config_cookie.py status` 检查配置状态

6. **文件权限问题**
   - 确保程序对 `config` 目录有写入权限
   - Windows用户可能需要以管理员身份运行

### 快速诊断

```bash
# 检查配置状态
python auto_config_cookie.py status

# 查看日志文件
type cookie_config_log.txt

# 重新配置（会自动备份原配置）
python auto_config_cookie.py "你的抖音链接"
```

### 配置文件说明

`config/cookie_config.txt` 文件格式：
```
# 抖音Cookie配置文件
cookie=你的完整cookie字符串
browser=chrome
# 最后更新时间：2024-01-20 10:30:17
```

## 工具对比

| 特性 | integrated_crawler.py | ai_talk_generator.py | batch_config_cookie.py | auto_config_cookie.py | auto_cookie_douyin.py |
|------|----------------------|---------------------|------------------------|----------------------|----------------------|
| **推荐度** | ⭐⭐⭐⭐⭐ 终极推荐 | ⭐⭐⭐⭐⭐ 强烈推荐 | ⭐⭐⭐⭐ 推荐 | ⭐⭐⭐ 推荐 | ⭐⭐ 基础工具 |
| **主要用途** | Cookie配置+用户信息抓取 | AI生成个性化话术 | 批量配置多个用户链接 | 单个链接直接配置 | 获取Cookie到独立文件 |
| **完整流程** | ✅ 信息抓取解决方案 | ✅ 话术生成解决方案 | ❌ 仅Cookie配置 | ❌ 仅Cookie配置 | ❌ 仅获取Cookie |
| **AI功能** | ❌ 不支持 | ✅ 基于Coze API | ❌ 不支持 | ❌ 不支持 | ❌ 不支持 |
| **输入方式** | urls_config.txt文件 | integrated_output目录 | urls_config.txt文件 | 命令行/交互式 | 命令行/交互式 |
| **输出格式** | 用户信息JSON文件 | 话术文本文件 | config/cookie_config.txt | config/cookie_config.txt | douyin_cookies.json |
| **批量处理** | ✅ 支持多链接 | ✅ 支持多用户 | ✅ 支持多链接 | ❌ 单链接 | ❌ 单链接 |
| **个性化** | ❌ 标准化抓取 | ✅ 基于用户信息定制 | ❌ 标准化配置 | ❌ 标准化配置 | ❌ 标准化获取 |
| **API依赖** | ❌ 仅浏览器Cookie | ✅ 需要Coze API | ❌ 仅浏览器Cookie | ❌ 仅浏览器Cookie | ❌ 仅浏览器Cookie |
| **处理统计** | ✅ 详细统计报告 | ✅ 详细统计报告 | ✅ 详细统计报告 | ❌ 无统计 | ❌ 无统计 |
| **使用场景** | 用户信息收集 | 社交话术生成 | Cookie批量配置 | 单个配置，测试使用 | Cookie分析，调试使用 |

### 使用建议

#### 🏆 完整业务流程推荐

**最佳组合：`integrated_crawler.py` + `ai_talk_generator.py`**

```bash
# 步骤1：批量抓取用户信息
python integrated_crawler.py

# 步骤2：生成个性化话术
python ai_talk_generator.py
```

这个组合提供了完整的解决方案：**用户信息收集 → AI话术生成**

#### 🎯 各工具的最佳使用场景

1. **🎯 `integrated_crawler.py`** - 用户信息收集：
   - 一站式完整的用户信息抓取方案
   - 自动配置Cookie + 抓取用户信息
   - 顺序处理，确保每个链接都使用最新Cookie
   - **最适合批量收集用户数据**

2. **🤖 `ai_talk_generator.py`** - AI话术生成：
   - 基于真实用户信息生成个性化话术
   - 使用Coze API，自然语言处理
   - 批量处理，高效生成
   - **最适合社交营销和用户沟通**

3. **🚀 `batch_config_cookie.py`** - Cookie批量配置：
   - 只需要批量配置Cookie，不需要抓取信息
   - 为其他工具准备Cookie配置
   - Cookie批量更新维护

4. **🔧 `auto_config_cookie.py`** - 单个Cookie配置：
   - 单个用户快速配置
   - 临时测试单个链接
   - 不需要批量处理的场景

5. **📁 `auto_cookie_douyin.py`** - Cookie获取分析：
   - 需要分析Cookie内容
   - 临时获取Cookie到JSON文件
   - 开发调试阶段

## 快速开始

### 第一次使用

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 在浏览器中登录抖音账号

# 3. 编辑URLs配置文件
notepad urls_config.txt
# 添加你的抖音用户链接，每行一个

# 4. 配置Coze API（可选，用于AI话术生成）
# 编辑 ai_talk_generator.py 中的API配置

# 5. 以管理员身份运行PowerShell（Windows）

# 6. 批量抓取用户信息
python integrated_crawler.py

# 7. 生成AI话术（可选）
python ai_talk_generator.py

# 8. 查看结果文件
dir integrated_output\
dir Talk_output\
```

### 日常使用

```bash
# 完整业务流程（最推荐）
python integrated_crawler.py    # 抓取用户信息
python ai_talk_generator.py     # 生成AI话术

# 仅批量更新Cookie
python batch_config_cookie.py

# 检查批量配置状态
python batch_config_cookie.py status

# 单个链接更新Cookie
python auto_config_cookie.py "抖音用户链接"

# 查看配置文件
type config\cookie_config.txt

# 查看用户信息文件
dir integrated_output\

# 查看AI生成的话术
dir Talk_output\

# 查看处理结果报告
type integrated_output\integrated_report_*.json
```

## 🤖 AI话术生成器详细说明

### 核心功能
`ai_talk_generator.py` 是一个基于Coze API的智能话术生成工具，能够：

1. **自动读取用户信息**: 从 `integrated_output/` 目录读取所有用户JSON文件
2. **智能分析用户特征**: 提取昵称、签名、粉丝数、地区等关键信息
3. **AI个性化生成**: 使用Coze API生成针对性的打招呼话术
4. **批量高效处理**: 支持同时处理多个用户，自动控制API调用频率
5. **完整日志记录**: 详细记录每个用户的处理过程和结果

### 工作流程
```
JSON用户信息 → Coze API → 个性化话术 → 保存到文件
```

### 输入格式
直接读取 `integrated_crawler.py` 生成的用户信息JSON文件，无需额外处理。

### 输出特点
- **文件一一对应**: 每个用户信息JSON文件对应一个话术文件
- **命名保持一致**: 输出文件名与输入文件名匹配，仅扩展名不同
- **内容结构化**: 包含生成时间、原始文件信息和话术内容

### API配置灵活性
- **配置文件方式**: 通过 `coze_config.json` 配置（推荐）
- **代码配置方式**: 直接在源码中配置
- **自动验证**: 启动前自动验证API配置有效性

### 错误处理机制
- **单个失败隔离**: 某个用户处理失败不影响其他用户
- **详细错误日志**: 记录具体的失败原因和API错误码
- **重试机制**: 对临时性错误提供友好的提示

### 性能优化
- **智能延迟**: 每次API调用间隔2秒，避免频率限制
- **内存高效**: 流式处理文件，不占用过多内存
- **进度可视**: 实时显示处理进度和统计信息

## 🔄 完整业务流程示例

### 端到端使用场景

```bash
# 步骤1: 准备用户链接
echo "https://v.douyin.com/iSNbMea7/" >> urls_config.txt
echo "https://www.douyin.com/user/MS4wLjABAAAAk9ajo..." >> urls_config.txt

# 步骤2: 配置API
notepad coze_config.json

# 步骤3: 批量抓取用户信息
python integrated_crawler.py

# 步骤4: 生成AI话术
python ai_talk_generator.py

# 步骤5: 查看结果
dir integrated_output\  # 用户信息
dir Talk_output\        # AI话术
```

### 实际输出效果
执行完成后，你将得到：
- **用户信息文件**: `integrated_output/20240120_103001_001_用户名.json`
- **AI话术文件**: `Talk_output/20240120_103001_001_用户名.txt`
- **处理报告**: 包含成功率、处理时长等统计信息

## 🎯 最佳实践建议

### 1. 配置优化
- **使用配置文件**: 避免在代码中硬编码API密钥
- **定期更新Token**: Coze API Token有有效期，建议定期更换
- **备份配置**: 保存好你的Bot ID和配置信息

### 2. 使用技巧
- **小批量测试**: 首次使用建议先测试少量用户
- **错误监控**: 关注日志中的错误信息，及时调整
- **频率控制**: 避免短时间内大量调用API

### 3. 内容质量
- **验证话术**: 生成后检查话术的质量和适用性
- **个性化调整**: 根据需要微调话术风格和长度
- **A/B测试**: 对比不同话术的实际效果

### 4. 数据管理
- **定期清理**: 清理过期的用户信息和话术文件
- **分类管理**: 按日期或用户类型组织文件
- **备份重要数据**: 定期备份成功的话术和配置

## 参考项目

本工具基于以下开源项目实现：
- Cookie获取实现：[TikTokDownloader](https://github.com/JoeanAmier/TikTokDownloader)
- 抖音信息获取实现：[douyin](https://github.com/erma0/douyin)
- AI话术生成：[Coze API](https://www.coze.cn/)

