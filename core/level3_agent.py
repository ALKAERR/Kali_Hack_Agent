"""Level 3 Agents: Tool Executors."""

from core.third_agent_factory import build_tool_executor

"""
三级 Agent：工具执行层
- 每个工具一个 Executor Agent
- 统一由 build_tool_executor 构建
"""

# =========================
# 1️⃣ 工具清单（唯一事实源）
# =========================

TOOL_NAMES = [
    # --- 信息收集 / OSINT ---
    "amass",
    "theharvester",
    "recon-ng",
    "spiderfoot",
    "fierce",
    "dnsenum",
    "nbtscan",
    "arp-scan",
    "kismet",
    "wafw00f",
    
    # --- 扫描与服务发现 ---
    "nmap",
    "masscan",
    "tcpdump",
    "tshark",
    "wireshark",
    "httpx",
    "curl",
    
    # --- 枚举 ---
    "enum4linux",
    "rpcclient",
    "smbmap",
    "dirb",
    "gobuster",
    "ffuf",
    "wfuzz",
    "nikto",
    "wpscan",
    "nxc",
    
    # --- Web ---
    "burpsuite",
    "sqlmap",
    
    # --- 利用 / 初始控制 ---
    "msfconsole",
    "msfvenom",
    "searchsploit",
    "evil-winrm",
    "hydra",
    "medusa",
    "patator",
    "responder",
    
    # --- 密码 / Crypto ---
    "hashcat",
    "john",
    "ophcrack",
    "hash-identifier",
    
    # --- 无线 ---
    "airmon-ng",
    "airodump-ng",
    "aireplay-ng",
    "aircrack-ng",
    
    # --- 逆向 ---
    "angr",
    "radare2",
    "objdump",
    "checksec",
    "strings",
    "file",
    "xxd",
    
    # --- 取证 ---
    "autopsy",
    "binwalk",
    "exiftool",
    "photorec",
    "testdisk",
    "scalpel",
]

tool_executors = {
    tool_name: build_tool_executor(tool_name)
    for tool_name in TOOL_NAMES
}

