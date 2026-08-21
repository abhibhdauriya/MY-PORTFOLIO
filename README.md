# Abhishek Singh — Portfolio CMS

A production-quality personal portfolio + private admin CMS, built with Python and Streamlit.

Public visitors see a professional portfolio (projects, Excel/VBA automation work, web apps,
skills, experience, resume, certificates, contact form). You manage all of it from a
password-protected `/admin-login` area — no code edits needed to add a new project.

---

## 1. Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your admin credentials (used only on first run to create your account)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml with your own username/password

# 3. (Optional) Seed realistic demo content so the site looks complete immediately
python seed_demo_data.py

# 4. Run
streamlit run app.py
```

Open the app, go to **Admin** in the sidebar → log in with the credentials you set in
`secrets.toml`. After first login, your password is stored bcrypt-hashed in `portfolio.db` —
`secrets.toml` is no longer read for auth, so you can safely change your password from
**Admin → Site Settings** afterward.

---

## 2. Project Structure

```
portfolio/
├── app.py                  # Entry point — navigation, DB init, styling
├── requirements.txt
├── seed_demo_data.py        # Populates fictional sample content
├── .gitignore
├── .streamlit/
│   ├── config.toml          # Theme
│   └── secrets.toml.example # Copy to secrets.toml, fill in, never commit
├── database/
│   ├── db.py                 # Connection + generic CRUD helpers
│   ├── schema.py              # All table definitions
│   └── backup.py              # DB download / JSON / CSV export
├── auth/
│   └── authentication.py      # bcrypt hashing, session gate, secrets bootstrap
├── pages_public/               # 10 public pages + admin login
├── pages_admin/                 # Dashboard + CRUD pages for every content type
├── components/                   # navbar, cards, filters, custom CSS
└── utils/                         # validators, file_manager, helpers
```

---

## 3. How Content Management Works

- **Projects** (Excel/VBA, Web, MIS, Data Analytics, etc.) all live in one `projects` table
  with a `category` field, so one admin form handles every project type — including
  Excel-specific fields (VBA/Power Query/Power Pivot flags, Excel version) which are simply
  left blank for non-Excel projects.
- Toggle **Featured** to show a project on the homepage; toggle **Published** to hide a
  draft from public view without deleting it.
- File uploads (thumbnails, screenshots, sample `.xlsx`/`.xlsm`, PDFs, resume, certificates)
  are validated by extension and size, saved to `uploads/<type>/` with a randomized filename,
  and the relative path is stored in the DB — never the raw bytes.

---

## 4. Security Notes

- Admin password is **bcrypt-hashed** in the database. It is never stored or displayed in
  plaintext, and never appears in source code.
- `secrets.toml` (your bootstrap credentials) and `portfolio.db` (contains the real hash and
  your content) are both git-ignored — check `.gitignore` before your first commit.
- All SQL queries are parameterized (`?` placeholders) — no string-formatted SQL anywhere in
  the codebase, so standard SQL injection via form fields isn't possible.
- Uploads are restricted to `png/jpg/jpeg/webp/pdf/xlsx/xlsm/xls/csv`, capped at 10MB. No
  executable file types are accepted.
- Admin pages call `require_login()` at the top of every render — there's no admin page
  reachable without a valid session flag, regardless of URL guessing.
- **Never commit real company data.** All demo data in `seed_demo_data.py` is fictional by
  design — replace it with your own sanitized project descriptions, not real employer data,
  screenshots, or internal reports.

---

## 5. Deployment (Streamlit Community Cloud)

### Push to GitHub
```bash
git init
git add .
git commit -m "Initial portfolio CMS"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```
Confirm `git status` does **not** show `.streamlit/secrets.toml` or `portfolio.db` — if it
does, your `.gitignore` isn't being picked up (run `git rm --cached <file>` to untrack it).

### Deploy
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**, select your repository and branch.
3. Set **Main file path** to `app.py`.
4. Under **Advanced settings → Secrets**, paste:
   ```toml
   admin_username = "your-username"
   admin_password = "your-strong-password"
   ```
5. Click **Deploy**.

### ⚠️ Important: ephemeral storage
Streamlit Cloud's filesystem is **not persistent** — it can reset on redeploys, restarts, or
inactivity. That means `portfolio.db` and everything in `uploads/` can be wiped.

**Workflow to protect your data:**
- After adding content, go to **Admin → Database Backup** and download `portfolio.db`
  regularly.
- If the app resets, use the **Restore from Backup** uploader on that same page to reload
  your last download.
- For anything beyond a personal portfolio's scale, migrating to a persistent store
  (e.g. Postgres via Supabase/Neon, or S3-compatible storage for uploads) is the long-term
  fix — the codebase is already structured so `database/db.py` is the only place that would
  need to change.

---

## 6. What's Deliberately Not Included (v1 scope)

Per the "don't overengineer" brief, these are noted as a future upgrade path rather than
built now: PostgreSQL, cloud file storage, a FastAPI backend/REST API, OAuth login, and
GitHub-repo-stats integration. The codebase is modular enough (clean `database/`, `auth/`,
`utils/` boundaries) to add these later without a rewrite.

---

## 7. Running seed data again / resetting

```bash
rm portfolio.db          # wipes all content — back up first if it matters!
python seed_demo_data.py # recreates schema + demo projects/skills
streamlit run app.py
```
