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
