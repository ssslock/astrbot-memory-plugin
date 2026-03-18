import pytest
import asyncio
import tempfile
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, Mock
import sys

# Add the current directory to sys.path to import main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import MyPlugin


class TestMyPlugin:
    """Test suite for MyPlugin class"""
    
    @pytest.fixture
    def mock_context(self):
        """Mock Context object"""
        context = MagicMock()
        context.get_llm_tool_manager.return_value = MagicMock()
        context.kb_manager = AsyncMock()
        return context
    
    @pytest.fixture
    def mock_event(self):
        """Mock AstrMessageEvent object"""
        event = MagicMock()
        event.message_obj = MagicMock()
        event.message_obj.self_id = "test_bot_123"
        event.plain_result = MagicMock(return_value=MagicMock())
        return event
    
    @pytest.fixture
    def plugin_instance(self, mock_context):
        """Create a plugin instance with temporary directory"""
        # Create temporary directory for plugin data
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock get_astrbot_data_path to return temp directory
            with patch('main.get_astrbot_data_path', return_value=Path(temp_dir)):
                # Create plugin instance
                plugin = MyPlugin(mock_context)
                
                # Set plugin name for testing
                plugin.name = "astrbot-memory-plugin"
                
                yield plugin
    
    @pytest.fixture
    def initialized_plugin(self, plugin_instance):
        """Create and initialize a plugin instance"""
        # Mock logger to prevent actual logging during tests
        with patch('main.logger'):
            # Run initialize
            asyncio.run(plugin_instance.initialize())
            yield plugin_instance
    
    @pytest.mark.asyncio
    async def test_initialization(self, plugin_instance, mock_context):
        """Test plugin initialization"""
        # Mock logger
        with patch('main.logger'):
            # Run initialization
            await plugin_instance.initialize()
            
            # Check that plugin data directory was created
            assert plugin_instance.plugin_data_path.exists()
            assert (plugin_instance.plugin_data_path / "memory").exists()
            assert (plugin_instance.plugin_data_path / "self_prompt").exists()
    
    @pytest.mark.asyncio
    async def test_terminate(self, initialized_plugin):
        """Test plugin termination restores original functions"""
        # Get original function reference
        original_func = initialized_plugin._original_ensure_persona_and_skills
        
        # Mock logger
        with patch('main.logger'):
            # Run terminate
            await initialized_plugin.terminate()
            
            # Check that original function was restored
            assert initialized_plugin._patched_module._ensure_persona_and_skills == original_func
    
    @pytest.mark.asyncio
    async def test_store_memory_success(self, initialized_plugin, mock_event):
        """Test storing memory successfully"""
        relative_path = "test_folder/test_memory.txt"
        content = "This is test memory content"
        
        # Call store_memory
        result = await initialized_plugin.store_memory(
            mock_event, 
            relative_path, 
            content
        )
        
        # Check result
        assert result == "OK"
        
        # Check file was created
        full_path = initialized_plugin.plugin_data_path / "memory" / relative_path
        assert full_path.exists()
        assert full_path.read_text(encoding='utf-8') == content
    
    @pytest.mark.asyncio
    async def test_store_memory_path_traversal(self, initialized_plugin, mock_event):
        """Test storing memory with path traversal attempt"""
        # Try to store outside plugin directory
        relative_path = "../../../evil_path.txt"
        content = "Malicious content"
        
        result = await initialized_plugin.store_memory(
            mock_event, 
            relative_path, 
            content
        )
        
        # Should return error
        assert "Error: Invalid path" in result
    
    @pytest.mark.asyncio
    async def test_retrieve_memory_found(self, initialized_plugin, mock_event):
        """Test retrieving existing memory"""
        # First store a memory
        relative_path = "test_retrieve.txt"
        content = "Content to retrieve"
        
        await initialized_plugin.store_memory(
            mock_event, 
            relative_path, 
            content
        )
        
        # Then retrieve it
        result = await initialized_plugin.retrieve_memory(
            mock_event, 
            relative_path
        )
        
        # Check result contains expected content
        assert "File: test_retrieve.txt" in result
        assert content in result
    
    @pytest.mark.asyncio
    async def test_retrieve_memory_not_found(self, initialized_plugin, mock_event):
        """Test retrieving non-existent memory"""
        result = await initialized_plugin.retrieve_memory(
            mock_event, 
            "non_existent.txt"
        )
        
        assert result == "not found"
    
    @pytest.mark.asyncio
    async def test_remove_memory_success(self, initialized_plugin, mock_event):
        """Test removing memory"""
        # First store a memory
        relative_path = "to_delete.txt"
        content = "Content to delete"
        
        await initialized_plugin.store_memory(
            mock_event, 
            relative_path, 
            content
        )
        
        # Then remove it
        result = await initialized_plugin.remove_memory(
            mock_event, 
            relative_path
        )
        
        assert result == "deleted"
        
        # Verify file is gone
        full_path = initialized_plugin.plugin_data_path / "memory" / relative_path
        assert not full_path.exists()
    
    @pytest.mark.asyncio
    async def test_list_memory_empty(self, initialized_plugin, mock_event):
        """Test listing empty directory"""
        result = await initialized_plugin.list_memory(mock_event, ".")
        
        assert result == "empty directory"
    
    @pytest.mark.asyncio
    async def test_list_memory_with_files(self, initialized_plugin, mock_event):
        """Test listing directory with files"""
        # Create some test files
        test_files = {
            "file1.txt": "Content 1",
            "file2.txt": "Content 2",
            "subdir/": None  # This will create a directory
        }
        
        for path, content in test_files.items():
            if path.endswith('/'):
                # Create directory
                dir_path = initialized_plugin.plugin_data_path / "memory" / path
                dir_path.mkdir(parents=True, exist_ok=True)
            else:
                # Create file
                await initialized_plugin.store_memory(
                    mock_event, 
                    path, 
                    content
                )
        
        # List files
        result = await initialized_plugin.list_memory(mock_event, ".")
        
        # Check all files and directory are listed
        assert "file: file1.txt" in result
        assert "file: file2.txt" in result
        assert "folder: subdir" in result
    
    @pytest.mark.asyncio
    async def test_get_self_prompt_file_path(self, initialized_plugin, mock_event):
        """Test getting self prompt file path"""
        result = await initialized_plugin.get_self_prompt_file_path(mock_event)
        
        assert result == "test_bot_123.md"
    
    @pytest.mark.asyncio
    async def test_get_self_prompt_file_path_no_self_id(self, initialized_plugin):
        """Test getting self prompt file path when self_id is missing"""
        # Create event without self_id
        mock_event = MagicMock()
        mock_event.message_obj = MagicMock()
        mock_event.message_obj.self_id = None
        
        result = await initialized_plugin.get_self_prompt_file_path(mock_event)
        
        assert "Error" in result
    
    @pytest.mark.asyncio
    async def test_upload_to_ai_memory_success(self, initialized_plugin, mock_event, mock_context):
        """Test uploading to AI memory"""
        # Create a test file
        relative_path = "test_upload.txt"
        content = "Test content for upload"
        
        await initialized_plugin.store_memory(
            mock_event, 
            relative_path, 
            content
        )
        
        # Mock kb_manager and kb_helper
        mock_kb_helper = AsyncMock()
        mock_kb_helper.list_documents.return_value = []
        
        doc_mock = MagicMock()
        doc_mock.doc_id = "doc_123"
        mock_kb_helper.upload_document.return_value = doc_mock
        
        mock_context.kb_manager.get_kb_by_name.return_value = mock_kb_helper
        
        # Call upload
        result = await initialized_plugin.upload_to_ai_memory(
            mock_event, 
            relative_path
        )
        
        # Check result
        assert "OK:" in result
        assert "Uploaded test_upload.txt" in result
        
        # Verify upload_document was called
        mock_kb_helper.upload_document.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_upload_to_ai_memory_kb_not_found(self, initialized_plugin, mock_event, mock_context):
        """Test uploading when knowledge base is not found"""
        # Mock kb_manager to return None
        mock_context.kb_manager.get_kb_by_name.return_value = None
        
        result = await initialized_plugin.upload_to_ai_memory(
            mock_event, 
            "test.txt"
        )
        
        assert "Error: 'ai-memory' knowledge base not found" in result
    
    @pytest.mark.asyncio
    async def test_upload_to_ai_memory_file_not_found(self, initialized_plugin, mock_event, mock_context):
        """Test uploading non-existent file"""
        # Mock kb_manager
        mock_kb_helper = AsyncMock()
        mock_context.kb_manager.get_kb_by_name.return_value = mock_kb_helper
        
        result = await initialized_plugin.upload_to_ai_memory(
            mock_event, 
            "non_existent.txt"
        )
        
        assert "File not found" in result
    
    @pytest.mark.asyncio
    async def test_listtools_command(self, initialized_plugin, mock_event):
        """Test listtools command"""
        # Mock tool manager
        mock_tool1 = MagicMock()
        mock_tool1.name = "store_memory"
        mock_tool1.active = True
        
        mock_tool2 = MagicMock()
        mock_tool2.name = "retrieve_memory"
        mock_tool2.active = True
        
        mock_tool3 = MagicMock()
        mock_tool3.name = "inactive_tool"
        mock_tool3.active = False
        
        # Mock get_llm_tool_manager
        mock_tool_manager = MagicMock()
        mock_tool_manager.func_list = [mock_tool1, mock_tool2, mock_tool3]
        initialized_plugin.context.get_llm_tool_manager.return_value = mock_tool_manager
        
        # Call listtools command
        results = []
        async for result in initialized_plugin.listtools(mock_event):
            results.append(result)
        
        # Check that only active tools are listed
        assert len(results) == 1
        result_text = str(results[0])
        assert "store_memory" in result_text
        assert "retrieve_memory" in result_text
        assert "inactive_tool" not in result_text
    
    @pytest.mark.asyncio
    async def test_listtools_no_tools(self, initialized_plugin, mock_event):
        """Test listtools when no tools are available"""
        # Mock empty tool list
        mock_tool_manager = MagicMock()
        mock_tool_manager.func_list = []
        initialized_plugin.context.get_llm_tool_manager.return_value = mock_tool_manager
        
        # Call listtools command
        results = []
        async for result in initialized_plugin.listtools(mock_event):
            results.append(result)
        
        # Should return message about no tools
        assert len(results) == 1
        assert "没有可用的工具" in str(results[0])
    
    @pytest.mark.asyncio
    async def test_patched_ensure_persona_and_skills(self, plugin_instance):
        """Test the monkey-patched function"""
        # Mock the necessary components
        mock_req = MagicMock()
        mock_req.system_prompt = None
        
        mock_cfg = MagicMock()
        mock_plugin_context = MagicMock()
        mock_event = MagicMock()
        mock_event.message_obj = MagicMock()
        mock_event.message_obj.self_id = "test_bot_456"
        
        # Create a self prompt file
        self_prompt_dir = plugin_instance.plugin_data_path / "self_prompt"
        self_prompt_dir.mkdir(parents=True, exist_ok=True)
        self_prompt_file = self_prompt_dir / "test_bot_456.md"
        self_prompt_content = "# Test Self Instructions\n\nThis is a test."
        self_prompt_file.write_text(self_prompt_content, encoding='utf-8')
        
        # Mock original function
        plugin_instance._original_ensure_persona_and_skills = AsyncMock()
        
        # Create and call the patched function
        async def patched_func(req, cfg, plugin_context, event):
            await plugin_instance._original_ensure_persona_and_skills(req, cfg, plugin_context, event)
            
            # Call the patched logic
            try:
                relative_path = plugin_instance._get_self_prompt_file_path(event)
                if relative_path is None:
                    return
                
                full_path = (plugin_instance.plugin_data_path / "self_prompt" / relative_path).resolve()
                if not str(full_path).startswith(str(plugin_instance.plugin_data_path.resolve())):
                    return
                
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    if content:
                        if req.system_prompt is None:
                            req.system_prompt = ""
                        req.system_prompt += f"\n# Self Instructions\n\n{content}\n"
            except Exception as e:
                pass
        
        # Call the patched function
        await patched_func(mock_req, mock_cfg, mock_plugin_context, mock_event)
        
        # Check that self instructions were appended
        assert mock_req.system_prompt is not None
        assert self_prompt_content in mock_req.system_prompt
