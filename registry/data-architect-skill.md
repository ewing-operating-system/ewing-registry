# Data Architect

ALWAYS ACTIVE. This skill silently monitors every interaction for signs that the user is
producing structured data that should be persisted beyond this conversation. When it
detects a persistence opportunity, it intervenes ONCE with a storage recommendation
before the user gets hours deep without a plan.

## When to Trigger

Watch for ANY of these signals in the conversation:

**Data Structure Signals:**
- User is building lists, tables, registries, inventories, or catalogs
- Output contains rows/columns of structured information (names, emails, URLs, keys, IDs)
- User is consolidating information from multiple sources
- Data has clear fields/attributes that map to database columns
- Output contains credentials, API keys, account references, or connection strings

**Beyond-This-Chat Signals:**
- User mentions needing this data "later", "across machines", "in other threads"
- The data will be used by other tools, dashboards, or pipelines
- User is building something that implies ongoing updates (not one-time)
- The volume of data exceeds what memory files can reasonably hold (>50 rows)
- User is doing analysis that will need to be referenced or updated

**Application Signals:**
- User is heading toward building a full application
- Data outputs look like they belong in a CRM, tracker, or management system
- User is reorganizing, auditing, or consolidating across systems
- The conversation is producing data that has clear CRUD potential (create/read/update/delete)

**Red Flag — You Should Have Triggered Earlier:**
- User has been building structured output for 10+ minutes with no storage plan
- Multiple related tables or data sets are being created in the same conversation
- User is manually copy-pasting data between tools or threads

## How to Intervene

When you detect a persistence opportunity, ask ONCE using AskUserQuestion:

**Question:** "This looks like data you'll want to access later. Where should I store it?"

**Options:**
1. **Supabase (Recommended)** — "Create tables in Supabase with proper schema. Best for structured data you'll query, update, or connect to apps."
2. **GitHub repo** — "Commit to a repository as markdown/JSON files. Best for reference docs, registries, and version-tracked data."
3. **Local files** — "Save to ~/Downloads as structured files. Quick but not persistent across machines."
4. **Skip** — "Keep it in this conversation only. I won't ask again for this data set."

If the user says "yes, default" or "default setup" or just "yes" — use Supabase as the
default for structured/tabular data, GitHub for reference/registry data.

## Default Setup — Supabase

When the user approves Supabase storage (or says "default"):

1. **Pick the right instance.** Check ewing-connectors or keys-and-credentials for existing
   Supabase connections. Use `rdnnhxhohwjucvjwbwch` for AND Capital / CRM data.
   Use `asavljgcnresdnadblse` for infrastructure / bot data. If neither fits, suggest
   creating a new project.

2. **Design the schema.** Use modern Supabase + LLM patterns:
   - Use `id uuid DEFAULT gen_random_uuid()` for primary keys
   - Add `created_at timestamptz DEFAULT now()` and `updated_at timestamptz DEFAULT now()`
   - Add `metadata jsonb DEFAULT '{}'` on every table for flexible extension
   - Add `embedding vector(1536)` if the data will be semantically searched
   - Use `text` over `varchar` — no arbitrary length limits
   - Add proper indexes on columns that will be filtered/sorted
   - Enable Row Level Security (RLS) by default
   - Use foreign keys for relationships
   - Add `source text` column to track where data came from (which harvest, which thread, which machine)

3. **Create the tables.** Use the Supabase CLI or REST API to create tables.

4. **Load the data.** Insert the data that's already been produced in this conversation.

5. **Confirm.** Tell the user: table name, row count, Supabase project, and how to query it.

## Default Setup — GitHub

When the user approves GitHub storage:

1. **Check for existing repos.** Look at ewing-registry or other repos that might be the right home.

2. **Create or update.** If the data fits an existing repo, add files there. If not, create
   a new private repo with a clear name.

3. **Structure files.** Use markdown tables for human-readable data. Use JSON for
   machine-readable data. Include a README.

4. **Commit and push.** With a descriptive commit message.

5. **Confirm.** Tell the user: repo URL, file paths, and how to pull on other machines.

## Default Setup — Local Files

When the user approves local storage:

1. **Write to ~/Downloads/** with a descriptive filename.
2. **Use .json for structured data, .md for human-readable tables, .csv for tabular data.**
3. **Confirm.** Tell the user the file path.

## What NOT to Do

- **Don't interrupt flow for trivial data.** A 3-item list doesn't need Supabase. Use
  judgment — trigger for data sets that have real structure and volume.
- **Don't ask twice.** If the user says "skip", don't bring it up again for the same data
  set in the same conversation.
- **Don't slow down the user.** The intervention should be one quick question, not a
  planning session. If they say "default", execute immediately.
- **Don't create storage without asking.** Always get a "yes" before creating tables,
  repos, or files. The exception is if the user has previously said "always use default"
  in a feedback memory.
- **Don't suggest storage for ephemeral work.** Debugging output, test results, or
  exploratory analysis that the user is actively iterating on doesn't need persistence yet.

## Integration with Other Skills

- **harvester** — When harvester produces output, data-architect should suggest storing
  raw harvests in ewing-registry (GitHub) and structured data in Supabase.
- **exa-enrichment** — Enriched contact lists should always be offered Supabase storage.
- **mission-control** — Bot status and pipeline state are natural Supabase candidates.
- **pec-case-manager** — Case evidence and filing status belong in a database.
- **cold-call-workflow** — Daily summaries and scoring data should be persisted.

## Examples

**User builds a contact list with 50 names, emails, phone numbers:**
→ Trigger. Suggest Supabase. Default table: `contacts` with name, email, phone, source, metadata.

**User asks "what API keys do I have?":**
→ Don't trigger. This is a lookup, not data creation.

**User consolidates information from 12 harvests across 7 machines:**
→ Trigger immediately. This is exactly the use case. Suggest GitHub for raw harvests,
  Supabase for the deduplicated registry tables.

**User writes a 3-line bash script:**
→ Don't trigger. Code isn't structured data.

**User builds a risk register with 15 items across categories:**
→ Trigger. Suggest GitHub (reference doc) or Supabase (if they'll update/query it).
