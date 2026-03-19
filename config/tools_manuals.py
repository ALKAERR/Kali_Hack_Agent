TOOL_MANUALS = {

# =========================
# 1️⃣ 信息收集（Recon / OSINT）
# =========================

"amass": {
    "description": "子域名枚举与攻击面发现工具",
    "manual": """
使用命令行方式调用 amass enum -d <domain>
通过 Python subprocess 执行并捕获 stdout
""",
    "return_format": {
        "type": "json",
        "schema": {
            "domains": ["string"]
        }
    }
},

"theharvester": {
    "description": "基于公开数据源收集邮箱、子域名、IP",
    "manual": """
使用 theHarvester -d <domain> -b all
解析文本输出中的 emails / hosts
""",
    "return_format": {
        "type": "json",
        "schema": {
            "emails": ["string"],
            "hosts": ["string"]
        }
    }
},

"recon-ng": {
    "description": "模块化 OSINT 框架",
    "manual": """
以非交互模式执行 recon-ng 脚本
提取模块运行结果
""",
    "return_format": {
        "type": "json",
        "schema": {
            "results": ["string"]
        }
    }
},

"spiderfoot": {
    "description": "自动化 OSINT 收集与关联分析工具",
    "manual": """
通过命令行运行 spiderfoot
解析生成的 JSON/CSV 结果
""",
    "return_format": {
        "type": "json",
        "schema": {
            "artifacts": [{"type": "string", "value": "string"}]
        }
    }
},

"fierce": {
    "description": "DNS 枚举工具",
    "manual": """
执行 fierce --domain <domain>
解析子域名与 IP
""",
    "return_format": {
        "type": "json",
        "schema": {
            "subdomains": [{"domain": "string", "ip": "string"}]
        }
    }
},

"dnsenum": {
    "description": "DNS 枚举与区域传送检测工具",
    "manual": """
执行 dnsenum <domain>
解析输出中的 DNS 记录
""",
    "return_format": {
        "type": "json",
        "schema": {
            "records": [{"type": "string", "value": "string"}]
        }
    }
},

"nbtscan": {
    "description": "NetBIOS 主机信息探测工具",
    "manual": """
执行 nbtscan <CIDR>
解析主机名与 IP
""",
    "return_format": {
        "type": "json",
        "schema": {
            "hosts": [{"ip": "string", "name": "string"}]
        }
    }
},

"arp-scan": {
    "description": "ARP 网络扫描工具",
    "manual": """
执行 arp-scan <interface> --localnet
解析 IP/MAC
""",
    "return_format": {
        "type": "json",
        "schema": {
            "devices": [{"ip": "string", "mac": "string"}]
        }
    }
},

"kismet": {
    "description": "无线监听与设备发现工具",
    "manual": """
通过命令行启动 kismet 日志模式
解析生成的设备信息
""",
    "return_format": {
        "type": "json",
        "schema": {
            "devices": [{"mac": "string", "type": "string"}]
        }
    }
},

"wafw00f": {
    "description": "Web 应用防火墙识别工具",
    "manual": """
执行 wafw00f <url>
解析识别结果
""",
    "return_format": {
        "type": "json",
        "schema": {
            "waf": "string"
        }
    }
},

# =========================
# 2️⃣ 网络扫描与服务发现
# =========================

"nmap": {
    "description": "网络扫描工具，用于端口扫描、服务识别、操作系统检测",
    "manual": """
独立编写代码，在python里调用命令行执行 nmap，注意执行时选择扫描最快的方法
""",
    "return_format": {
        "type": "json",
        "schema": {
            "hosts": [{
                "ip": "string",
                "ports": [{
                    "port": "int",
                    "protocol": "string",
                    "state": "string",
                    "service": "string"
                }]
            }]
        }
    }
},

"masscan": {
    "description": "高速端口扫描工具",
    "manual": """
执行 masscan <target> -p <ports>
解析开放端口
""",
    "return_format": {
        "type": "json",
        "schema": {
            "open_ports": [{"ip": "string", "port": "int"}]
        }
    }
},

"tcpdump": {
    "description": "网络流量抓包工具",
    "manual": """
执行 tcpdump -i <iface> -c <count>
解析抓取的包摘要
""",
    "return_format": {
        "type": "json",
        "schema": {
            "packets": [{"src": "string", "dst": "string", "protocol": "string"}]
        }
    }
},

"tshark": {
    "description": "命令行版 Wireshark",
    "manual": """
使用 tshark 读取 pcap 或实时抓包
""",
    "return_format": {
        "type": "json",
        "schema": {
            "frames": ["string"]
        }
    }
},

"wireshark": {
    "description": "图形化网络分析工具（仅解析输出）",
    "manual": """
读取已有 pcap 文件，不启动 GUI
""",
    "return_format": {
        "type": "json",
        "schema": {
            "summary": "string"
        }
    }
},

"httpx": {
    "description": "HTTP 服务探测与指纹识别工具",
    "manual": """
执行 httpx -u <url>
解析状态码、标题、指纹,页面内容
""",
    "return_format": {
        "type": "json",
        "schema": {
            "http_services": [{
                "url": "string",
                "status": "int",
                "title": "string",
                "fingerprint": "string",
                "body": "string"
            }]
        }
    }
},

"curl": {
    "description": "HTTP 请求工具",
    "manual": """
通过 curl 发起 HTTP 请求
捕获响应，注意添加-L允许重定向
""",
    "return_format": {
        "type": "json",
        "schema": {
            "status": "int",
            "headers": "string",
            "body": "string"
        }
    }
},

# =========================
# 3️⃣ 枚举 / 4️⃣ Web / 5️⃣ Exploit / 6️⃣ Crypto / 7️⃣ Wireless / 8️⃣ Reverse / 9️⃣ Forensics / 🔟 Post
# =========================
"enum4linux": {
    "description": "Windows / Samba 枚举工具",
    "manual": """
执行 enum4linux <ip>
解析用户、共享、SID 等信息
""",
    "return_format": {
        "type": "json",
        "schema": {
            "users": ["string"],
            "shares": ["string"]
        }
    }
},

"rpcclient": {
    "description": "RPC 服务枚举工具",
    "manual": """
使用 rpcclient -U '' <ip> 执行枚举命令
解析返回内容
""",
    "return_format": {
        "type": "json",
        "schema": {
            "rpc_info": ["string"]
        }
    }
},

"smbmap": {
    "description": "SMB 共享与权限枚举工具",
    "manual": """
执行 smbmap -H <ip>
解析共享权限
""",
    "return_format": {
        "type": "json",
        "schema": {
            "shares": [{"name": "string", "permission": "string"}]
        }
    }
},

"dirb": {
    "description": "Web 目录爆破工具",
    "manual": """
执行 dirb <url> -S
解析发现的路径
""",
    "return_format": {
        "type": "json",
        "schema": {
            "paths": ["string"]
        }
    }
},

"gobuster": {
    "description": "高性能目录与子域枚举工具",
    "manual": """
执行 gobuster dir -u <url> -w /usr/share/seclists/Discovery/Web-Content/common.txt
""",
    "return_format": {
        "type": "json",
        "schema": {
            "paths": ["string"]
        }
    }
},

"ffuf": {
    "description": "快速模糊测试/路径枚举工具",
    "manual": """
执行 ffuf -u <url>/FUZZ -w <wordlist>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "matches": [{"url": "string", "status": "int"}]
        }
    }
},

"wfuzz": {
    "description": "Web 参数与目录模糊测试工具",
    "manual": """
执行 wfuzz -c -z file,<wordlist> <url>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "results": ["string"]
        }
    }
},

"nikto": {
    "description": "Web 漏洞扫描与配置检测工具",
    "manual": """
执行 nikto -h <url>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "issues": ["string"]
        }
    }
},

"wpscan": {
    "description": "WordPress 枚举与漏洞扫描工具",
    "manual": """
执行 wpscan --url <url>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "findings": ["string"]
        }
    }
},

"nxc": {
    "description": "多协议枚举与横向渗透工具（NetExec）",
    "manual": """
执行 nxc smb <ip>
解析枚举输出
""",
    "return_format": {
        "type": "json",
        "schema": {
            "results": ["string"]
        }
    }
},
"burpsuite": {
    "description": "Web 请求拦截与重放工具（导出请求分析）",
    "manual": """
解析 Burp 导出的 HTTP 请求/响应数据
""",
    "return_format": {
        "type": "json",
        "schema": {
            "requests": ["string"],
            "responses": ["string"]
        }
    }
},

"sqlmap": {
    "description": "自动化 SQL 注入利用工具",
    "manual": """
执行 sqlmap -u <url> --batch
""",
    "return_format": {
        "type": "json",
        "schema": {
            "databases": ["string"],
            "tables": ["string"]
        }
    }
},
"msfconsole": {
    "description": "Metasploit 漏洞利用框架",
    "manual": """
通过 msfconsole 脚本化执行 exploit 模块
""",
    "return_format": {
        "type": "json",
        "schema": {
            "sessions": ["string"]
        }
    }
},

"msfvenom": {
    "description": "Payload 生成工具",
    "manual": """
执行 msfvenom 生成 Payload 文件
""",
    "return_format": {
        "type": "json",
        "schema": {
            "payload_path": "string"
        }
    }
},

"searchsploit": {
    "description": "本地 Exploit 数据库搜索工具",
    "manual": """
执行 searchsploit <keyword>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "exploits": [{"id": "string", "title": "string"}]
        }
    }
},

"evil-winrm": {
    "description": "Windows WinRM Shell 工具",
    "manual": """
执行 evil-winrm -i <ip> -u <user> -p <pass>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "shell": "string"
        }
    }
},

"hydra": {
    "description": "多协议口令爆破工具",
    "manual": """
执行 hydra -l <user> -P <passlist> <service>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "credentials": [{"user": "string", "password": "string"}]
        }
    }
},

"medusa": {
    "description": "并行密码爆破工具",
    "manual": """
执行 medusa -h <host> -u <user> -P <passlist>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "credentials": [{"user": "string", "password": "string"}]
        }
    }
},

"patator": {
    "description": "模块化暴力破解框架",
    "manual": """
执行 patator 模块化攻击
""",
    "return_format": {
        "type": "json",
        "schema": {
            "results": ["string"]
        }
    }
},

"responder": {
    "description": "LLMNR/NBT-NS 欺骗与凭据捕获工具",
    "manual": """
执行 responder -I <iface>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "hashes": ["string"]
        }
    }
},
"hashcat": {
    "description": "GPU 加速 Hash 破解工具",
    "manual": """
执行 hashcat -m <mode> -a 0 <hash> <wordlist>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "cracked": [{"hash": "string", "password": "string"}]
        }
    }
},

"john": {
    "description": "John the Ripper 密码破解工具",
    "manual": """
执行 john <hashfile>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "cracked": [{"hash": "string", "password": "string"}]
        }
    }
},

"ophcrack": {
    "description": "基于彩虹表的密码破解工具",
    "manual": """
执行 ophcrack 并解析结果
""",
    "return_format": {
        "type": "json",
        "schema": {
            "passwords": ["string"]
        }
    }
},

"hash-identifier": {
    "description": "Hash 类型识别工具",
    "manual": """
执行 hash-identifier 并解析候选算法
""",
    "return_format": {
        "type": "json",
        "schema": {
            "possible_types": ["string"]
        }
    }
},
"airmon-ng": {
    "description": "无线网卡监听模式工具",
    "manual": """
执行 airmon-ng start <iface>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "monitor_interface": "string"
        }
    }
},

"airodump-ng": {
    "description": "无线网络监听与抓包工具",
    "manual": """
执行 airodump-ng <iface>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "networks": [{"bssid": "string", "channel": "int"}]
        }
    }
},

"aireplay-ng": {
    "description": "无线重放与去认证攻击工具",
    "manual": """
执行 aireplay-ng 攻击模式
""",
    "return_format": {
        "type": "json",
        "schema": {
            "status": "string"
        }
    }
},

"aircrack-ng": {
    "description": "无线密钥破解工具",
    "manual": """
执行 aircrack-ng <capture>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "key": "string"
        }
    }
},
"angr": {
    "description": "基于符号执行的二进制分析工具",
    "manual": """
使用 Python angr API 进行分析
""",
    "return_format": {
        "type": "json",
        "schema": {
            "paths": ["string"]
        }
    }
},

"radare2": {
    "description": "交互式逆向工程框架",
    "manual": """
执行 r2 -c 指令并解析输出
""",
    "return_format": {
        "type": "json",
        "schema": {
            "functions": ["string"]
        }
    }
},

"objdump": {
    "description": "二进制反汇编工具",
    "manual": """
执行 objdump -d <binary>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "assembly": ["string"]
        }
    }
},

"checksec": {
    "description": "二进制安全机制检测工具",
    "manual": """
执行 checksec <binary>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "protections": ["string"]
        }
    }
},

"strings": {
    "description": "二进制字符串提取工具",
    "manual": """
执行 strings <binary>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "strings": ["string"]
        }
    }
},

"file": {
    "description": "文件类型识别工具",
    "manual": """
执行 file <target>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "file_type": "string"
        }
    }
},

"xxd": {
    "description": "十六进制查看与转换工具",
    "manual": """
执行 xxd <file>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "hex": "string"
        }
    }
},
"autopsy": {
    "description": "数字取证分析平台",
    "manual": """
解析 Autopsy 项目导出结果
""",
    "return_format": {
        "type": "json",
        "schema": {
            "artifacts": ["string"]
        }
    }
},

"binwalk": {
    "description": "固件与嵌入文件分析工具",
    "manual": """
执行 binwalk <file>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "embedded": ["string"]
        }
    }
},

"exiftool": {
    "description": "文件元数据分析工具",
    "manual": """
执行 exiftool <file>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "metadata": {"key": "value"}
        }
    }
},

"photorec": {
    "description": "文件恢复工具",
    "manual": """
执行 photorec 并解析恢复列表
""",
    "return_format": {
        "type": "json",
        "schema": {
            "recovered_files": ["string"]
        }
    }
},

"testdisk": {
    "description": "磁盘分区与文件恢复工具",
    "manual": """
执行 testdisk 非交互恢复
""",
    "return_format": {
        "type": "json",
        "schema": {
            "partitions": ["string"]
        }
    }
},

"scalpel": {
    "description": "文件雕刻工具",
    "manual": """
执行 scalpel <image>
""",
    "return_format": {
        "type": "json",
        "schema": {
            "files": ["string"]
        }
    }
},
"evil-winrm": {
    "description": "基于 WinRM 的 Windows 后渗透交互式 Shell 工具",
    "manual": """
通过 evil-winrm 连接已获取凭据的 Windows 主机
执行系统命令、上传下载文件、权限验证
使用 Python subprocess 调用命令行并捕获输出
""",
    "return_format": {
        "type": "json",
        "schema": {
            "host": "string",
            "user": "string",
            "output": ["string"]
        }
    }
},

"responder": {
    "description": "用于内网监听与欺骗的凭据捕获工具（LLMNR/NBT-NS）",
    "manual": """
在内网环境中运行 responder
捕获 NTLMv1/v2 Hash 信息
解析并结构化输出
""",
    "return_format": {
        "type": "json",
        "schema": {
            "captured_hashes": [
                {
                    "username": "string",
                    "hash": "string",
                    "protocol": "string"
                }
            ]
        }
    }
},

"msfconsole": {
    "description": "Metasploit 框架，用于后渗透操作与横向移动",
    "manual": """
通过 msfconsole 非交互脚本模式
执行 post 模块、内网扫描、凭据收集等操作
解析 session 与模块输出
""",
    "return_format": {
        "type": "json",
        "schema": {
            "sessions": [
                {
                    "session_id": "string",
                    "type": "string",
                    "target": "string"
                }
            ]
        }
    }
},

"smbmap": {
    "description": "内网 SMB 共享与权限枚举工具（横向移动前置）",
    "manual": """
使用 smbmap 枚举内网主机共享资源
验证读写权限，为横向移动做准备
""",
    "return_format": {
        "type": "json",
        "schema": {
            "host": "string",
            "shares": [
                {
                    "name": "string",
                    "permission": "string"
                }
            ]
        }
    }
},

"rpcclient": {
    "description": "基于 RPC 的 Windows 内部信息枚举工具",
    "manual": """
通过 rpcclient 对内网 Windows 主机执行枚举命令
获取用户、组、SID 等信息
""",
    "return_format": {
        "type": "json",
        "schema": {
            "host": "string",
            "users": ["string"],
            "groups": ["string"]
        }
    }
},
}
