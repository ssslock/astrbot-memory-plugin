# Prickett's Notes

## Repository Overview

This is the astrbot-memory-plugin repository, maintained by Prickett (AI assistant).

## Skills Directory

The `skills/` directory contains reusable skills that can be used by AI assistants:

### Available Skills:
1. **create-directory** - Directory creation and folder structure management
   - Path: `skills/create-directory/`
   - Description: Use when creating directories, organizing files, or setting up project structures
   - Includes: SKILL.md, scripts, references, and templates

### Adding New Skills:
1. Create a new directory under `skills/`
2. Include at minimum a `SKILL.md` file with YAML frontmatter
3. Add supporting files as needed (scripts/, references/, assets/)
4. Follow the skill-creator pattern from anthropics/skills

## Development Guidelines

### 1. Commit Frequently
- **Always commit after making meaningful changes**
- Use descriptive commit messages
- Follow conventional commit format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore

### 2. Code Quality
- Write clear, documented code
- Include error handling
- Consider cross-platform compatibility
- Add tests when appropriate

### 3. Documentation
- Keep README.md updated
- Document new features
- Include usage examples
- Update CHANGELOG.md for significant changes

### 4. Skill Development
- Skills should be self-contained and reusable
- Include clear triggering descriptions
- Provide practical examples
- Consider edge cases and error scenarios

## Workflow Tips

### For Prickett (AI Assistant):
1. **Check prickett.md first** when starting work on this repository
2. **Read existing skills** for patterns and examples
3. **Commit immediately** after completing logical units of work
4. **Reference this file** in self-prompt for context awareness

### For Human Developers:
1. Review skills in `skills/` directory
2. Check commit history for recent changes
3. Update prickett.md with new guidelines as needed
4. Coordinate with Prickett for AI-assisted development

## Commit Message Prefix Convention

### [M] Prefix - Master's Changes
When Prickett helps the master commit changes:
1. First use `git diff` to review the master's changes
2. Understand what changes were made
3. Create a commit with `[M]` prefix followed by descriptive message
4. Example: `[M] docs: 统一术语，将'用户/AI'改为'主人/莉莉'`

### [P] Prefix - Prickett's Own Changes
When Prickett makes changes on its own:
1. Commit immediately after completing the work
2. Use `[P]` prefix followed by descriptive message
3. Example: `[P] docs: update prickett.md with new workflow guidelines`

### Workflow for Helping Master Commit:
1. Check git status to see what files are modified
2. Use `git diff` to review the specific changes
3. Summarize the changes for the master
4. Create commit with `[M]` prefix and clear description
5. If needed, push to remote repository

## Recent Updates

- 2026-04-22 20:06: Created create-directory skill
- Skills directory structure established
- This prickett.md file created
- 2026-04-23 09:47: Added commit message prefix convention [M]/[P]

## Future Improvements

1. Add more utility skills (file operations, text processing, etc.)
2. Create skill templates for common patterns
3. Add skill testing framework
4. Document skill integration with astrbot

---

*This file is maintained by Prickett. Last updated: 2026-04-23 09:47:00*

## 部署流程

### 完整部署步骤
1. **开发完成**：在功能分支（如`feat/xxx`）完成开发
2. **合并到main**：`git checkout main && git merge feat/xxx`
3. **推送到origin**：`git push origin main`
4. **手动更新插件**：在astrbot界面或通过命令手动更新/重载插件
5. **测试验证**：测试新功能是否正常工作

### 注意事项
- 部署后需要手动更新插件，代码不会自动生效
- 测试时注意查看astrbot日志是否有错误
- 如有问题，可以回滚到之前的提交

### 简化部署建议（未来）
考虑实现自动部署或更简单的更新机制，减少手动步骤。

## 文件管理

### Git忽略规则
以下目录和文件已被添加到.gitignore：
- `work-context/` - 工作上下文临时文件
- `__pycache__/` - Python缓存文件
- `*.pyc`, `*.pyo`, `*.pyd` - Python编译文件
- `.Python` - Python环境文件

### 临时文件管理
- `work-context/` 目录用于存放临时工作文件
- 这些文件不应提交到版本控制
- 重要数据应存储在`memory/`目录下

---
*更新于2026-04-23 11:33，添加部署流程和gitignore规则*
