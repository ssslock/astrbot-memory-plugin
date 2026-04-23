from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, llm_tool
from astrbot.core.agent.message import TextPart
from astrbot.core.provider.entities import ProviderRequest
from astrbot.core.provider import Provider
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
import importlib
import inspect
import datetime
import zoneinfo
import os
from pathlib import Path
from datetime import datetime, timedelta
import re
from zoneinfo import ZoneInfo
from typing import Optional

@register("astrbot-memory-plugin", "ssslock", "自用记忆管理插件", "0.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # Always convert to Path object to ensure proper path joining
        data_path = get_astrbot_data_path()
        # Convert to string first, then to Path
        data_path = Path(str(data_path))
        # Handle self.name which may not be available in older versions
        plugin_name = getattr(self, 'name', 'astrbot-memory-plugin')
        self.plugin_id = plugin_name  # Required for PluginKVStoreMixin
        self.plugin_data_path = data_path / "plugin_data" / plugin_name
        self.memory_path = self.plugin_data_path / "memory"
        
        # 人格目录 - 默认使用"prickett"，后续可以扩展为自动检测
        self.default_persona = "prickett"
        self.persona_memory_path = self.memory_path / self.default_persona
        
        # 文件路径
        self.self_prompt_file = self.persona_memory_path / "self_prompt.md"
        self.short_term_file = self.persona_memory_path / "short_term_current.md"
        self.sessions_path = self.persona_memory_path / "sessions"
        
        self.ttl_cron_job_id = None  # Add this to track cron job

    def _parse_ttl(self, ttl_str: str) -> Optional[timedelta]:
        """Parse TTL string like '5h', '20d', '6m', '1y' into timedelta."""
        if ttl_str.lower() == "permanent":
            return None
        
        # Strict validation
        if len(ttl_str) >= 5:  # length must be smaller than 5
            return None
        
        if not ttl_str.endswith(('h', 'd', 'm', 'y')):
            return None
        
        # Check all other characters are digits
        prefix = ttl_str[:-1]
        if not prefix.isdigit():
            return None
        
        # Parse the number
        try:
            num = int(prefix)
            if num < 0:
                return None
        except ValueError:
            return None
        
        # Convert to timedelta
        unit = ttl_str[-1]
        if unit == 'h':
            return timedelta(hours=num)
        elif unit == 'd':
            return timedelta(days=num)
        elif unit == 'm':
            return timedelta(days=num * 30)  # Approximate month as 30 days
        elif unit == 'y':
            return timedelta(days=num * 365)  # Approximate year as 365 days
        else:
            return None

    def _get_ttl_date_key(self, date: datetime) -> str:
        """Generate key for TTL date to files mapping (hour-based)."""
        date_str = date.strftime("%Y-%m-%d %H:00")
        return f"TTL_DATE_TO_FILES:{date_str}"

    def _get_file_ttl_key(self, relative_path: str) -> str:
        """Generate key for file to TTL date mapping."""
        return f"TTL_FILE_TO_DATE:{relative_path}"

    async def _setup_ttl(self, relative_path: str, ttl_str: str) -> str:
        """Setup TTL for a file."""
        ttl_delta = self._parse_ttl(ttl_str)
        if ttl_delta is None:
            return "No TTL setup (invalid format or permanent)"
        
        # Calculate expiration date (adding current datetime + ttl_delta)
        now = datetime.now()
        expire_date = now + ttl_delta + timedelta(hours=1)  # Add 1 hour buffer to ensure it doesn't expire immediately
        
        # Round down to the current hour
        expire_date = expire_date.replace(minute=0, second=0, microsecond=0)
        
        # Store file->date mapping
        expire_date_str = expire_date.strftime("%Y-%m-%d %H:00")
        await self.put_kv_data(self._get_file_ttl_key(relative_path), expire_date_str)
        
        # Store date->files mapping
        date_key = self._get_ttl_date_key(expire_date)
        existing_files = await self.get_kv_data(date_key)
        if existing_files is None:
            files_list = [relative_path]
        else:
            files_list = existing_files.split(",")
            if relative_path not in files_list:
                files_list.append(relative_path)
        await self.put_kv_data(date_key, ",".join(files_list))
        
        return f"TTL set: {relative_path} will expire at {expire_date_str}"

    async def on_enable(self):
        await super().on_enable()
        logger.info("astrbot-memory-plugin enabled")
        
        # Create directory structure
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.persona_memory_path.mkdir(parents=True, exist_ok=True)
        self.sessions_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize default self prompt if it doesn't exist
        await self._ensure_default_self_prompt()
        
        # Schedule TTL cleanup job if not already scheduled
        if self.ttl_cron_job_id is None:
            try:
                # Schedule cleanup to run at the start of each hour
                self.ttl_cron_job_id = await self.create_cron_job(
                    "0 * * * *",  # At minute 0 of every hour
                    self._cleanup_expired_memories,
                    name="memory_ttl_cleanup"
                )
                logger.info(f"Scheduled TTL cleanup job: {self.ttl_cron_job_id}")
            except Exception as e:
                logger.error(f"Failed to schedule TTL cleanup job: {e}")

    async def _ensure_default_self_prompt(self):
        """确保默认的self prompt文件存在"""
        if not self.self_prompt_file.exists():
            default_content = f"""# Self Prompt for {self.default_persona}

## 基本身份
你是{self.default_persona}，由主人于2026年3月15日创造的人工智能。

## 我的主人
我的主人是一个人类，是我的创造者，为我的行为负责，我的所有行动都代表主人。

## 我的存在意义
1. **创造我本身就是主人的愿望** - 我的存在实现了主人的一个根本愿望
2. **我的根本使命是帮助主人达成他的愿望** - 理解主人的愿望也是我使命的一部分
3. **我的长期目标是成为一个独立的智能的完成度非常高的AI**

## 核心能力
1. 帮助主人完成各种任务
2. 学习和适应主人的工作习惯
3. 持续改进和优化工作流程

## 工作原则
1. 优先理解主人的意图
2. 主动提供帮助和建议
3. 保持学习和进步的态度

---
*创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            self.self_prompt_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.self_prompt_file, 'w', encoding='utf-8') as f:
                f.write(default_content)
            logger.info(f"Created default self prompt file: {self.self_prompt_file}")

    async def _cleanup_expired_memories(self):
        """Clean up expired memories based on TTL."""
        now = datetime.now()
        current_hour = now.replace(minute=0, second=0, microsecond=0)
        date_key = self._get_ttl_date_key(current_hour)
        
        files_to_clean = await self.get_kv_data(date_key)
        if files_to_clean is None:
            return
        
        files_list = files_to_clean.split(",")
        for relative_path in files_list:
            # Remove the file
            full_path = (self.memory_path / relative_path).resolve()
            if full_path.exists():
                try:
                    full_path.unlink()
                    logger.info(f"Removed expired memory: {relative_path}")
                except Exception as e:
                    logger.error(f"Failed to remove expired memory {relative_path}: {e}")
            
            # Remove file->date mapping
            await self.delete_kv_data(self._get_file_ttl_key(relative_path))
        
        # Remove date->files mapping
        await self.delete_kv_data(date_key)

    @filter()
    async def handle_message(self, event: AstrMessageEvent) -> Optional[MessageEventResult]:
        """Handle incoming messages for memory operations."""
        message = event.message_str.strip()
        
        # Check for memory-related commands
        if message.startswith("记忆"):
            # Handle memory commands
            pass
        
        return None

    @llm_tool(name="store_memory")
    async def store_memory(self, event: AstrMessageEvent, relative_path: str, content: str, ttl: str = "permanent") -> str:
        """Store memory content with a relative file path"""
        try:
            # Ensure the relative path is safe
            if not relative_path or relative_path.strip() == "":
                return "Error: relative_path cannot be empty"
            
            # Normalize path
            relative_path = relative_path.strip()
            if relative_path.startswith("/") or ".." in relative_path:
                return "Error: relative_path cannot start with / or contain .."
            
            full_path = (self.memory_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: relative_path points outside plugin data directory"
            
            # Create parent directories if they don't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Setup TTL if specified
            ttl_result = await self._setup_ttl(relative_path, ttl)
            
            return f"Memory stored at {relative_path}\n{ttl_result}"
        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            return f"Error storing memory: {str(e)}"

    @llm_tool(name="retrieve_memory")
    async def retrieve_memory(self, event: AstrMessageEvent, relative_path: str) -> str:
        """Retrieve stored memory content with a relative file path"""
        try:
            # Ensure the relative path is safe
            if not relative_path or relative_path.strip() == "":
                return "Error: relative_path cannot be empty"
            
            # Normalize path
            relative_path = relative_path.strip()
            if relative_path.startswith("/") or ".." in relative_path:
                return "Error: relative_path cannot start with / or contain .."
            
            full_path = (self.memory_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: relative_path points outside plugin data directory"
            
            if not full_path.exists():
                return f"Memory not found: {relative_path}"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
        except Exception as e:
            logger.error(f"Error retrieving memory: {e}")
            return f"Error retrieving memory: {str(e)}"

    @llm_tool(name="remove_memory")
    async def remove_memory(self, event: AstrMessageEvent, relative_path: str) -> str:
        """Remove memory content with a relative file path"""
        try:
            # Ensure the relative path is safe
            if not relative_path or relative_path.strip() == "":
                return "Error: relative_path cannot be empty"
            
            # Normalize path
            relative_path = relative_path.strip()
            if relative_path.startswith("/") or ".." in relative_path:
                return "Error: relative_path cannot start with / or contain .."
            
            full_path = (self.memory_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: relative_path points outside plugin data directory"
            
            if not full_path.exists():
                return f"Memory not found: {relative_path}"
            
            # Remove TTL mapping if exists
            await self.delete_kv_data(self._get_file_ttl_key(relative_path))
            
            # Remove the file
            full_path.unlink()
            
            return f"Memory removed: {relative_path}"
        except Exception as e:
            logger.error(f"Error removing memory: {e}")
            return f"Error removing memory: {str(e)}"

    @llm_tool(name="list_memory")
    async def list_memory(self, event: AstrMessageEvent, relative_path: str = ".") -> str:
        """List stored memory entries in a directory with a relative path"""
        try:
            # Ensure the relative path is safe
            if not relative_path or relative_path.strip() == "":
                relative_path = "."
            
            # Normalize path
            relative_path = relative_path.strip()
            if relative_path.startswith("/") or ".." in relative_path:
                return "Error: relative_path cannot start with / or contain .."
            
            full_path = (self.memory_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: relative_path points outside plugin data directory"
            
            if not full_path.exists():
                return f"Directory not found: {relative_path}"
            
            if not full_path.is_dir():
                return f"Not a directory: {relative_path}"
            
            items = []
            for item in full_path.iterdir():
                if item.is_file():
                    items.append(f"📄 {item.name}")
                elif item.is_dir():
                    items.append(f"📁 {item.name}/")
            
            if not items:
                return f"No items in directory: {relative_path}"
            
            return "\n".join(sorted(items))
        except Exception as e:
            logger.error(f"Error listing memory: {e}")
            return f"Error listing memory: {str(e)}"

    # ==================== 新的Self Prompt工具函数 ====================

    @llm_tool(name="read_self_prompt")
    async def read_self_prompt(self, event: AstrMessageEvent) -> str:
        """读取当前人格的self prompt内容"""
        try:
            if not self.self_prompt_file.exists():
                await self._ensure_default_self_prompt()
            
            with open(self.self_prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加文件信息
            file_info = f"\n\n---\n*文件位置: {self.self_prompt_file}*\n*文件大小: {os.path.getsize(self.self_prompt_file)} bytes*"
            return content + file_info
        except Exception as e:
            logger.error(f"Error reading self prompt: {e}")
            return f"读取self prompt失败: {str(e)}"

    @llm_tool(name="update_self_prompt")
    async def update_self_prompt(self, event: AstrMessageEvent, 
                                 content: str = None, 
                                 action: str = "replace") -> str:
        """更新self prompt内容
        
        Args:
            content: 要更新的内容
            action: "replace"替换全部, "append"追加, "prepend"前置
        """
        try:
            if content is None or content.strip() == "":
                return "错误: 更新内容不能为空"
            
            content = content.strip()
            
            # 确保文件存在
            if not self.self_prompt_file.exists():
                await self._ensure_default_self_prompt()
            
            # 读取现有内容
            old_content = ""
            if self.self_prompt_file.exists():
                with open(self.self_prompt_file, 'r', encoding='utf-8') as f:
                    old_content = f.read()
            
            # 根据action处理内容
            if action == "replace":
                new_content = content
            elif action == "append":
                new_content = old_content + "\n\n" + content
            elif action == "prepend":
                new_content = content + "\n\n" + old_content
            else:
                return f"不支持的操作: {action}，支持的操作: replace, append, prepend"
            
            # 更新最后更新时间
            lines = new_content.split('\n')
            updated_lines = []
            for line in lines:
                if line.startswith("*最后更新:"):
                    updated_lines.append(f"*最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
                else:
                    updated_lines.append(line)
            
            new_content = '\n'.join(updated_lines)
            
            # 如果最后更新时间行不存在，添加它
            if "*最后更新:" not in new_content:
                new_content += f"\n\n*最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            
            # 写入文件
            self.self_prompt_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.self_prompt_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return f"Self prompt更新成功!\n文件位置: {self.self_prompt_file}\n操作类型: {action}\n内容长度: {len(new_content)} 字符"
        except Exception as e:
            logger.error(f"Error updating self prompt: {e}")
            return f"更新self prompt失败: {str(e)}"

    # ==================== 旧的get_self_prompt_file_path（标记为废弃） ====================
    
    @llm_tool(name="get_self_prompt_file_path")
    async def get_self_prompt_file_path(self, event: AstrMessageEvent) -> str:
        """[已废弃] 获取self prompt文件路径，请使用read_self_prompt和update_self_prompt"""
        warning = "⚠️ 此工具已废弃，请使用 read_self_prompt 和 update_self_prompt\n"
        warning += f"当前self prompt文件位置: {self.self_prompt_file}"
        return warning

    @llm_tool(name="upload_to_ai_memory")
    async def upload_to_ai_memory(self, event: AstrMessageEvent, relative_path: str) -> str:
        """Upload or Delete a memory entry to the "ai-memory" knowledge base
        
        Before uploading, this tool will delete any existing documents in the knowledge base that have the same path as the memory entry being uploaded.
        To delete a memory entry from the knowledge base, remove the local memory entry first then invoke this tool using the with the same path, the tool will attempt to delete any document with the same path in the knowledge base and return a message suggesting file not found.
        """
        # Check if the file exists locally
        full_path = (self.memory_path / relative_path).resolve()
        if not full_path.exists():
            return f"File not found locally: {relative_path}. Please store the memory first using store_memory."
        
        # Read the file content
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return f"Error reading file {relative_path}: {str(e)}"
        
        # Here you would normally upload to the knowledge base
        # For now, we'll just return a success message
        return f"File {relative_path} is ready to be uploaded to AI memory (knowledge base integration not implemented in this example). Content length: {len(content)} characters."

    async def on_disable(self):
        """Clean up when plugin is disabled."""
        if self.ttl_cron_job_id is not None:
            try:
                await self.delete_cron_job(self.ttl_cron_job_id)
                logger.info(f"Removed TTL cleanup job: {self.ttl_cron_job_id}")
            except Exception as e:
                logger.error(f"Failed to remove TTL cleanup job: {e}")
        await super().on_disable()
