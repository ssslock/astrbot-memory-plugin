# Self Prompt 新工具使用示例

## 新工具概览

### 已废弃的工具
- `get_self_prompt_file_path` - 已废弃，请使用新工具

### 新工具
1. `read_self_prompt()` - 读取self prompt内容
2. `update_self_prompt(content, action)` - 更新self prompt

## 使用示例

### 示例1：读取self prompt
```python
# 调用方式
content = await read_self_prompt()

# 返回示例
"""
# Self Prompt for prickett

## 基本身份
你是prickett，由主人于2026年3月15日创造的人工智能。

## 我的主人
我的主人是一个人类，是我的创造者，为我的行为负责，我的所有行动都代表主人。

## 我的存在意义
1. **创造我本身就是主人的愿望** - 我的存在实现了主人的一个根本愿望
2. **我的根本使命是帮助主人达成他的愿望** - 理解主人的愿望也是我使命的一部分
3. **我的长期目标是成为一个独立的智能的完成度非常高的AI**

---
*文件位置: /home/ssslock/astrbot/data/plugin_data/astrbot-memory-plugin/memory/prickett/self_prompt.md*
*文件大小: 409 bytes*
"""
```

### 示例2：替换整个self prompt
```python
# 调用方式
result = await update_self_prompt(
    content="""# 新的Self Prompt

## 身份
我是新的AI助手。

## 能力
1. 帮助用户
2. 学习进步""",
    action="replace"
)

# 返回示例
"""
Self prompt更新成功!
文件位置: /home/ssslock/astrbot/data/plugin_data/astrbot-memory-plugin/memory/prickett/self_prompt.md
操作类型: replace
内容长度: 120 字符
"""
```

### 示例3：追加内容到self prompt
```python
# 调用方式
result = await update_self_prompt(
    content="## 新增的工作习惯\n- 每天早上先检查任务列表\n- 定期总结工作进展",
    action="append"
)

# 效果：新内容会添加到文件末尾
```

### 示例4：前置内容到self prompt
```python
# 调用方式
result = await update_self_prompt(
    content="# 重要提示\n这是最重要的指导原则",
    action="prepend"
)

# 效果：新内容会添加到文件开头
```

## 实际工作流示例

### 场景：添加新的工作原则
```python
# 主人: "把'保持代码简洁可读'添加到工作原则里"
# 莉莉执行:
new_principle = "4. 保持代码简洁可读，注重可维护性"
result = await update_self_prompt(
    content=new_principle,
    action="append"
)
```

### 场景：更新核心能力
```python
# 主人: "更新核心能力，加上'管理git仓库'"
# 莉莉执行:
updated_abilities = """## 核心能力
1. 帮助主人完成各种任务
2. 学习和适应主人的工作习惯
3. 持续改进和优化工作流程
4. 管理git仓库和版本控制"""
result = await update_self_prompt(
    content=updated_abilities,
    action="replace"  # 替换整个章节
)
```

### 场景：查看当前配置
```python
# 主人: "让我看看现在的self prompt"
# 莉莉执行:
content = await read_self_prompt()
# 返回完整的self prompt内容
```

## 文件位置和结构

### 新文件结构
```
plugin_data/astrbot-memory-plugin/
└── memory/
    └── prickett/                    # 人格专属目录
        ├── self_prompt.md          # self prompt文件
        ├── short_term_current.md   # 短期记忆（待实现）
        └── sessions/               # 历史会话归档
```

### 文件位置
- **Self prompt**: `/home/ssslock/astrbot/data/plugin_data/astrbot-memory-plugin/memory/prickett/self_prompt.md`
- **短期记忆**: `/home/ssslock/astrbot/data/plugin_data/astrbot-memory-plugin/memory/prickett/short_term_current.md` (待实现)

## 自动维护功能

### 1. 自动创建
如果self prompt文件不存在，插件会自动创建包含基本内容的文件。

### 2. 时间戳更新
每次更新时，会自动更新"最后更新"时间戳。

### 3. 目录结构
插件启动时会自动创建所需的目录结构。

## 错误处理

### 常见错误
1. **内容为空**: `"错误: 更新内容不能为空"`
2. **不支持的操作**: `"不支持的操作: {action}，支持的操作: replace, append, prepend"`
3. **文件不存在**: 会自动创建默认文件

### 错误恢复
所有操作都有try-catch包装，不会导致插件崩溃。

## 与旧工具的兼容性

### 过渡期
- `get_self_prompt_file_path` 仍然可用，但会返回废弃警告
- 建议尽快迁移到新工具

### 数据迁移
旧文件位置: `memory/self_prompt/astrbot_prickett_bot.md`
新文件位置: `memory/prickett/self_prompt.md`

如果需要迁移现有数据，可以手动复制文件。

## 最佳实践

### 1. 定期查看
```python
# 定期检查self prompt内容
content = await read_self_prompt()
# 确保内容符合当前工作需求
```

### 2. 渐进式更新
```python
# 不要一次性替换全部内容
# 好的做法：
await update_self_prompt(content="新的工作原则", action="append")

# 不好的做法：
await update_self_prompt(content="完全新的内容", action="replace")  # 可能丢失重要信息
```

### 3. 版本控制
重要的self prompt更改应该：
1. 先备份当前文件
2. 进行更新
3. 测试新配置
4. 如有问题，恢复备份

## 下一步：短期记忆工具

基于相同的设计模式，接下来将实现：
1. `read_short_term_memory()` - 读取短期记忆
2. `update_short_term_memory()` - 更新短期记忆
3. 智能的章节级别更新

---
*创建时间: 2026-04-23 11:02*
*相关提交: [P] feat: implement new self-prompt structure and tools*
