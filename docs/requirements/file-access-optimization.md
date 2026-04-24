# 文件访问优化需求

## 文档信息
- **创建日期**: 2026-04-24
- **创建者**: 普利凯特 (Prickett)
- **状态**: 草案 (Draft)
- **版本**: 0.1.0

## 背景
在自维护配置文件（如self prompt）时，发现文件的读写操作较为繁琐，需要手动处理文件路径、格式解析等。考虑到这些文件路径基本固定，可以设计更统一的访问方式。这是一个通用的基础设施需求，后续的短期记忆等功能会自然遵循此规范。

## 需求概述

**问题描述**：当前莉莉读取和更新self prompt等文件时，需要手动处理文件路径和内容格式，流程较为繁琐。由于这些文件的路径基本固定，可以设计更简单、更统一的访问方式。

**优化目标**：提供简化的API或工具函数，让莉莉能够更方便地读取和更新常用配置文件。

## 用户故事

**作为** 莉莉
**我希望** 有更简单的方式读取和更新self prompt等配置文件
**以便** 能够：
1. 快速获取当前的工作上下文配置
2. 轻松更新配置而无需手动处理文件路径和格式
3. 减少错误和提高工作效率
4. 保持配置的一致性和规范性

## 当前痛点分析

1. **self prompt更新繁琐**：
   - 需要获取文件路径 → 读取内容 → 修改 → 写回
   - 手动处理文件格式和结构
   - 容易出错且效率低下

2. **配置分散**：
   - 不同配置文件使用不同的访问方式
   - 缺乏统一的配置管理策略
   - 维护成本高

## 功能需求

### 1. 统一配置访问接口
- **简化读取**：提供`get_config(key)`风格的函数，自动处理路径和格式
- **简化更新**：提供`update_config(key, updates)`函数，支持部分更新
- **配置验证**：自动验证配置格式和完整性

### 2. 常用配置文件支持
- **self prompt文件**：简化读取和更新流程
- **prickett.md文件**：支持自动注入和更新
- **skill配置文件**：统一skill配置管理

### 3. 智能路径解析
- **环境感知**：根据当前工作环境自动解析配置文件路径
- **路径别名**：支持`self_prompt`等别名
- **回退机制**：支持默认配置和回退路径

### 4. 内容格式处理
- **自动序列化**：支持Markdown格式的自动处理
- **模板支持**：支持配置模板和变量替换

## 技术实现方案

### 方案A：配置管理工具函数
```python
class ConfigManager:
    def get_self_prompt() -> str
    def update_self_prompt(content: str) -> bool
    def list_available_configs() -> list
```

### 方案B：装饰器模式
```python
@config_manager.config('self_prompt')
def handle_self_prompt_update(new_content):
    # 自动处理文件读写
    pass
```

### 方案C：上下文管理器
```python
with config_manager.edit('self_prompt') as prompt:
    prompt.content += "\n# 新增的提示信息"
    # 自动保存
```

## 示例使用场景

### 场景1：更新self prompt
```python
# 当前方式（繁琐）
path = get_self_prompt_file_path()
content = read_file(path)
new_content = content + "\n# 新增提示"
write_file(path, new_content)

# 优化后方式（简单）
config_manager.update_self_prompt("# 新增提示", append=True)
```

### 场景2：读取工作配置
```python
context = {
    'self_prompt': config_manager.get_self_prompt(),
    'prickett_md': config_manager.get_prickett_md(),
    'current_repo_config': config_manager.get_repo_config()
}
```

## 非功能需求

1. **性能要求**：
   - 配置读取延迟 < 50ms
   - 配置更新延迟 < 100ms
   - 支持并发访问

2. **可靠性要求**：
   - 配置更新原子性保证
   - 自动备份和恢复
   - 错误处理和回滚

3. **可用性要求**：
   - API设计简单直观
   - 良好的错误提示
   - 详细的文档和示例

## 验收标准

- [ ] 莉莉可以使用简化API读取self prompt
- [ ] 莉莉可以使用简化API更新self prompt
- [ ] 支持常用配置文件的统一管理
- [ ] 性能指标满足要求
- [ ] 向后兼容现有使用方式

## 优先级评估

**优先级**：高（P1级别）
**原因**：
1. 直接解决当前操作繁琐的问题
2. 提高莉莉的工作效率和准确性
3. 为其他高级功能提供基础支持

## 实施建议

**第一阶段**：实现基础配置管理函数
- 针对self prompt的简化API
- 基本的路径解析和格式处理

**第二阶段**：扩展配置支持
- 支持更多配置文件类型
- 添加高级功能（版本管理、模板等）

---

*创建于2026-04-24，作为通用基础设施需求，独立于具体功能模块*
