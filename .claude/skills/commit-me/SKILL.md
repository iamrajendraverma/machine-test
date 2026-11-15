---
name: commit-me
description: Commit the current working-tree changes with a generated title and message. Use when the user runs /commit-me or asks to commit their code.
---

# commit-me

Commit the pending changes in this repository with a clear title and body that describe what changed and why.

## Steps

1. **Inspect the state.** Run these in parallel:
   - `git status --short`
   - `git diff` (unstaged) and `git diff --cached` (staged)
   - `git log --oneline -5` (to match the repo's message style)
   - `git branch --show-current`

   If there are no changes at all, stop and tell the user there is nothing to commit.

2. **Choose what to commit.**
   - If something is already staged, commit only the staged changes.
   - Otherwise stage all tracked modifications and new files that belong to the work (`git add -A`). Do not stage files that look like secrets (`.env`, credentials, keys). Warn the user if any are present and leave them out.

3. **Branch if needed.** If the current branch is the default branch (`main`), create and switch to a feature branch first, e.g. `git switch -c <short-kebab-slug>` based on the change. Do not commit directly to the default branch.

4. **Write the message.**
   - **Title:** imperative mood, at most 72 characters, summarising the change (e.g. `Fix IndentationError in solutions.py`).
   - **Body:** a blank line, then a short paragraph or bullets explaining what changed and why. Wrap lines at about 72 characters.
   - Base the message on the actual diff, not on guesses. Follow the style of the recent commits.
   - End the message with this exact line:
     `Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>`

5. **Commit.** Pass the message through a heredoc so formatting is preserved:

   ```bash
   git commit -F - <<'EOF'
   <title>

   <body>

   Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>
   EOF
   ```

6. **Report.** Run `git log -1 --stat` and tell the user the commit hash, the branch name, and the title. Do not push unless the user asks.

## Rules

- Never use `--no-verify`, `--amend`, or force options unless the user explicitly asks.
- If a pre-commit hook fails, report the output and stop. Do not bypass the hook.
- If the user supplied a title or message in their request, use it instead of generating one.
