# 部署测试检查清单

## 代码状态
- ✅ 代码已合并到main分支
- ✅ 代码已推送到origin
- ✅ 分支状态正常

## 文件结构验证
预期的目录结构应该已经创建或将在插件启动时创建：

```
/home/ssslock/astrbot/data/plugin_data/astrbot-memory-plugin/
└── memory/
    └── prickett/
        ├── self_prompt.md
        ├── short_term_current.md (待创建)
        └── sessions/
```

## 新工具验证
部署后可以测试以下新工具：

### 1. read_self_prompt
```bash
# 预期：返回self prompt内容
# 如果文件不存在，会自动创建默认内容
```

### 2. update_self_prompt
```bash
# 测试追加内容
update_self_prompt(content="测试追加内容", action="append")

# 测试替换内容  
update_self_prompt(content="# 测试标题\n测试内容", action="replace")

# 测试前置内容
update_self_prompt(content="# 重要提示", action="prepend")
```

### 3. get_self_prompt_file_path (已废弃)
```bash
# 预期：返回废弃警告，但显示文件路径
```

## 测试步骤建议

### 步骤1：检查插件是否正常加载
1. 重启astrbot或重新加载插件
2. 检查日志是否有错误

### 步骤2：测试基本功能
```python
# 在对话中测试
主人: "读取一下self prompt"
莉莉: 调用read_self_prompt()并返回内容

主人: "在self prompt里添加'测试内容'"
莉莉: 调用update_self_prompt(content="测试内容", action="append")
```

### 步骤3：验证文件创建
1. 检查文件是否创建：`/home/ssslock/astrbot/data/plugin_data/astrbot-memory-plugin/memory/prickett/self_prompt.md`
2. 检查内容格式是否正确
3. 检查时间戳是否自动更新

## 已知问题处理

### 如果插件加载失败
1. 检查Python语法错误
2. 检查导入依赖
3. 查看astrbot日志

### 如果工具不可用
1. 检查工具是否正确定义为`@llm_tool`
2. 检查函数签名是否正确
3. 检查插件是否成功注册

### 如果文件未创建
1. 检查目录权限
2. 检查路径解析逻辑
3. 检查`on_enable`方法是否执行

## 回滚方案

如果新代码有问题，可以回滚到上一个版本：

```bash
# 在仓库中
git revert HEAD
git push origin main

# 或者使用之前的提交
git reset --hard 0cedc3c
git push origin main --force
```

## 成功标准

- [ ] 插件正常加载，无错误日志
- [ ] `read_self_prompt` 返回有效内容
- [ ] `update_self_prompt` 成功更新文件
- [ ] 文件在正确位置创建
- [ ] 时间戳自动更新
- [ ] 废弃工具返回警告但可用

## 后续步骤

如果部署成功：
1. 开始实现短期记忆功能
2. 添加更多测试用例
3. 优化性能和错误处理

如果部署失败：
1. 分析错误原因
2. 修复问题
3. 重新部署

---
*测试时间: 2026-04-23 11:14*
*部署提交: 555b75a*
