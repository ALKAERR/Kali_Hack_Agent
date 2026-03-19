"""Docker executor for running code in Kali Linux container."""

import docker
import base64


class KaliDockerExecutor:
    """只负责在 Docker 里跑代码，不负责 Session 管理"""
    
    def __init__(self, container_name: str):
        self.client = docker.from_env()
        try:
            self.container = self.client.containers.get(container_name)
        except Exception as e:
            print(f"❌ 找不到 Docker 容器: {container_name}")
            self.container = None

    def execute(self, code: str) -> str:
        if not self.container:
            return "❌ 错误: 无法连接到 Kali Docker 环境"

        try:
            # Base64 编码防止 Shell 注入和换行符问题
            b64_code = base64.b64encode(code.encode('utf-8')).decode('ascii')
            cmd = f'/bin/bash -c "echo {b64_code} | base64 -d | python3"'
            
            result = self.container.exec_run(cmd, demux=False)
            output = result.output.decode('utf-8', errors='ignore')
            
            if result.exit_code != 0:
                return f"❌ [Runtime Error] Exit Code {result.exit_code}:\n{output}"
            return f"{output}"
            
        except Exception as e:
            return f"❌ [System Error]: {str(e)}"

