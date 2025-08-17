import os
import json
from typing import Optional, Dict, Any, Union
from openai import OpenAI
from rich.console import Console


class AIConfig:
    """AI 配置管理器，负责配置的加载、验证和管理"""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 model: str = "gpt-5-nano",
                 timeout: Optional[Union[int, float, str]] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url
        self.model = model
        self.timeout = self._convert_timeout(timeout)
        
    def _convert_timeout(self, timeout: Optional[Union[int, float, str]]) -> Optional[float]:
        """
        1. 将不同类型的超时时间参数转换为统一的浮点数格式；
        2. 用于 OpenAI API 客户端的超时设置。

        Args:
            timeout: 可以是 int、float 或 str 类型的超时时间值
        Returns:
            Optional[float]: 转换后的超时时间，或 None 如果未设置
        
        """
        if timeout is None:
            return None
        
        try:
            if isinstance(timeout, str):
                timeout_converted = float(timeout.strip())
            else:
                timeout_converted = float(timeout)
            
            if timeout_converted <= 0:
                raise ValueError("timeout 必须为正数")
            
            return timeout_converted
        except ValueError as e:
            raise ValueError(f"无效的 timeout 值：{timeout} ({e})") from e
    
    def validate(self) -> tuple[bool, str]:
        """
        验证配置的有效性

        Args:
            None
        Returns:
            tuple[bool, str]: 验证结果和消息

        """
        if not self.api_key:
            return False, "未找到 API 密钥"
        
        if self.base_url and not self.base_url.startswith(('http://', 'https://')):
            return False, f"无效的 base_url 格式：{self.base_url}"
        
        return True, ""
    
    def to_client_kwargs(self) -> Dict[str, Any]:
        """
        将 AIConfig 对象的配置参数转换为 OpenAI 客户端构造函数所需的关键字参数字典
        """
        kwargs: Dict[str, Any] = {'api_key': self.api_key}
        
        if self.base_url:
            kwargs['base_url'] = self.base_url
        
        if self.timeout is not None:
            kwargs['timeout'] = self.timeout
        
        return kwargs
    
    @classmethod
    def from_config_file(cls, config_file: str = "config.json") -> 'AIConfig':
        """从配置文件创建配置对象"""
        config = {}
        
        # 尝试加载配置文件
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception:
                pass  # 使用默认配置
        
        ai_config = config.get('ai', {})
        
        return cls(
            api_key=ai_config.get('api_key'),
            base_url=ai_config.get('base_url'),
            model=ai_config.get('model', 'gpt-5-nano'),
            timeout=ai_config.get('timeout')
        )


class PromptBuilder:
    """提示词构建器，负责构建 AI 摘要的提示词"""
    
    @staticmethod
    def build_summary_prompt(title: str, content: str, max_content_length: int = 2000) -> str:
        """
        构建用于 AI 摘要的提示词
        
        Args:
            title: 文章标题
            content: 文章内容
            max_content_length: 最大内容长度
            
        Returns:
            格式化的提示词
        """
        # 限制内容长度，避免超出 token 限制
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        
        return f"""
                请为以下文章生成一个简洁的中文摘要（200-400 字）：

                标题：{title}

                内容：
                {content}

                要求：
                1. 摘要应该概括文章的主要内容和关键信息
                2. 使用简洁、通俗易懂的中文
                3. 长度控制在 200-300 字之间
                4. 突出文章的核心观点或重要信息
                5. 不要包含"本文"、"文章"等自指性词汇
                6. 使用列表或段落格式清晰表达

                摘要：
              """


class SummaryValidator:
    """摘要验证器，负责验证生成的摘要质量"""
    
    @staticmethod
    def is_valid(summary: str, min_length: int = 20) -> bool:
        """
        验证摘要质量
        
        Args:
            summary: 生成的摘要
            min_length: 最小长度要求
            
        Returns:
            是否为有效摘要
        """
        if not summary or not summary.strip():
            return False
        
        # 检查长度
        if len(summary.strip()) < min_length:
            return False
        
        # 检查是否包含常见的错误响应
        invalid_phrases = [
            "抱歉", "无法", "不能", "错误", "失败", 
            "sorry", "error", "无法生成", "内容不足"
        ]
        
        summary_lower = summary.lower()
        for phrase in invalid_phrases:
            if phrase in summary_lower:
                return False
        
        return True


class ErrorHandler:
    """错误处理器，负责统一处理和格式化错误信息"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def handle_api_error(self, error: Exception) -> None:
        """
        处理 API 相关错误

        Args:
            error: 引发的异常对象
        Returns:
            None
        """

        error_msg = str(error)
        
        if "401" in error_msg or "invalid_api_key" in error_msg.lower():
            self.console.print("[red]❌ AI 摘要生成失败：API 密钥无效，请检查您的 API 密钥是否正确 [/red]")
        elif "403" in error_msg or "insufficient_quota" in error_msg.lower():
            self.console.print("[red]❌ AI 摘要生成失败：API 配额不足，请检查您的账户余额 [/red]")
        elif "429" in error_msg or "rate_limit" in error_msg.lower():
            self.console.print("[yellow]⚠️  AI 摘要生成失败：请求过于频繁，请稍后重试 [/yellow]")
        elif "connection" in error_msg.lower() or "network" in error_msg.lower():
            self.console.print("[yellow]⚠️  AI 摘要生成失败：网络连接问题，请检查网络设置 [/yellow]")
        else:
            self.console.print(f"[red]❌ AI 摘要生成失败：{error}[/red]")


class AISummarizer:
    """AI 文章摘要生成器，主类"""
    
    def __init__(self, config: AIConfig):
        """
        初始化 AI 摘要生成器
        
        Args:
            config: AI 配置对象
        """

        self.console = Console()
        self.config = config
        self.error_handler = ErrorHandler(self.console)
        self.prompt_builder = PromptBuilder()
        self.validator = SummaryValidator()
        
        # 验证配置并初始化客户端
        self.enabled = self._initialize_client()
    
    def _initialize_client(self) -> bool:
        """
        初始化 OpenAI 客户端

        Args:
            None

        Returns:
            bool: 是否成功初始化客户端
        """


        # 验证配置
        is_valid, error_msg = self.config.validate()

        # 配置无效，打印错误信息
        if not is_valid:
            self.console.print(f"[yellow]⚠️  {error_msg}。请检查配置文件或环境变量 [/yellow]")
            return False
        
        # 创建客户端
        try:
            # 把配置转换为 OpenAI 客户端所需的关键字参数
            client_kwargs = self.config.to_client_kwargs()
            self.client = OpenAI(**client_kwargs)

            self.console.print("[green]✅ AI 摘要服务已启用 [/green]")
            return True
        except Exception as e:
            self.console.print(f"[red]❌ AI 摘要服务初始化失败：{e}[/red]")
            return False
    
    def generate_summary(self, title: str, content: str) -> Optional[str]:
        """
        为文章生成 AI 摘要
        
        Args:
            title: 文章标题
            content: 文章内容
            
        Returns:
            AI 生成的摘要，如果失败则返回 None
        """

        if not self.enabled:
            return None
        
        if not content or not content.strip():
            return None
        
        try:
            return self._call_api(title, content)
        except Exception as e:
            self.error_handler.handle_api_error(e)
            return None
    
    def _call_api(self, title: str, content: str) -> Optional[str]:
        """
        调用 OpenAI API 生成摘要

        Args:
            title: 文章标题
            content: 文章内容

        Returns:
            Optional[str]: 生成的摘要，如果失败则返回 None
        """

        # 构建提示词
        prompt = self.prompt_builder.build_summary_prompt(title, content)
        
        # 调用 API
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的文章摘要助手。请为用户提供的文章生成简洁、准确的中文摘要。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )
        
        summary = response.choices[0].message.content
        if not summary:
            self.console.print("[yellow]⚠️  API 返回空摘要，跳过此次摘要 [/yellow]")
            return None
        
        summary = summary.strip()
        
        # 验证摘要质量
        if self.validator.is_valid(summary):
            return summary
        else:
            self.console.print("[yellow]⚠️  生成的摘要质量不佳，跳过此次摘要 [/yellow]")
            return None
    
    def is_enabled(self) -> bool:
        """检查 AI 摘要服务是否可用"""
        return self.enabled


def create_ai_summarizer_from_config(config_file: str = "config.json") -> AISummarizer:
    """
    从配置文件创建 AI 摘要器
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        AI 摘要器实例
    """
    config = AIConfig.from_config_file(config_file)
    return AISummarizer(config)


# 为了保持向后兼容，提供原始构造函数接口
def create_ai_summarizer(api_key: Optional[str] = None,
                        base_url: Optional[str] = None,
                        model: str = "gpt-5-nano",
                        timeout: Optional[Union[int, float, str]] = None) -> AISummarizer:
    """
    直接创建 AI 摘要器（向后兼容接口）
    
    Args:
        api_key: API 密钥
        base_url: API 基础 URL
        model: 使用的模型名称
        timeout: 请求超时时间
        
    Returns:
        AI 摘要器实例
    """
    config = AIConfig(api_key=api_key, base_url=base_url, model=model, timeout=timeout)
    return AISummarizer(config)