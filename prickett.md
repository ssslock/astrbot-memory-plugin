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

## Recent Updates

- 2026-04-22 20:06: Created create-directory skill
- Skills directory structure established
- This prickett.md file created

## Future Improvements

1. Add more utility skills (file operations, text processing, etc.)
2. Create skill templates for common patterns
3. Add skill testing framework
4. Document skill integration with astrbot

---

*This file is maintained by Prickett. Last updated: 2026-04-22 20:06:34*
