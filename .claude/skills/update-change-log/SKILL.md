# Update Change Log Skill

1. Run `git diff` to review all current unstaged changes across the codebase.
2. Identify every modified file and summarize what changed in each — be specific (e.g., section removed, title changed, content reformatted).
3. Group the changes into log-worthy entries. Skip changes to `change-log.mdx` itself, `docs.json` nav/config tweaks that aren't user-facing, and timestamp-only updates unless they accompany real content changes. Do include `docs.json` changes that are visible to readers (e.g., renamed anchors, icon changes).
4. Open `pages/change-log.mdx` and check whether a `<Update label="YYYY-MM-DD">` entry for today already exists.
   - If it exists, update it in place.
   - If it does not exist, insert a new one at the top of the file, directly after the frontmatter.
5. Write each bullet in this format, matching the style of existing entries:
   - `Updated: [Page title](/pages/page-slug) – One sentence describing what changed.`
   - `Published: [Page title](/pages/page-slug)` (no description needed for new pages)
   - For non-page changes (e.g., global anchor, navigation): describe plainly without a link.
6. Keep descriptions to one sentence. Lead with the change, not the reason.
7. Update `Last update:` in `pages/change-log.mdx` to today's date in `YYYY.MM.DD` format if it isn't already current.
