# SubProtoX

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

SubProtoX 是一个先进的 VPN 订阅和协议转换框架，旨在将多种代理标准（包括 VLESS、VMess、Trojan 和 Shadowsocks）统一到一个无缝的智能配置系统中。它具有智能路由、基于 Web 的管理、研究优化的规则集和精美的双语界面，使其成为高级用户和学术网络加速场景的终极工具。

[English Documentation](README.md)

## ✨ 主要特性

### 核心功能
- 🔄 **多协议支持**: VLESS、VMess、Trojan、Shadowsocks 协议，完整参数支持
- 📋 **订阅转换**: Base64 编码和明文订阅 URL 转换
- 🎯 **智能分流**: 内置规则集（均衡、科研、最小）及自定义规则支持
- 🔐 **安全认证**: 基于会话的身份验证，24小时超时保护
- 📱 **RESTful API**: 完整的 API 接口，配备详尽文档

### 高级功能
- 🛡️ **SSL/HTTPS 支持**: 可选 HTTPS 加密，支持自定义域名
- 📊 **历史管理**: 转换历史追踪和管理，支持导出
- 🔄 **订阅自动更新**: 可配置的自动更新间隔
- 📈 **流量限制**: 为订阅设置流量限制
- 🛠️ **高级配置**: 面板 URL 根路径、日志配置、数据库维护
- ⚡ **节点预览与编辑**: 生成配置前预览和编辑节点名称

## 🚀 快速开始

### 方法一：一键安装（推荐）

```bash
# 克隆项目
git clone https://github.com/maxiao0234/SubProtoX.git
cd SubProtoX

# 运行安装脚本
sudo bash install.sh
```

安装脚本将自动完成：
- 从模板创建 `config.py`
- 验证 SSL 证书（如已配置）
- 在虚拟环境中安装 Python 依赖
- 创建并启用 systemd 服务
- 自动启动服务

### 方法二：手动安装

```bash
# 1. 克隆项目
git clone https://github.com/maxiao0234/SubProtoX.git
cd SubProtoX

# 2. 创建配置文件
cp config.example.py config.py

# 3. 根据您的环境修改配置文件
nano config.py

# 4. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 运行服务
python app.py
```

## ⚙️ 配置说明

### 配置文件结构

复制 `config.example.py` 为 `config.py` 并根据您的环境修改：

```python
# 服务器配置
SERVER_CONFIG = {
    'host': '0.0.0.0',      # 监听地址
    'port': 7777,           # 监听端口
    'debug': False,         # 调试模式
    'base_path': ''         # 面板 URL 根路径（如 'panel' → '/panel/'）
}

# SSL 配置
SSL_CONFIG = {
    'enabled': True,                           # 启用 SSL
    'cert_path': '/path/to/your/cert.pem',     # SSL 证书路径
    'key_path': '/path/to/your/key.pem',       # SSL 私钥路径
    'domain': 'your-domain.com'                # 自定义域名（可选）
}

# 默认用户配置（请务必修改！）
DEFAULT_USER = {
    'username': 'admin',
    'password': 'admin'     # ⚠️ 请在部署后立即修改此密码！
}

# 订阅转换配置
CONVERTER_CONFIG = {
    'max_proxies': 1000,    # 单个配置最大代理数限制
    'timeout': 30,          # 订阅获取超时时间（秒）
    'user_agent': 'SubProtoX/1.0'
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',        # 日志级别：DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': None            # 日志文件路径，None 表示输出到控制台
}
```

### 重要配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `SERVER_CONFIG.port` | 服务端口 | 7777 |
| `SERVER_CONFIG.base_path` | 面板 URL 前缀 | '' (根路径) |
| `SSL_CONFIG.enabled` | 是否启用 HTTPS | False |
| `SSL_CONFIG.domain` | 自定义域名 | '' |
| `DEFAULT_USER.username` | 默认用户名 | admin |
| `DEFAULT_USER.password` | 默认密码 | admin |
| `CONVERTER_CONFIG.max_proxies` | 单配置最大代理数 | 1000 |
| `CONVERTER_CONFIG.timeout` | 获取超时（秒） | 30 |
| `LOG_CONFIG.level` | 日志级别 | INFO |

## 🔧 服务管理

```bash
# 启动服务
sudo systemctl start subprotox

# 停止服务
sudo systemctl stop subprotox

# 重启服务
sudo systemctl restart subprotox

# 查看状态
sudo systemctl status subprotox

# 查看日志
sudo journalctl -u subprotox -f

# 设置开机自启
sudo systemctl enable subprotox
```

## 🎯 分流规则

| 规则类型 | 名称 | 说明 | 适用场景 |
|----------|------|------|----------|
| **Default** | 默认路由 | 均衡的路由规则 | 日常使用 |
| **Research** | 学术与研究路由 | 学术资源优化 | 科研访问（GitHub、arXiv、学术API） |
| **Minimal** | 最小规则 | 基础路由，规则较少 | 追求简洁和速度 |
| **Custom** | 用户自定义 | 完全可定制 | 自定义路由需求 |

## 📂 项目结构

```
SubProtoX/
├── app.py                      # 主应用程序入口
├── config.example.py           # 配置文件模板
├── install.sh                  # 自动化安装脚本
├── uninstall.sh                # 自动化安装脚本
├── requirements.txt            # Python 依赖
├── README.md / README_zh.md    # 文档（中英文）
├── LICENSE                     # MIT 许可证
│
├── core/                       # 核心模块
│   └── converter.py            # SubConverter - 协议解析和转换
│
├── rules/                      # 路由规则系统
│   ├── rule_manager.py         # RuleManager - 规则编排
│   ├── base_rules.py           # BaseRuleSet 抽象基类
│   ├── *_rules.py              # 规则实现（默认、科研、最小）
│   └── proxy_groups.py         # ProxyGroupGenerator
│
├── web/                        # Web 界面
│   ├── blueprints/             # Flask 蓝图
│   │   ├── auth.py             # 认证路由
│   │   ├── converter.py        # 转换 API 路由
│   │   └── management.py       # 管理界面路由
│   │
│   ├── templates/              # HTML 模板（Python 模块形式）
│   │   ├── login.py            # 登录页面
│   │   └── management.py       # 主管理界面
│   │
│   └── i18n/                   # 国际化
│       └── languages.py        # 中英文翻译
│
├── utils/                      # 工具模块
│   └── github_api.py           # GitHub API 集成（可选）
│
└── static/                     # 静态文件
    ├── css/                    # Bootstrap CSS
    ├── js/                     # JavaScript 库
    └── logo/                   # Logo 图像
```

## 🤝 贡献

欢迎社区贡献！如果您想改进 SubProtoX：

1. Fork 项目
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交修改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request


## ⚠️ 免责声明

本项目专为教育目的和合规网络环境优化设计。SubProtoX 仅提供网络访问规则模板，用于在合规环境下优化学术数据同步、开源代码访问与学术资源下载（如 GitHub、arXiv、OpenAI API 等）。

**重要说明：**
- 本项目不包含任何代理服务器信息或可连接的节点配置
- 用户需自行在合法合规的网络环境中使用本软件
- 本项目仅用于学术研究加速和合法的网络优化
- 用户有责任确保遵守当地法律法规
- 使用本项目所产生的任何后果由用户自行承担
- 不得将本软件用于违反当地法律法规的任何活动

## 📞 支持

如需社区支持和项目信息：

- 🐛 [提交 Bug](https://github.com/maxiao0234/SubProtoX/issues)
- 💡 [功能建议](https://github.com/maxiao0234/SubProtoX/issues)
- 📖 [查看文档](https://github.com/maxiao0234/SubProtoX/wiki)
- 💬 [讨论区](https://github.com/maxiao0234/SubProtoX/discussions)

*请注意：支持基于社区尽力而为的原则提供。*

## 🌟 致谢

- Bootstrap 5 提供精美的 UI 框架
- Material Symbols 提供图标集
- Flask 提供轻量级 Web 框架
- 开源社区的灵感和反馈

---

**如果这个项目对您有帮助，请给个 ⭐ Star 支持一下！**
