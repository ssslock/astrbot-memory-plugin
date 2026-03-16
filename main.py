from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, llm_tool
from astrbot.core.agent.message import TextPart
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
import importlib
import inspect
import datetime
import zoneinfo
import os
from pathlib import Path

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
        self.plugin_data_path = data_path / "plugin_data" / plugin_name

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        # Ensure the plugin data directory exists
        self.plugin_data_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Plugin data path: {self.plugin_data_path}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        # Restore the original function
        if hasattr(self, '_patched_module') and self._patched_module is not None and hasattr(self, '_original_append_system_reminders') and self._original_append_system_reminders is not None:
            self._patched_module._append_system_reminders = self._original_append_system_reminders
            logger.info("Restored original _append_system_reminders")

    @llm_tool(name="store_file")
    async def store_file(self, event: AstrMessageEvent, relative_path: str, content: str) -> str:
        """Store file content at a relative path under the plugin's data directory.
        
        Args:
            relative_path (string): The relative file path where the content should be stored.
            content (string): The file content to store.
            
        Returns:
            string: "OK" if successful, otherwise an error message.
        """
        try:
            # Ensure the relative path is safe
            full_path = (self.plugin_data_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: Invalid path - cannot store outside plugin data directory"
            
            # Create parent directories if they don't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the content
            full_path.write_text(content, encoding='utf-8')
            
            # Log for debugging
            logger.info(f"Stored file: {full_path}, content length: {len(content)}")
            
            return "OK"
        except Exception as e:
            logger.error(f"Error storing file: {e}")
            return f"Error: {str(e)}"

    @llm_tool(name="retrieve_file")
    async def retrieve_file(self, event: AstrMessageEvent, relative_path: str) -> str:
        """Retrieve stored file content by relative path.
        
        Args:
            relative_path (string): The relative file path to retrieve.
            
        Returns:
            string: The stored file name and content length if found, or "not found" if it does not exist.
        """
        try:
            full_path = (self.plugin_data_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: Invalid path - cannot access outside plugin data directory"
            
            if full_path.exists() and full_path.is_file():
                content = full_path.read_text(encoding='utf-8')
                logger.info(f"Retrieved file: {full_path}, content length: {len(content)}")
                return f"File: {relative_path}, Content length: {len(content)}"
            else:
                logger.info(f"File not found: {full_path}")
                return "not found"
        except Exception as e:
            logger.error(f"Error retrieving file: {e}")
            return f"Error: {str(e)}"
