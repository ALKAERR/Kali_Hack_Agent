"""Tool to Category Mapping for Level 1 Agent."""

# 工具名称到类别的映射
# 这个映射用于一级Agent根据工具名称进行准确分类
# 注意：某些工具可能适用于多个类别，这里列出的是主要/最常见的用途

TOOL_TO_CATEGORY = {
    # 信息收集 (information_collection)
    "amass": "information_collection",
    "theharvester": "information_collection",
    "the-harvester": "information_collection",  # 别名
    "recon-ng": "information_collection",
    "reconng": "information_collection",  # 别名
    "spiderfoot": "information_collection",
    "spider-foot": "information_collection",  # 别名
    "fierce": "information_collection",
    "dnsenum": "information_collection",
    "dns-enum": "information_collection",  # 别名
    "nbtscan": "information_collection",
    "nbt-scan": "information_collection",  # 别名
    "arp-scan": "information_collection",
    "arpscan": "information_collection",  # 别名
    "wafw00f": "information_collection",
    
    # 扫描与服务发现 (scanning)
    "nmap": "scanning",
    "masscan": "scanning",
    "mass-can": "scanning",  # 别名
    "tcpdump": "scanning",
    "tcp-dump": "scanning",  # 别名
    "tshark": "scanning",
    "wireshark": "scanning",
    "wire-shark": "scanning",  # 别名
    "httpx": "scanning",
    "http-x": "scanning",  # 别名
    
    # 枚举 (enumeration)
    "enum4linux": "enumeration",
    "enum4linux-ng": "enumeration",  # 别名
    "dirb": "enumeration",
    "nxc": "enumeration",
    "netexec": "enumeration",  # 别名
    "rpcclient": "enumeration",  # 注意：也在post_exploitation中，但枚举更常见
    "rpc-client": "enumeration",  # 别名
    "smbmap": "enumeration",  # 注意：也在post_exploitation中，但枚举更常见
    "smb-map": "enumeration",  # 别名
    "ffuf": "enumeration",  # 注意：也在web_exploitation中
    "wfuzz": "enumeration",  # 注意：也在web_exploitation中
    "w-fuzz": "enumeration",  # 别名
    "nikto": "enumeration",  # 注意：也在web_exploitation中
    "wpscan": "enumeration",  # 注意：也在web_exploitation中
    "wp-scan": "enumeration",  # 别名
    "gobuster": "enumeration",  # 注意：也在scanning和web_exploitation中
    "go-buster": "enumeration",  # 别名
    "curl": "enumeration",  # 注意：在多个类别中，但枚举场景最常见
    
    # Web利用 (web_exploitation)
    "sqlmap": "web_exploitation",
    "sql-map": "web_exploitation",  # 别名
    "burpsuite": "web_exploitation",
    "burp-suite": "web_exploitation",  # 别名
    "burp": "web_exploitation",  # 别名
    
    # 漏洞利用 (exploitation)
    "msfvenom": "exploitation",
    "msf-venom": "exploitation",  # 别名
    "searchsploit": "exploitation",
    "search-sploit": "exploitation",  # 别名
    "hydra": "exploitation",  # 注意：也在password_crypto中，但利用更常见
    "medusa": "exploitation",  # 注意：也在password_crypto中，但利用更常见
    "patator": "exploitation",  # 注意：也在password_crypto中，但利用更常见
    "msfconsole": "exploitation",  # 注意：也在post_exploitation中，但利用更常见
    "msf-console": "exploitation",  # 别名
    "metasploit": "exploitation",  # 别名
    "msf": "exploitation",  # 别名
    "evil-winrm": "exploitation",  # 注意：也在post_exploitation中，但利用更常见
    "evilwinrm": "exploitation",  # 别名
    "responder": "exploitation",  # 注意：也在post_exploitation中，但利用更常见
    
    # 密码破解 (password_crypto)
    "hashcat": "password_crypto",
    "hash-cat": "password_crypto",  # 别名
    "john": "password_crypto",
    "john-the-ripper": "password_crypto",  # 别名
    "jtr": "password_crypto",  # 别名
    "ophcrack": "password_crypto",
    "oph-crack": "password_crypto",  # 别名
    "hash-identifier": "password_crypto",
    "hashidentifier": "password_crypto",  # 别名
    
    # 无线攻击 (wireless_attack)
    "airmon-ng": "wireless_attack",
    "airmon": "wireless_attack",  # 别名
    "airodump-ng": "wireless_attack",
    "airodump": "wireless_attack",  # 别名
    "aireplay-ng": "wireless_attack",
    "aireplay": "wireless_attack",  # 别名
    "aircrack-ng": "wireless_attack",
    "aircrack": "wireless_attack",  # 别名
    "kismet": "wireless_attack",  # 注意：也在information_collection中，但无线攻击更常见
    
    # 逆向工程 (reverse_engineering)
    "angr": "reverse_engineering",
    "radare2": "reverse_engineering",
    "r2": "reverse_engineering",  # 别名
    "radare": "reverse_engineering",  # 别名
    "objdump": "reverse_engineering",
    "obj-dump": "reverse_engineering",  # 别名
    "checksec": "reverse_engineering",
    "check-sec": "reverse_engineering",  # 别名
    "strings": "reverse_engineering",
    "file": "reverse_engineering",
    "xxd": "reverse_engineering",
    
    # 数字取证 (forensics)
    "autopsy": "forensics",
    "binwalk": "forensics",
    "bin-walk": "forensics",  # 别名
    "exiftool": "forensics",
    "exif-tool": "forensics",  # 别名
    "photorec": "forensics",
    "photo-rec": "forensics",  # 别名
    "testdisk": "forensics",
    "test-disk": "forensics",  # 别名
    "scalpel": "forensics",
    
    # 后渗透 (post_exploitation)
    # 注意：以下工具的主要用途在其他类别，但明确用于后渗透场景时选择此类别
}

# 多类别工具映射（工具可能在多个类别中使用）
MULTI_CATEGORY_TOOLS = {
    "curl": ["information_collection", "scanning", "enumeration", "web_exploitation"],
    "gobuster": ["scanning", "enumeration", "web_exploitation"],
    "nikto": ["enumeration", "web_exploitation"],
    "wpscan": ["enumeration", "web_exploitation"],
    "ffuf": ["enumeration", "web_exploitation"],
    "wfuzz": ["enumeration", "web_exploitation"],
    "hydra": ["exploitation", "password_crypto"],
    "medusa": ["exploitation", "password_crypto"],
    "patator": ["exploitation", "password_crypto"],
    "msfconsole": ["exploitation", "post_exploitation"],
    "evil-winrm": ["exploitation", "post_exploitation"],
    "responder": ["exploitation", "post_exploitation"],
    "smbmap": ["enumeration", "post_exploitation"],
    "rpcclient": ["enumeration", "post_exploitation"],
    "kismet": ["information_collection", "wireless_attack"],
    "tcpdump": ["scanning", "forensics"],
    "tshark": ["scanning", "forensics"],
    "wireshark": ["scanning", "forensics"],
}

# 类别描述
CATEGORY_DESCRIPTIONS = {
    "information_collection": "信息收集与OSINT（开放源情报）工具，包括域名枚举、DNS查询、子域名发现、邮箱收集等",
    "scanning": "网络扫描与服务发现工具，包括端口扫描、服务识别、流量分析等",
    "enumeration": "服务枚举与攻击面扩展工具，包括SMB枚举、RPC枚举、Web目录枚举等",
    "web_exploitation": "Web漏洞利用工具，包括SQL注入、Web漏洞扫描等",
    "exploitation": "漏洞利用与初始控制工具，包括Metasploit、Payload生成、凭证爆破等",
    "password_crypto": "密码破解与加密分析工具，包括Hash破解、密码爆破等",
    "wireless_attack": "无线网络攻击工具，包括WiFi监听、密钥破解等",
    "reverse_engineering": "二进制分析与逆向工程工具，包括反汇编、符号执行等",
    "forensics": "数字取证与数据恢复工具，包括文件分析、数据恢复等",
    "post_exploitation": "后渗透与内网横向移动工具，包括权限提升、横向移动等",
    "custom_code": "自定义代码执行，用于执行用户自定义的Python代码或脚本",
}

# 生成工具列表字符串用于一级Agent
def get_tool_category_mapping_text():
    """生成工具到类别的映射文本，用于一级Agent的instructions"""
    lines = ["\n📋 工具到类别映射（重要：如果用户明确指定了工具名称，请根据此映射分类）：\n"]
    
    # 按类别组织工具
    category_tools = {}
    for tool, category in TOOL_TO_CATEGORY.items():
        if category not in category_tools:
            category_tools[category] = []
        category_tools[category].append(tool)
    
    for category, tools in sorted(category_tools.items()):
        category_desc = CATEGORY_DESCRIPTIONS.get(category, "")
        lines.append(f"\n【{category}】{category_desc}")
        # 去重并排序
        unique_tools = sorted(set(tools))
        lines.append(f"工具列表: {', '.join(unique_tools)}")
    
    # 添加多类别工具的说明
    if MULTI_CATEGORY_TOOLS:
        lines.append("\n\n⚠️ 多类别工具说明（这些工具可能属于多个类别，需要根据上下文判断）：")
        for tool, categories in sorted(MULTI_CATEGORY_TOOLS.items()):
            main_category = TOOL_TO_CATEGORY.get(tool, "未知")
            lines.append(f"  - {tool}: 主要类别={main_category}, 也可用于={', '.join(categories)}")
    
    lines.append("\n\n⚠️ 分类规则（按优先级）：")
    lines.append("1. 【最高优先级】如果用户明确提到了工具名称（如'使用nmap扫描'、'用sqlmap测试'），必须根据上述映射选择对应的target")
    lines.append("2. 工具名称不区分大小写（如nmap/Nmap/NMAP都视为同一工具）")
    lines.append("3. 如果工具名称有多种写法，参考别名（如metasploit/msf/msfconsole都指向同一工具）")
    lines.append("4. 对于多类别工具，按以下规则处理：")
    lines.append("   - 优先选择映射表中的主要类别")
    lines.append("   - 如果任务描述中包含明确的场景关键词，选择匹配的类别")
    lines.append("   - 例如：'用gobuster枚举目录' → enumeration，'用gobuster扫描端口' → scanning")
    lines.append("   - 例如：'用hydra爆破SSH' → exploitation，'用hydra破解密码' → password_crypto")
    lines.append("5. 如果用户没有明确指定工具，则根据任务描述的内容进行分类")
    lines.append("6. 如果工具名称在映射表中找不到，根据任务描述的关键词进行分类")
    
    return "\n".join(lines)
