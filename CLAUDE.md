This file provides guidance to Claude Code when working with this repository.

## Project context
- Format: MDX files with YAML frontmatter
- Config: docs.json for navigation, theme, settings
- Components: Mintlify components

## Frontmatter requirements for pages
- title: Clear, descriptive page title
- description: Concise summary for SEO/navigation

## Writing standards
- Match style and formatting of existing pages
- Language tags on all code blocks
- Relative paths for internal links

## Git workflow
- NEVER use --no-verify when committing
- Ask how to handle uncommitted changes before starting
- Commit frequently throughout development
- NEVER skip or disable pre-commit hooks

## Navigation conventions (docs.json)

**Tab order:** Get Started → Articles → An Extended Mind System → Change Log

**File naming by prefix:**
- `pages/index-{tab-slug}` — landing page for a tab
- `pages/article-{slug}` — Articles tab content
- `pages/extended-mind-{slug}` — Extended Mind System context pages
- `pages/collection-{slug}` — Collection group pages
- `pages/reference-{slug}` — Reference group pages
- `pages/change-log-{slug}` / `pages/change-log` — Change Log pages

**Group order within "An Extended Mind System":** Get Started → Collections → Reference

**Collections** are listed alphabetically within their group.

**Change Log** lists the "about" page first, then the log page.

**Global anchor:** Single entry — "Amanda Mashburn" with `house` icon, linking to personal site.

## Page structure
- Every page ends with a divider and timestamp: `---` then `Last update: YYYY.MM.DD`
- Incomplete pages: append `(DRAFT)` or `(PLACEHOLDER)` to the `title` frontmatter value — not as separate fields
- Page order: establish context/rationale first, then practical implementation

## Mintlify components
Only use Mintlify-native components. Components in active use:
- `<Columns cols={2}>` + `<Card>` — grid layouts and navigation cards
- `<Callout>` — prerequisites, warnings, context-setting notices
- `<Accordion>` — long collapsible content (e.g., prompts)
- `<Update label="YYYY-MM-DD">` — change log entries

## Images and assets
- Content images: hosted on Cloudflare R2, embedded as `![Alt text](url)`
- `/assets/` directory: site-level files only (logo, favicon, social card) — never store content images here

## Do not
- Skip frontmatter on any MDX file
- Add frontmatter fields beyond `title` and `description`
- Omit the `Last update:` timestamp from new or edited pages
- Use absolute URLs for internal links (internal links: `/pages/page-name`, no `.mdx` extension)
- Store content images in `/assets/`
- Use custom or third-party components (Mintlify-native only)
- Make assumptions - always ask for clarification