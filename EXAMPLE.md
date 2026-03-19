# 使用示例

## 快速开始

1. **配置环境变量**

创建 `.env` 文件：
```env
DOCKER_NAME=kali-container
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o
```

2. **启动Docker容器**

确保你的Kali Linux容器正在运行：
```bash
docker ps | grep kali
```

3. **运行程序**

```bash
python main.py
```

## 使用示例

### 示例1: 端口扫描
```
> 扫描192.168.1.1的开放端口
```

系统会自动：
1. Level 1 Agent 识别为 "scanning" 任务
2. Level 2 Agent 选择 nmap 工具
3. Level 3 Agent 在容器中执行 nmap 命令

### 示例2: Web漏洞扫描
```
> 对http://example.com进行SQL注入测试
```

系统会自动：
1. Level 1 Agent 识别为 "web_exploitation" 任务
2. Level 2 Agent 选择 sqlmap 工具
3. Level 3 Agent 在容器中执行 sqlmap 命令

### 示例3: 信息收集
```
> 收集example.com的子域名信息
```

系统会自动：
1. Level 1 Agent 识别为 "information_collection" 任务
2. Level 2 Agent 选择 amass 或 theharvester 工具
3. Level 3 Agent 在容器中执行相应命令

### 示例4: 自定义代码执行
```
> 写一段Python代码来扫描192.168.1.1的80端口
```

或

```
> 帮我执行Python代码，读取/etc/passwd文件
```

系统会自动：
1. Level 1 Agent 识别为 "custom_code" 任务
2. Level 2 Agent (Custom Code Executor) 直接执行Python代码
3. 代码在Kali Linux容器中运行，返回执行结果

## 工作流程

```
用户输入任务
    ↓
Level 1 Agent (任务分类)
    ↓
Level 2 Agent (选择工具)
    ↓
Level 3 Agent (执行工具)
    ↓
Docker容器执行
    ↓
返回结果
```

## 注意事项

- 所有代码执行都在Docker容器中进行，确保环境隔离
- 确保容器中有相应的渗透测试工具
- API调用需要有效的OpenAI API密钥
- 执行结果会实时流式输出

