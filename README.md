# SubProtoX

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

SubProtoX is an advanced VPN subscription and protocol conversion framework designed to unify multiple proxy standards — including VLESS, VMess, Trojan, and Shadowsocks — into a seamless, intelligent configuration system. It features smart routing, web-based management, research-optimized rule sets, and a beautiful bilingual interface, making it the ultimate tool for both power users and academic network acceleration scenarios.

[中文文档](README_zh.md)

## ✨ Features

### Core Features
- 🔄 **Multi-Protocol Support**: VLESS, VMess, Trojan, Shadowsocks protocols with full parameter support
- 📋 **Subscription Conversion**: Base64 and plain text subscription URL conversion
- 🎯 **Smart Routing**: Built-in rule sets (Balance, Research, Minimal) with custom rule support
- 🔐 **Secure Authentication**: Session-based authentication with 24-hour timeout
- 📱 **RESTful API**: Complete API interface with comprehensive documentation

### Advanced Features
- 🛡️ **SSL/HTTPS Support**: Optional HTTPS encryption with custom domain support
- 📊 **History Management**: Track and manage conversion history with export support
- 🔄 **Auto-Update Subscriptions**: Configurable auto-update intervals
- 📈 **Traffic Limiting**: Set traffic limits for subscriptions
- 🛠️ **Advanced Configuration**: Panel URL base path, logging, database maintenance
- ⚡ **Node Preview & Editing**: Preview and edit node names before generating configurations

## 🚀 Quick Start

### Method 1: One-Click Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/maxiao0234/SubProtoX.git
cd SubProtoX

# Run installation script
sudo bash install.sh
```

The installation script will:
- Create `config.py` from template
- Validate SSL certificates (if configured)
- Install Python dependencies in virtual environment
- Create and enable systemd service
- Start the service automatically

### Method 2: Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/maxiao0234/SubProtoX.git
cd SubProtoX

# 2. Create configuration file
cp config.example.py config.py

# 3. Edit configuration file according to your environment
nano config.py

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the service
python app.py
```

## ⚙️ Configuration

### Configuration File Structure

Copy `config.example.py` to `config.py` and modify according to your environment:

```python
# Server configuration
SERVER_CONFIG = {
    'host': '0.0.0.0',      # Listen address
    'port': 7777,           # Listen port
    'debug': False,         # Debug mode
    'base_path': ''         # Panel URL base path (e.g., 'panel' → '/panel/')
}

# SSL configuration
SSL_CONFIG = {
    'enabled': True,                           # Enable SSL
    'cert_path': '/path/to/your/cert.pem',     # SSL certificate path
    'key_path': '/path/to/your/key.pem',       # SSL private key path
    'domain': 'your-domain.com'                # Custom domain (optional)
}

# Default user configuration (Please change!)
DEFAULT_USER = {
    'username': 'admin',
    'password': 'admin'     # ⚠️ Please change this password after deployment!
}

# Subscription conversion configuration
CONVERTER_CONFIG = {
    'max_proxies': 1000,    # Maximum number of proxies limit
    'timeout': 30,          # Subscription fetch timeout in seconds
    'user_agent': 'SubProtoX/1.0'
}

# Logging configuration
LOG_CONFIG = {
    'level': 'INFO',        # Log level: DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': None            # Log file path, None means console output
}
```

### Important Configuration Items

| Configuration Item | Description | Default Value |
|-------------------|-------------|---------------|
| `SERVER_CONFIG.port` | Service port | 7777 |
| `SERVER_CONFIG.base_path` | Panel URL prefix | '' (root) |
| `SSL_CONFIG.enabled` | Enable HTTPS | False |
| `SSL_CONFIG.domain` | Custom domain | '' |
| `DEFAULT_USER.username` | Default username | admin |
| `DEFAULT_USER.password` | Default password | admin |
| `CONVERTER_CONFIG.max_proxies` | Max proxies per config | 1000 |
| `CONVERTER_CONFIG.timeout` | Fetch timeout (seconds) | 30 |
| `LOG_CONFIG.level` | Logging level | INFO |

## 🔧 Service Management

```bash
# Start service
sudo systemctl start subprotox

# Stop service
sudo systemctl stop subprotox

# Restart service
sudo systemctl restart subprotox

# Check status
sudo systemctl status subprotox

# View logs
sudo journalctl -u subprotox -f

# Enable auto-start on boot
sudo systemctl enable subprotox
```

## 🎯 Routing Rules

| Rule Type | Name | Description | Use Case |
|-----------|------|-------------|----------|
| **Default** | Default Routing | Balanced routing rules | Ordinary usage |
| **Research** | Academic & Research Routing | Academic resource optimization | Research access (GitHub, arXiv, academic APIs) |
| **Minimal** | Minimal Rules | Basic routing with fewer rules | Simplicity and speed |
| **Custom** | User-defined | Fully customizable | Custom routing needs |

## 📂 Project Structure

```
SubProtoX/
├── app.py                      # Main application entry point
├── config.example.py           # Configuration template
├── install.sh                  # Automated installation script
├── uninstall.sh                # Automated uninstallation script
├── requirements.txt            # Python dependencies
├── README.md / README_zh.md    # Documentation (EN/ZH)
├── LICENSE                     # MIT License
│
├── core/                       # Core modules
│   └── converter.py            # SubConverter - protocol parsing & conversion
│
├── rules/                      # Routing rules system
│   ├── rule_manager.py         # RuleManager - rule orchestration
│   ├── base_rules.py           # BaseRuleSet abstract class
│   ├── *_rules.py              # Rule implementations (default, research, minimal)
│   └── proxy_groups.py         # ProxyGroupGenerator
│
├── web/                        # Web interface
│   ├── blueprints/             # Flask blueprints
│   │   ├── auth.py             # Authentication routes
│   │   ├── converter.py        # Conversion API routes
│   │   └── management.py       # Management interface routes
│   │
│   ├── templates/              # HTML templates (as Python modules)
│   │   ├── login.py            # Login page
│   │   └── management.py       # Main management interface
│   │
│   └── i18n/                   # Internationalization
│       └── languages.py        # EN/ZH translations
│
├── utils/                      # Utility modules
│   └── github_api.py           # GitHub API integration (optional)
│
└── static/                     # Static files
    ├── css/                    # Bootstrap CSS
    ├── js/                     # JavaScript libraries
    └── logo/                   # Logo images
```

## 🤝 Contributing

Community contributions are welcome! If you'd like to improve SubProtoX:

1. Fork the project
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Submit Pull Request


## ⚠️ Disclaimer

This project is designed for educational purposes and compliant network environment optimization only. SubProtoX provides network access rule templates exclusively for optimizing academic data synchronization, open-source code access, and academic resource downloads (such as GitHub, arXiv, OpenAI API, etc.) in compliant environments.

**Important Notes:**
- This project does not contain any proxy server information or connectable node configurations
- Users must use this software within legal and compliant network environments
- The project is intended solely for academic research acceleration and legitimate network optimization
- Users are responsible for ensuring compliance with local laws and regulations
- Any consequences arising from the use of this project are the user's responsibility
- The software should not be used for any activities that violate local laws or regulations

## 📞 Support

For community support and project information:

- 🐛 [Report Bug](https://github.com/maxiao0234/SubProtoX/issues)
- 💡 [Feature Request](https://github.com/maxiao0234/SubProtoX/issues)
- 📖 [Documentation](https://github.com/maxiao0234/SubProtoX/wiki)
- 💬 [Discussions](https://github.com/maxiao0234/SubProtoX/discussions)

*Please note: Support is provided on a best-effort community basis.*

## 🌟 Acknowledgments

- Bootstrap 5 for the beautiful UI framework
- Material Symbols for the icon set
- Flask for the lightweight web framework
- The open-source community for inspiration and feedback

---

**If this project helps you, please give it a ⭐ Star!**
