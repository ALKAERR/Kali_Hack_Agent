# Kali Code Executor

一个基于三层Agent架构的容器代码执行系统，专门用于在Kali Linux Docker容器中执行渗透测试工具。

## 架构说明

本项目采用三层Agent架构：

1. **Level 1 Agent (任务分类器)**: 将用户任务分类到不同的安全测试领域
2. **Level 2 Agent (领域专家)**: 每个领域有专门的专家Agent，负责选择合适工具
3. **Level 3 Agent (工具执行器)**: 每个工具都有专门的执行Agent，在Docker容器中执行代码

## 功能特性

- ✅ 三层Agent自动路由和执行
- ✅ 支持50+渗透测试工具（nmap, sqlmap, metasploit等）
- ✅ 在Kali Linux Docker容器中安全执行代码
- ✅ 流式输出，实时查看执行过程
- ✅ 支持多种安全测试领域（信息收集、扫描、枚举、Web利用等）

## 安装

1. 克隆项目：
```bash
cd /mnt/data/lzq/Kali_Code_Excuter
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量，创建 `.env` 文件：
```env
DOCKER_NAME=你的kali容器名称
OPENAI_API_KEY=你的API密钥
OPENAI_BASE_URL=你的API地址
MODEL_NAME=gpt-4o
```

## 使用方法

运行主程序：
```bash
python main.py
```

程序启动后会自动开启Web界面，访问 **http://localhost:8000** 即可在浏览器中查看对话历史。

### Web界面功能

- 📊 **实时对话历史展示**：自动更新，无需刷新
- 🔄 **WebSocket实时通信**：新消息自动推送到浏览器
- 📥 **导出对话历史**：支持导出为JSON格式
- 🗑️ **清空历史记录**：一键清空所有对话
- 📈 **统计信息**：显示总对话数和最后更新时间

然后输入你的任务，例如：
- "扫描192.168.1.1的开放端口"
- "对http://example.com进行SQL注入测试"
- "枚举192.168.1.1的SMB共享"
- "写一段Python代码来扫描端口"（自定义代码执行）
- "帮我执行Python代码处理文件"（自定义代码执行）

### 对话历史功能

系统会在同一次运行中保持对话记忆，你可以：
- 连续提问，系统会记住之前的对话内容
- 输入 `history` 或 `历史` 查看对话历史
- 输入 `clear` 或 `清空` 清空对话历史
- 输入 `quit` 或 `exit` 退出程序

**示例：**
```
> 扫描192.168.1.1的开放端口
> 对刚才扫描到的80端口进行Web漏洞扫描
> 用刚才的结果继续深入测试
```

## 项目结构

```
Kali_Code_Excuter/
├── core/
│   ├── docker_executor.py      # Docker执行器
│   ├── tools.py                 # 工具定义（python_execute）
│   ├── level1_agent.py          # 一级Agent（任务分类）
│   ├── level2_agent.py          # 二级Agent（领域专家）
│   ├── level3_agent.py          # 三级Agent（工具执行器）
│   ├── third_agent_factory.py   # 三级Agent工厂
│   └── agent_runner.py          # Agent运行器
├── config/
│   ├── execute_config.py        # 执行配置
│   └── tools_manuals.py         # 工具手册
├── main.py                      # 主入口
├── requirements.txt              # 依赖列表
└── README.md                    # 本文件
```

## 支持的领域

- 信息收集 (Information Collection)
- 扫描与服务发现 (Scanning)
- 枚举 (Enumeration)
- Web利用 (Web Exploitation)
- 漏洞利用 (Exploitation)
- 密码破解 (Password & Crypto)
- 无线攻击 (Wireless Attack)
- 逆向工程 (Reverse Engineering)
- 数字取证 (Forensics)
- 后渗透 (Post-Exploitation)
- **自定义代码执行 (Custom Code)** - 新增：可以自由编写和执行Python代码

## 注意事项

1. 确保Docker容器正在运行且可访问
2. 确保容器名称与 `.env` 中的 `DOCKER_NAME` 一致
3. 需要有效的OpenAI API密钥和地址
4. 所有代码执行都在隔离的Docker容器中进行

## 许可证

MIT License

