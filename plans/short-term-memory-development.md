# 短期记忆功能开发计划

## 项目概述

基于记忆插件现有架构，开发类似self prompt的短期记忆功能，采用自主维护模式。

## 当前架构分析

### 现有self prompt实现
1. **路径管理**：`self.self_prompt_path = self.memory_path / "self_prompt"`
2. **文件命名**：`{self_id}.md` 格式
3. **工具函数**：`get_self_prompt_file_path()` 返回文件路径
4. **存储位置**：`plugin_data/astrbot-memory-plugin/memory/self_prompt/`

### 插件结构
- 主类：`MyPlugin(Star)`
- 工具装饰器：`@llm_tool`
- 事件处理：`AstrMessageEvent`
- 数据存储：`plugin_data` 目录

## 开发目标

### 核心功能
1. **短期记忆文件管理**：类似self prompt的文件创建、读取、更新
2. **简化更新接口**：主人指导，莉莉执行的更新命令
3. **智能建议功能**：基于对话历史建议更新内容
4. **渐进式自动化**：为本地LLM自动化归档奠定基础

### 非功能目标
1. **与现有架构兼容**：复用self prompt的基础设施
2. **简单易用**：更新操作直观简单
3. **可扩展性**：支持未来功能扩展

## 技术方案

### 1. 文件结构设计
```
plugin_data/astrbot-memory-plugin/memory/
├── self_prompt/
│   └── {self_id}.md
└── short_term/
    ├── current.md          # 当前工作会话
    ├── sessions/           # 历史会话归档
    │   ├── 2026-04-23_10-29_记忆系统开发.md
    │   └── ...
    └── templates/          # 记忆模板
        └── default.md
```

### 2. 数据格式
采用Markdown格式，类似self prompt但更结构化：
```markdown
# 短期记忆 - 工作上下文

## 元数据
- **会话ID**: 2026-04-23_10-29_记忆系统开发
- **开始时间**: 2026-04-23T10:29:00+08:00
- **最后更新**: 2026-04-23T10:35:00+08:00
- **更新者**: 莉莉

## 当前状态
- **工作仓库**: astrbot-memory-plugin
- **当前分支**: feat/docs-memory-system-improvements
- **工作模式**: 需求分析与开发计划

## 任务目标
1. 开发短期记忆功能
2. 设计类似self prompt的自主维护模式
3. 制定详细开发计划

## 工作进度
✅ 已完成:
- 分析了现有self prompt实现
- 确定了短期记忆设计思路

🔄 进行中:
- 制定开发计划
- 设计技术方案

⏳ 待完成:
- 实现基础文件管理
- 开发更新工具函数

## 关键决策
1. 采用类似self prompt的自主维护模式
2. 主人指导，莉莉执行的协作方式
3. 渐进式自动化路线

## 待办事项
- [ ] 设计短期记忆文件格式
- [ ] 实现基础CRUD操作
- [ ] 开发简化更新接口
```

### 3. 工具函数设计

#### 核心工具函数
```python
@llm_tool(name="get_short_term_memory")
async def get_short_term_memory(self, event: AstrMessageEvent) -> str:
    """获取当前短期记忆内容"""
    
@llm_tool(name="update_short_term_memory")
async def update_short_term_memory(self, event: AstrMessageEvent, 
                                   section: str, content: str, 
                                   action: str = "replace") -> str:
    """更新短期记忆的特定部分"""
    # action: "replace", "append", "remove", "clear"
    
@llm_tool(name="suggest_short_term_update")
async def suggest_short_term_update(self, event: AstrMessageEvent) -> str:
    """基于对话历史建议短期记忆更新"""
    
@llm_tool(name="archive_short_term_session")
async def archive_short_term_session(self, event: AstrMessageEvent, 
                                     session_name: str = None) -> str:
    """归档当前短期记忆会话"""
```

#### 辅助函数
```python
def _get_short_term_path(self) -> Path:
    """获取短期记忆文件路径"""
    
def _parse_short_term_content(self, content: str) -> dict:
    """解析短期记忆Markdown内容"""
    
def _format_short_term_update(self, section: str, content: str, 
                              action: str) -> str:
    """格式化更新内容"""
    
def _analyze_conversation_for_updates(self, recent_messages: list) -> dict:
    """分析对话历史，提取可能的更新"""
```

## 开发阶段

### 阶段1：基础框架（第1天）
**目标**：建立短期记忆文件系统基础
- [ ] 创建短期记忆目录结构
- [ ] 实现基础文件读写函数
- [ ] 设计Markdown模板格式
- [ ] 添加配置管理

### 阶段2：核心工具函数（第2-3天）
**目标**：实现主要工具函数
- [ ] `get_short_term_memory()` - 读取功能
- [ ] `update_short_term_memory()` - 更新功能
- [ ] 基础section管理（替换、追加、删除）
- [ ] 错误处理和验证

### 阶段3：智能功能（第4-5天）
**目标**：添加智能建议和自动化功能
- [ ] `suggest_short_term_update()` - 建议功能
- [ ] 对话历史分析
- [ ] 模式识别基础
- [ ] `archive_short_term_session()` - 归档功能

### 阶段4：集成优化（第6-7天）
**目标**：完善用户体验和集成
- [ ] 与self prompt的协同
- [ ] 文件访问优化集成
- [ ] 性能优化和测试
- [ ] 文档和示例

## 具体实施步骤

### 第1步：修改插件初始化
```python
def __init__(self, context: Context):
    super().__init__(context)
    # 现有代码...
    self.short_term_path = self.memory_path / "short_term"
    self.current_memory_file = self.short_term_path / "current.md"
    self.sessions_path = self.short_term_path / "sessions"
    self.templates_path = self.short_term_path / "templates"
```

### 第2步：创建目录结构
```python
async def on_enable(self):
    await super().on_enable()
    # 现有代码...
    # 创建短期记忆目录
    self.short_term_path.mkdir(parents=True, exist_ok=True)
    self.sessions_path.mkdir(parents=True, exist_ok=True)
    self.templates_path.mkdir(parents=True, exist_ok=True)
    
    # 初始化当前记忆文件
    if not self.current_memory_file.exists():
        self._init_short_term_memory()
```

### 第3步：实现基础工具函数
参考现有`store_memory`/`retrieve_memory`的实现模式，但针对短期记忆优化。

### 第4步：添加智能建议功能
基于对话历史分析，提取关键信息建议更新。

## 与现有系统的集成点

### 1. 复用self prompt基础设施
- 相同的路径管理机制
- 类似的工具函数装饰器
- 一致的事件处理模式

### 2. 与记忆系统协同
- 短期记忆可作为长期记忆的输入源
- 支持短期记忆内容归档到长期存储
- 共享配置和管理界面

### 3. 与开发系统集成
- 自动检测工作仓库并更新短期记忆
- 与prickett.md自动注入协同
- 支持skill上下文管理

## 测试计划

### 单元测试
1. 文件读写功能测试
2. Markdown解析测试
3. 更新操作测试
4. 错误处理测试

### 集成测试
1. 与self prompt的兼容性测试
2. 工具函数调用测试
3. 实际工作流测试

### 用户验收测试
1. 主人指导更新测试
2. 智能建议功能测试
3. 归档和恢复测试

## 风险与缓解

### 技术风险
1. **Markdown解析复杂性**
   - 缓解：使用简单正则表达式，避免复杂解析
   
2. **并发访问冲突**
   - 缓解：使用文件锁或原子操作
   
3. **性能影响**
   - 缓解：缓存机制，异步处理

### 业务风险
1. **用户体验不佳**
   - 缓解：渐进式开发，持续收集反馈
   
2. **功能过于复杂**
   - 缓解：保持核心功能简单，逐步扩展

## 成功标准

### 功能标准
- [ ] 莉莉能够根据主人指令更新短期记忆
- [ ] 短期记忆文件格式清晰易读
- [ ] 支持基本的增删改查操作
- [ ] 智能建议功能可用

### 性能标准
- [ ] 读取延迟 < 100ms
- [ ] 更新延迟 < 200ms
- [ ] 内存占用 < 10MB

### 用户体验标准
- [ ] 主人觉得更新操作简单直观
- [ ] 莉莉能够准确执行更新指令
- [ ] 短期记忆内容对工作有帮助

## 后续扩展

### 短期扩展（1个月内）
1. 更智能的更新建议
2. 多会话管理
3. 搜索和检索功能

### 中期扩展（3个月内）
1. 本地LLM自动化归档
2. 跨会话知识关联
3. 工作模式学习

### 长期扩展（6个月内）
1. 完全自动化维护
2. 智能工作流优化
3. 与其他AI系统集成

---

*创建时间：2026-04-23 10:29*
*最后更新：2026-04-23 10:35*
*状态：进行中*

## 紧急修复：self prompt文件路径问题

### 问题描述
当前self prompt使用`event.message_obj.self_id`作为文件名，但实际应该使用人格名称。从日志可见：
```
Self prompt file /home/ssslock/astrbot/data/plugin_data/astrbot-memory-plugin/memory/self_prompt/astrbot_prickett_bot.md does not exist
```

### 根本原因
1. `self_id`可能是会话ID或平台特定的标识符，不是人格名称
2. 人格名称应该从context的persona_manager获取

### 解决方案
根据`/home/ssslock/repos/_prickett/AstrBot/astrbot/core/star/context.py`的分析：

#### 1. 获取当前人格的方法
```python
# 从context获取persona_manager
persona_manager = self.context.persona_manager

# 获取当前会话的人格
# 需要event.session作为umo参数
persona = await persona_manager.resolve_selected_persona(
    umo=event.session,
    conversation_persona_id=None,
    platform_name=event.get_platform_name(),
    provider_settings=None
)

# persona[0]是persona_id, persona[1]是persona对象
persona_id = persona[0]  # 如"prickett"
persona_obj = persona[1]  # Personality对象
```

#### 2. 修改_get_self_prompt_file_path方法
```python
def _get_self_prompt_file_path(self, event: AstrMessageEvent) -> str:
    """获取self prompt文件路径，基于人格名称而不是self_id"""
    try:
        # 方法1：尝试从persona_manager获取当前人格
        persona_manager = self.context.persona_manager
        
        # 获取当前会话的人格信息
        persona_info = await persona_manager.resolve_selected_persona(
            umo=event.session,
            conversation_persona_id=None,
            platform_name=event.get_platform_name(),
            provider_settings=None
        )
        
        persona_id = persona_info[0]
        if persona_id:
            file_path = f"{persona_id}.md"
            return file_path
        
        # 方法2：回退到默认人格
        default_persona = await persona_manager.get_default_persona_v3(event.session)
        if default_persona and hasattr(default_persona, 'name'):
            file_path = f"{default_persona.name}.md"
            return file_path
        
        # 方法3：最终回退到self_id
        self_id = getattr(event.message_obj, 'self_id', None)
        if self_id:
            logger.warning(f"Using self_id as fallback for persona: {self_id}")
            return f"{self_id}.md"
            
        return None
        
    except Exception as e:
        logger.error(f"Error getting persona for self prompt: {e}")
        # 回退到原来的self_id逻辑
        try:
            self_id = event.message_obj.self_id
            if self_id:
                return f"{self_id}.md"
        except:
            pass
        return None
```

#### 3. 创建默认self prompt文件
如果文件不存在，应该创建默认内容：
```python
async def ensure_self_prompt_file(self, event: AstrMessageEvent):
    """确保self prompt文件存在，如果不存在则创建默认内容"""
    file_path = self._get_self_prompt_file_path(event)
    if not file_path:
        return False
    
    full_path = self.self_prompt_path / file_path
    if not full_path.exists():
        # 获取人格名称用于默认内容
        persona_name = file_path.replace('.md', '')
        
        default_content = f"""# Self Prompt for {persona_name}

## 基本身份
你是{persona_name}，一个AI助手。

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
"""
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(default_content)
        logger.info(f"Created default self prompt file: {full_path}")
    
    return True
```

### 实施步骤

#### 步骤1：修改现有代码
1. 更新`_get_self_prompt_file_path`方法，使用人格名称
2. 添加`ensure_self_prompt_file`方法，确保文件存在
3. 在`on_enable`或首次调用时创建默认文件

#### 步骤2：测试验证
1. 验证人格名称正确获取
2. 测试文件创建功能
3. 验证回退机制

#### 步骤3：更新文档
1. 说明self prompt现在基于人格名称
2. 提供文件位置和命名规则
3. 添加使用示例

### 对短期记忆开发的影响

#### 正面影响
1. **统一命名规则**：短期记忆也可以使用人格名称作为基础
2. **更好的上下文**：知道当前人格有助于个性化短期记忆
3. **一致性**：self prompt和短期记忆使用相同的身份标识

#### 调整短期记忆文件命名
```python
# 原计划：current.md
# 新方案：{persona_name}_current.md 或 {persona_name}/current.md

# 示例：
# prickett_current.md 或 prickett/current.md
```

#### 人格感知的短期记忆
短期记忆可以包含人格特定信息：
```markdown
# 短期记忆 - {persona_name}的工作上下文

## 人格信息
- **名称**: {persona_name}
- **角色**: {persona_role}
- **工作风格**: {从self prompt中提取}

## 当前工作状态
...
```

### 时间安排
这个修复应该**优先于**短期记忆开发，因为：
1. 是现有功能的严重bug
2. 影响短期记忆的基础设计
3. 相对简单，可以快速完成

**预计时间**：1-2小时

### 测试计划
1. 单元测试：验证人格名称获取逻辑
2. 集成测试：测试文件创建和读取
3. 回归测试：确保现有功能不受影响

### 风险控制
1. **回退机制**：保留self_id作为回退，确保不崩溃
2. **日志记录**：详细记录人格获取过程，便于调试
3. **兼容性**：确保与现有self prompt文件兼容

---

*添加于2026-04-23 10:37，紧急修复self prompt问题*

## 文件路径结构调整方案

### 当前问题分析
1. **路径混乱**：self_prompt目录下按人格分文件，但实际只有一个人格在使用
2. **工具冗余**：`get_self_prompt_file_path`工具只是返回路径，实际用处有限
3. **使用不便**：需要先获取路径再操作，步骤繁琐

### 新方案设计

#### 1. 文件结构重组
```
plugin_data/astrbot-memory-plugin/memory/
├── prickett/                    # 人格专属目录
│   ├── self_prompt.md          # self prompt文件
│   ├── short_term_current.md   # 当前短期记忆
│   └── sessions/               # 历史会话归档
│       ├── 2026-04-23_10-29_记忆系统开发.md
│       └── ...
├── other_persona/              # 其他人格（如有）
│   ├── self_prompt.md
│   └── ...
└── shared/                     # 共享记忆（可选）
    └── common_knowledge.md
```

#### 2. 工具函数简化
**移除**：`get_self_prompt_file_path` - 返回路径的工具用处有限
**新增**：
- `read_self_prompt()` - 直接读取self prompt内容
- `update_self_prompt()` - 直接更新self prompt
- `read_short_term_memory()` - 读取短期记忆
- `update_short_term_memory()` - 更新短期记忆

#### 3. 路径解析逻辑
```python
def _get_persona_directory(self, persona_name: str = None) -> Path:
    """获取人格目录路径"""
    if persona_name is None:
        # 自动检测当前人格
        persona_name = self._get_current_persona_name()
    
    persona_dir = self.memory_path / persona_name
    persona_dir.mkdir(parents=True, exist_ok=True)
    return persona_dir

def _get_self_prompt_path(self, persona_name: str = None) -> Path:
    """获取self prompt文件路径"""
    persona_dir = self._get_persona_directory(persona_name)
    return persona_dir / "self_prompt.md"

def _get_short_term_path(self, persona_name: str = None) -> Path:
    """获取短期记忆文件路径"""
    persona_dir = self._get_persona_directory(persona_name)
    return persona_dir / "short_term_current.md"
```

### 工具函数设计

#### 1. Self Prompt工具
```python
@llm_tool(name="read_self_prompt")
async def read_self_prompt(self, event: AstrMessageEvent) -> str:
    """读取当前人格的self prompt内容"""
    try:
        file_path = self._get_self_prompt_path()
        if not file_path.exists():
            return f"Self prompt文件不存在: {file_path}\n请使用update_self_prompt创建。"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
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
        file_path = self._get_self_prompt_path()
        
        if action == "replace":
            new_content = content
        elif action == "append":
            old_content = ""
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    old_content = f.read()
            new_content = old_content + "\n" + content
        elif action == "prepend":
            old_content = ""
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    old_content = f.read()
            new_content = content + "\n" + old_content
        else:
            return f"不支持的操作: {action}"
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return f"Self prompt更新成功: {file_path}"
    except Exception as e:
        return f"更新self prompt失败: {str(e)}"
```

#### 2. 短期记忆工具
```python
@llm_tool(name="read_short_term_memory")
async def read_short_term_memory(self, event: AstrMessageEvent) -> str:
    """读取当前短期记忆内容"""
    try:
        file_path = self._get_short_term_path()
        if not file_path.exists():
            return "短期记忆文件不存在，请先创建或更新。"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"读取短期记忆失败: {str(e)}"

@llm_tool(name="update_short_term_memory")
async def update_short_term_memory(self, event: AstrMessageEvent,
                                   section: str = None,
                                   content: str = None,
                                   action: str = "replace") -> str:
    """更新短期记忆
    
    Args:
        section: 要更新的章节，如"任务目标"、"工作进度"
        content: 更新内容
        action: "replace"替换, "append"追加, "remove"删除
    """
    # 实现章节级别的智能更新
    pass
```

### 实施步骤

#### 阶段1：重构文件结构（第1天）
1. **修改初始化代码**：
   ```python
   def __init__(self, context: Context):
       super().__init__(context)
       # 现有代码...
       self.persona_memory_path = self.memory_path / "prickett"  # 默认人格
   ```

2. **创建目录结构**：
   ```python
   async def on_enable(self):
       await super().on_enable()
       # 创建人格目录
       self.persona_memory_path.mkdir(parents=True, exist_ok=True)
       (self.persona_memory_path / "sessions").mkdir(exist_ok=True)
   ```

3. **迁移现有文件**（如有）：
   - 将`self_prompt/astrbot_prickett_bot.md`移动到`prickett/self_prompt.md`
   - 更新相关引用

#### 阶段2：实现新工具函数（第2天）
1. **实现`read_self_prompt`和`update_self_prompt`**
2. **实现`read_short_term_memory`和`update_short_term_memory`**
3. **移除`get_self_prompt_file_path`工具**
4. **更新测试用例**

#### 阶段3：智能更新功能（第3天）
1. **实现章节解析**：解析Markdown的章节结构
2. **智能合并**：支持章节级别的增删改
3. **格式保持**：保持Markdown格式的完整性

### 优势分析

#### 1. 使用更简单
**之前**：
```python
# 需要两步
path = await get_self_prompt_file_path()
# 然后手动读取/写入文件
```

**之后**：
```python
# 一步完成
content = await read_self_prompt()
await update_self_prompt(content="新内容", action="append")
```

#### 2. 结构更清晰
- 每个人格有自己的目录
- 相关文件组织在一起
- 易于备份和迁移

#### 3. 扩展性更好
- 容易添加新的人格
- 支持人格特定的配置
- 便于实现人格切换功能

#### 4. 减少错误
- 直接操作内容，不需要处理文件路径
- 内置错误处理和验证
- 统一的接口设计

### 兼容性考虑

#### 向后兼容
1. **逐步迁移**：先添加新工具，再标记旧工具为废弃
2. **数据迁移**：提供迁移脚本或自动迁移
3. **文档更新**：更新使用文档和示例

#### 向前兼容
1. **灵活的人格检测**：支持自动检测和手动指定人格
2. **可配置的路径**：允许通过配置调整目录结构
3. **扩展接口**：为未来功能预留接口

### 测试策略

#### 单元测试
1. 路径解析函数测试
2. 文件读写操作测试
3. 章节解析逻辑测试

#### 集成测试
1. 工具函数调用测试
2. 实际工作流测试
3. 错误处理测试

#### 迁移测试
1. 现有数据迁移测试
2. 兼容性测试
3. 性能测试

### 时间安排

#### 第1天：基础重构
- 修改文件结构
- 实现基础工具函数
- 基本测试

#### 第2天：功能完善
- 实现智能更新
- 添加错误处理
- 完善测试

#### 第3天：集成优化
- 与现有系统集成
- 性能优化
- 文档更新

### 风险控制

#### 技术风险
1. **文件迁移风险**：确保数据不丢失
   - 缓解：先备份，再迁移
   
2. **兼容性风险**：现有代码依赖旧路径
   - 缓解：保持旧工具一段时间，逐步迁移

3. **性能风险**：频繁文件操作可能影响性能
   - 缓解：添加缓存机制，异步处理

#### 业务风险
1. **用户体验变化**：需要适应新工具
   - 缓解：提供详细文档和示例
   
2. **学习成本**：新的工具接口需要学习
   - 缓解：保持接口简单直观

### 成功标准

#### 功能标准
- [ ] 新工具函数正常工作
- [ ] 文件结构正确创建
- [ ] 数据迁移完整无误

#### 性能标准
- [ ] 读取延迟 < 50ms
- [ ] 更新延迟 < 100ms
- [ ] 内存占用合理

#### 用户体验标准
- [ ] 工具使用简单直观
- [ ] 错误信息清晰明确
- [ ] 迁移过程平滑无感

---

*更新于2026-04-23 10:51，采用新的文件结构设计*
