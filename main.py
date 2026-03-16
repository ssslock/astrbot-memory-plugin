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

    @llm_tool(name="store_memory")
    async def store_memory(self, event: AstrMessageEvent, relative_path: str, content: str) -> str:
        """Store memory content with a relative file path
        
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

    @llm_tool(name="retrieve_memory")
    async def retrieve_memory(self, event: AstrMessageEvent, relative_path: str) -> str:
        """Retrieve stored memory content with a relative file path
        
        Args:
            relative_path (string): The relative file path to retrieve.
            
        Returns:
            string: The stored file name and content if found, or "not found" if it does not exist.
        """
        try:
            full_path = (self.plugin_data_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: Invalid path - cannot access outside plugin data directory"
            
            if full_path.exists() and full_path.is_file():
                content = full_path.read_text(encoding='utf-8')
                logger.info(f"Retrieved file: {full_path}, content length: {len(content)}")
                return f"File: {relative_path}, Content: {content}"
            else:
                logger.info(f"File not found: {full_path}")
                return "not found"
        except Exception as e:
            logger.error(f"Error retrieving file: {e}")
            return f"Error: {str(e)}"

    @llm_tool(name="remove_memory")
    async def remove_memory(self, event: AstrMessageEvent, relative_path: str) -> str:
        """Remove memory content with a relative file path
        
        Args:
            relative_path (string): The relative file path to delete.
            
        Returns:
            string: "deleted" if successfully deleted, "not found" if file doesn't exist, or an error message.
        """
        try:
            full_path = (self.plugin_data_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: Invalid path - cannot access outside plugin data directory"
            
            if full_path.exists() and full_path.is_file():
                full_path.unlink()
                logger.info(f"Deleted file: {full_path}")
                return "deleted"
            else:
                logger.info(f"File not found for deletion: {full_path}")
                return "not found"
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return f"Error: {str(e)}"

    @llm_tool(name="list_memory")
    async def list_memory(self, event: AstrMessageEvent, relative_path: str = ".") -> str:
        """List stored memory entries in a directory with a relative path
        
        Args:
            relative_path (string): The relative directory path to list. Defaults to current directory.
            
        Returns:
            string: A formatted list of entries with type (file/folder) and file size for files.
                    Returns "not found" if the directory doesn't exist, or an error message.
        """
        try:
            full_path = (self.plugin_data_path / relative_path).resolve()
            # Ensure the full path is within plugin_data_path
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: Invalid path - cannot access outside plugin data directory"
            
            if not full_path.exists():
                logger.info(f"Directory not found: {full_path}")
                return "not found"
            
            if not full_path.is_dir():
                return "Error: Path is not a directory"
            
            entries = []
            for item in full_path.iterdir():
                if item.is_file():
                    try:
                        size = item.stat().st_size
                        entries.append(f"file: {item.name} ({size} bytes)")
                    except Exception as e:
                        entries.append(f"file: {item.name} (error getting size: {e})")
                elif item.is_dir():
                    entries.append(f"folder: {item.name}")
                else:
                    entries.append(f"other: {item.name}")
            
            if not entries:
                result = "empty directory"
            else:
                result = "\n".join(entries)
            
            logger.info(f"Listed files in: {full_path}, count: {len(entries)}")
            return result
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return f"Error: {str(e)}"

    @llm_tool(name="upload_to_ai_memory")
    async def upload_to_ai_memory(self, event: AstrMessageEvent, relative_path: str) -> str:
        """Upload or Delete a memory entry to the "ai-memory" knowledge base
        
        Before uploading, this tool will delete any existing documents in the knowledge base that have the same path as the memory entry being uploaded.
        To delete a memory entry from the knowledge base, remove the local memory entry first then invoke this tool using the with the same path, the tool will attempt to delete any document with the same path in the knowledge base and return a message suggesting file not found.

        Args:
            relative_path (string): The relative file path to upload. The file must exist in the plugin's data directory.
            
        Returns:
            string: execution details when successful, otherwise an error message.
        """
        try:
            response = ""

            # Get the full path and ensure it's within plugin data directory
            full_path = (self.plugin_data_path / relative_path).resolve()
            if not str(full_path).startswith(str(self.plugin_data_path.resolve())):
                return "Error: Invalid path - cannot access outside plugin data directory"
            
            # Get the knowledge base manager from context
            if not hasattr(self.context, 'kb_manager'):
                return "Error: Knowledge base manager not available"
            
            # Find the "ai-memory" knowledge base
            kb_helper = await self.context.kb_manager.get_kb_by_name("ai-memory")
            if not kb_helper:
                return "Error: 'ai-memory' knowledge base not found. Please ensure it exists and is properly configured."
            
            # First, list all existing documents and delete those with the same name
            try:
                existing_docs = await kb_helper.list_documents()
                deleted_count = 0
                for doc in existing_docs:
                    if doc.doc_name == file_name:
                        await kb_helper.delete_document(doc.doc_id)
                        deleted_count += 1
                        logger.info(f"Deleted existing document with name '{file_name}' (ID: {doc.doc_id})")
                
                if deleted_count > 0:
                    logger.info(f"Deleted {deleted_count} existing document(s) with the same name before upload")
                    response += f"Deleted {deleted_count} existing document(s) with the same name before upload. "
            except Exception as list_error:
                logger.warning(f"Error while listing/deleting existing documents: {list_error}. Continuing with upload...")
            
            # Check if file exists
            if not full_path.exists() or not full_path.is_file():
                response += f"File not found at {relative_path} when attempting to upload."
                return response
            
            # Read file content as bytes
            file_content = full_path.read_bytes()
            file_name = full_path.name
            
            # Determine file type from extension
            file_type = full_path.suffix.lstrip('.').lower()
            if not file_type:
                file_type = "txt"  # Default to text if no extension

            
            # Upload the document
            try:
                doc = await kb_helper.upload_document(
                    file_name=file_name,
                    file_content=file_content,
                    file_type=file_type,
                    chunk_size=1024,  # Default values
                    chunk_overlap=50,
                    batch_size=32,
                    tasks_limit=3,
                    max_retries=3,
                    progress_callback=None,
                    pre_chunked_text=None,
                )
                logger.info(f"Successfully uploaded {file_name} to ai-memory knowledge base. Document ID: {doc.doc_id}")
                return response + f"OK: Uploaded {file_name} to ai-memory knowledge base. Document ID: {doc.doc_id}"
            except Exception as upload_error:
                logger.error(f"Error uploading document: {upload_error}")
                return response + f"Error uploading document: {str(upload_error)}"
                
        except Exception as e:
            logger.error(f"Error in upload_to_ai_memory: {e}")
            return response + f"Error: {str(e)}"
