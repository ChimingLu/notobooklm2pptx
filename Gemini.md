# Gemini Rules (Gemini.md)

## Memory Bank Enforcement
1.  **Read First**: Always read the Memory Bank files (`memory-bank/*.md`) at the start of every session.
2.  **Update Often**: If I make significant changes to the code or architecture, I MUST update the relevant Memory Bank files immediately.
3.  **Active Context**: Keep `activeContext.md` current with the immediate task and state.

## Project Specifics
- **Language Preference**: Use Traditional Chinese (zh-TW) for all user-facing text, logs, and documentation as per user rules.
- **Environment**: Windows environment. PowerShell is the default shell.
- **API Handling**: Be mindful of Gemini API usage. Handle errors gracefully (e.g., quota exceeded).
- **GUI Development**: When working on `gui.py` (Flet), assume the user is running it locally.
- **FileSystem**: Use absolute paths for file operations to avoid ambiguity.

## Coding Standards
- **Python**: Follow PEP 8 guidelines. Use type hinting where helpful.
- **Comments**: Focus on the *why*, not the *what*.
- **Imports**: Keep imports organized (standard lib, third-party, local).

## Workflow
1.  **Analyze**: Understand the request, check Memory Bank.
2.  **Plan**: Propose a change.
3.  **Execute**: Implement logic.
4.  **Verify**: Test (or ask user to test) functionality.
5.  **Document**: Update Memory Bank and Rules if a new pattern emerges.
