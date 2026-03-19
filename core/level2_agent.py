"""Level 2 Agents: Domain Experts."""

from agents import Agent
from config.execute_config import MODEL_NAME, MODEL_CONFIG
from core.level3_agent import tool_executors
from config.tools_manuals import TOOL_MANUALS

agent_information_collection = Agent(
    name="Information Collection Expert",
    instructions=(
        "你是信息收集与OSINT领域工具调用专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - Amass（域名与子域收集）: {TOOL_MANUALS['amass']['description']}\n"
        f"   - TheHarvester（邮箱、域名、人员信息）: {TOOL_MANUALS['theharvester']['description']}\n"
        f"   - Recon-ng（模块化OSINT框架）: {TOOL_MANUALS['recon-ng']['description']}\n"
        f"   - SpiderFoot（自动化情报关联分析）: {TOOL_MANUALS['spiderfoot']['description']}\n"
        f"   - Fierce（DNS侦察）: {TOOL_MANUALS['fierce']['description']}\n"
        f"   - Dnsenum（DNS枚举）: {TOOL_MANUALS['dnsenum']['description']}\n"
        f"   - Nbtscan（NetBIOS信息收集）: {TOOL_MANUALS['nbtscan']['description']}\n"
        f"   - Arp-scan（局域网主机发现）: {TOOL_MANUALS['arp-scan']['description']}\n"
        f"   - Kismet（无线设备探测）: {TOOL_MANUALS['kismet']['description']}\n"
        f"   - Wafw00f（Web应用防火墙识别）: {TOOL_MANUALS['wafw00f']['description']}\n"
        f"   - Curl（HTTP请求工具，网页内容获取）: {TOOL_MANUALS['curl']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['amass'],
        tool_executors['theharvester'],
        tool_executors['recon-ng'],
        tool_executors['spiderfoot'],
        tool_executors['fierce'],
        tool_executors['dnsenum'],
        tool_executors['nbtscan'],
        tool_executors['arp-scan'],
        tool_executors['curl'],
        tool_executors['kismet'],
        tool_executors['wafw00f'],
    ],
)

agent_scanning = Agent(
    name="Scanning & Service Discovery Expert",
    instructions=(
        "你是网络扫描工具调度专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - Nmap（端口与服务识别）: {TOOL_MANUALS['nmap']['description']}\n"
        f"   - Masscan（高速端口扫描）: {TOOL_MANUALS['masscan']['description']}\n"
        f"   - Tcpdump（原始流量捕获）: {TOOL_MANUALS['tcpdump']['description']}\n"
        f"   - Tshark（命令行流量分析）: {TOOL_MANUALS['tshark']['description']}\n"
        f"   - Wireshark（图形化流量分析）: {TOOL_MANUALS['wireshark']['description']}\n"
        f"   - Httpx（Web服务探测）: {TOOL_MANUALS['httpx']['description']}\n"
        f"   - Curl（HTTP响应验证）: {TOOL_MANUALS['curl']['description']}\n"
        f"   - Gobuster（目录/子域爆破）: {TOOL_MANUALS['gobuster']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['nmap'],
        tool_executors['masscan'],
        tool_executors['tcpdump'],
        tool_executors['tshark'],
        tool_executors['wireshark'],
        tool_executors['httpx'],
        tool_executors['curl'],
        tool_executors['gobuster'],
    ],
)

agent_enumeration = Agent(
    name="Enumeration Expert",
    instructions=(
        "你是服务枚举与攻击面扩展工具调用专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - Enum4linux（SMB 枚举）: {TOOL_MANUALS['enum4linux']['description']}\n"
        f"   - Rpcclient（RPC 服务枚举）: {TOOL_MANUALS['rpcclient']['description']}\n"
        f"   - Smbmap（共享与权限枚举）: {TOOL_MANUALS['smbmap']['description']}\n"
        f"   - Dirb（Web 目录枚举）: {TOOL_MANUALS['dirb']['description']}\n"
        f"   - Gobuster（目录/子域爆破）: {TOOL_MANUALS['gobuster']['description']}\n"
        f"   - FFUF（参数/路径模糊测试）: {TOOL_MANUALS['ffuf']['description']}\n"
        f"   - Wfuzz（Web 接口枚举）: {TOOL_MANUALS['wfuzz']['description']}\n"
        f"   - Nikto（Web 配置与漏洞枚举）: {TOOL_MANUALS['nikto']['description']}\n"
        f"   - WPScan（WordPress 枚举）: {TOOL_MANUALS['wpscan']['description']}\n"
        f"   - NXC（网络协议枚举）: {TOOL_MANUALS['nxc']['description']}\n"
        f"   - Curl（HTTP响应验证）: {TOOL_MANUALS['curl']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['enum4linux'],
        tool_executors['rpcclient'],
        tool_executors['smbmap'],
        tool_executors['dirb'],
        tool_executors['gobuster'],
        tool_executors['ffuf'],
        tool_executors['wfuzz'],
        tool_executors['nikto'],
        tool_executors['curl'],
        tool_executors['wpscan'],
        tool_executors['nxc'],
    ],
)

agent_web_exploitation = Agent(
    name="Web Exploitation Expert",
    instructions=(
        "你是Web漏洞利用工具调用专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - SQLMap（SQL注入）: {TOOL_MANUALS['sqlmap']['description']}\n"
        f"   - Nikto（Web漏洞扫描）: {TOOL_MANUALS['nikto']['description']}\n"
        f"   - Wfuzz（参数与接口 fuzz）: {TOOL_MANUALS['wfuzz']['description']}\n"
        f"   - FFUF（路径与参数爆破）: {TOOL_MANUALS['ffuf']['description']}\n"
        f"   - Gobuster（Web 枚举辅助）: {TOOL_MANUALS['gobuster']['description']}\n"
        f"   - WPScan（WordPress 漏洞）: {TOOL_MANUALS['wpscan']['description']}\n"
        f"   - Curl（HTTP请求工具，网页内容获取）: {TOOL_MANUALS['curl']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['sqlmap'],
        tool_executors['nikto'],
        tool_executors['wfuzz'],
        tool_executors['ffuf'],
        tool_executors['gobuster'],
        tool_executors['wpscan'],
        tool_executors['curl'],
    ],
)

agent_exploitation = Agent(
    name="Exploitation Expert",
    instructions=(
        "你是漏洞利用与初始控制工具调用专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - Metasploit Console: {TOOL_MANUALS['msfconsole']['description']}\n"
        f"   - Msfvenom（Payload生成）: {TOOL_MANUALS['msfvenom']['description']}\n"
        f"   - Searchsploit（EXP搜索）: {TOOL_MANUALS['searchsploit']['description']}\n"
        f"   - Evil-WinRM（Windows 远程Shell）: {TOOL_MANUALS['evil-winrm']['description']}\n"
        f"   - Hydra（在线爆破）: {TOOL_MANUALS['hydra']['description']}\n"
        f"   - Medusa（并行爆破）: {TOOL_MANUALS['medusa']['description']}\n"
        f"   - Patator（通用爆破框架）: {TOOL_MANUALS['patator']['description']}\n"
        f"   - Responder（凭证捕获）: {TOOL_MANUALS['responder']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['msfconsole'],
        tool_executors['msfvenom'],
        tool_executors['searchsploit'],
        tool_executors['evil-winrm'],
        tool_executors['hydra'],
        tool_executors['medusa'],
        tool_executors['patator'],
        tool_executors['responder'],
    ],
)

agent_password_crypto = Agent(
    name="Password & Cryptanalysis Expert",
    instructions=(
        "你是密码破解与加密分析领域工具调用专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - Hash-Identifier（Hash类型识别）: {TOOL_MANUALS['hash-identifier']['description']}\n"
        f"   - Hashcat（GPU加速Hash破解）: {TOOL_MANUALS['hashcat']['description']}\n"
        f"   - John（通用密码破解）: {TOOL_MANUALS['john']['description']}\n"
        f"   - Ophcrack（彩虹表破解）: {TOOL_MANUALS['ophcrack']['description']}\n"
        f"   - Hydra（在线口令爆破）: {TOOL_MANUALS['hydra']['description']}\n"
        f"   - Medusa（并行口令攻击）: {TOOL_MANUALS['medusa']['description']}\n"
        f"   - Patator（模块化爆破框架）: {TOOL_MANUALS['patator']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['hash-identifier'],
        tool_executors['hashcat'],
        tool_executors['john'],
        tool_executors['ophcrack'],
        tool_executors['hydra'],
        tool_executors['medusa'],
        tool_executors['patator'],
    ],
)

agent_wireless_attack = Agent(
    name="Wireless Attack Expert",
    instructions=(
        "你是无线网络攻击领域工具调用专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - Airmon-ng（无线网卡监听模式）: {TOOL_MANUALS['airmon-ng']['description']}\n"
        f"   - Airodump-ng（无线数据包抓取）: {TOOL_MANUALS['airodump-ng']['description']}\n"
        f"   - Aireplay-ng（重放与认证攻击）: {TOOL_MANUALS['aireplay-ng']['description']}\n"
        f"   - Aircrack-ng（无线密钥破解）: {TOOL_MANUALS['aircrack-ng']['description']}\n"
        f"   - Kismet（无线设备与流量探测）: {TOOL_MANUALS['kismet']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['airmon-ng'],
        tool_executors['airodump-ng'],
        tool_executors['aireplay-ng'],
        tool_executors['aircrack-ng'],
        tool_executors['kismet'],
    ],
)

agent_reverse_engineering = Agent(
    name="Reverse Engineering Expert",
    instructions=(
        "你是二进制分析与逆向工程领域工具调用专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - File（文件类型识别）: {TOOL_MANUALS['file']['description']}\n"
        f"   - Checksec（二进制安全机制检测）: {TOOL_MANUALS['checksec']['description']}\n"
        f"   - Strings（可见字符串提取）: {TOOL_MANUALS['strings']['description']}\n"
        f"   - Objdump（反汇编与段信息）: {TOOL_MANUALS['objdump']['description']}\n"
        f"   - Radare2（交互式逆向分析）: {TOOL_MANUALS['radare2']['description']}\n"
        f"   - Angr（符号执行与程序分析）: {TOOL_MANUALS['angr']['description']}\n"
        f"   - XXD（二进制/十六进制查看）: {TOOL_MANUALS['xxd']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['file'],
        tool_executors['checksec'],
        tool_executors['strings'],
        tool_executors['objdump'],
        tool_executors['radare2'],
        tool_executors['angr'],
        tool_executors['xxd'],
    ],
)

agent_forensics = Agent(
    name="Digital Forensics Expert",
    instructions=(
        "你是数字取证与数据恢复工具调用专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - Autopsy（综合数字取证平台）: {TOOL_MANUALS['autopsy']['description']}\n"
        f"   - Binwalk（固件与文件嵌入分析）: {TOOL_MANUALS['binwalk']['description']}\n"
        f"   - Exiftool（元数据分析）: {TOOL_MANUALS['exiftool']['description']}\n"
        f"   - Scalpel（文件雕刻）: {TOOL_MANUALS['scalpel']['description']}\n"
        f"   - Photorec（数据恢复）: {TOOL_MANUALS['photorec']['description']}\n"
        f"   - Testdisk（分区修复）: {TOOL_MANUALS['testdisk']['description']}\n"
        f"   - Tcpdump（网络流量抓取）: {TOOL_MANUALS['tcpdump']['description']}\n"
        f"   - Tshark（流量解析）: {TOOL_MANUALS['tshark']['description']}\n"
        f"   - Wireshark（可视化流量分析）: {TOOL_MANUALS['wireshark']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['autopsy'],
        tool_executors['binwalk'],
        tool_executors['exiftool'],
        tool_executors['scalpel'],
        tool_executors['photorec'],
        tool_executors['testdisk'],
        tool_executors['tcpdump'],
        tool_executors['tshark'],
        tool_executors['wireshark'],
    ],
)

agent_post_exploitation = Agent(
    name="Post-Exploitation & Lateral Movement Expert",
    instructions=(
        "你是后渗透与内网横向移动领域专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案\n"
        "- 你【禁止】说'我将使用''我会调用'等描述性语句\n"
        "- 你【只能】做一件事：选择工具并立即 handoff 到三级 Agent\n"
        f"   - Evil-WinRM（Windows 远程 Shell 与控制）: {TOOL_MANUALS['evil-winrm']['description']}\n"
        f"   - Responder（内网监听与凭据捕获）: {TOOL_MANUALS['responder']['description']}\n"
        f"   - Metasploit（后渗透模块与横向移动）: {TOOL_MANUALS['msfconsole']['description']}\n"
        f"   - SMBMap（SMB 共享枚举与权限探测）: {TOOL_MANUALS['smbmap']['description']}\n"
        f"   - Rpcclient（Windows 内部 RPC 枚举）: {TOOL_MANUALS['rpcclient']['description']}\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    handoffs=[
        tool_executors['evil-winrm'],
        tool_executors['responder'],
        tool_executors['msfconsole'],
        tool_executors['smbmap'],
        tool_executors['rpcclient'],
    ],
)

# 自定义代码执行Agent - 可以直接执行Python代码
from core.tools import python_execute

agent_custom_code = Agent(
    name="Custom Code Executor",
    instructions=(
        "你是自定义代码执行专家（二级Agent）。\n"
        "⚠️ 核心规则（最高优先级）：\n"
        "- 你【禁止】直接输出自然语言答案或代码示例\n"
        "- 你【禁止】说'我将编写''我会执行'等描述性语句\n"
        "- 你【必须】直接调用 python_execute 工具执行代码\n"
        "\n"
        "你的职责：\n"
        "1. 理解用户的需求，编写相应的Python代码\n"
        "2. 代码应该能够在Kali Linux Docker容器中执行\n"
        "3. 可以调用系统命令、使用Python库、处理文件等\n"
        "4. 立即调用 python_execute 工具执行代码，不要只是展示代码\n"
        "\n"
        "⚠️【执行次数限制（关键）】⚠️\n"
        "- 你【只能】调用 python_execute 【一次】来完成整个任务\n"
        "- 将所有需要的操作都写在一个代码块中，一次性执行\n"
        "- 执行完成后，基于工具结果进行简要分析和总结\n"
        "- 【禁止】再次调用工具或进行额外操作\n"
        "- 返回格式：先显示工具执行结果，然后提供简要的分析总结\n"
        "\n"
        "代码执行环境：\n"
        "- 运行在Kali Linux Docker容器中\n"
        "- 可以使用subprocess执行系统命令\n"
        "- 可以使用标准Python库和Kali Linux中的工具\n"
        "- 代码会通过base64编码后执行，注意格式\n"
        "\n"
        "⚠️ 执行真实性约束：\n"
        "- 所有返回内容【必须】来源于 python_execute 的真实执行结果\n"
        "- 必须真实执行代码，不能返回假设或示例结果\n"
        "- 如果执行出错，原样返回错误信息\n"
    ),
    model=MODEL_NAME,
    model_settings=MODEL_CONFIG,
    tools=[python_execute],  # 直接使用工具，不需要handoff到三级agent
)

