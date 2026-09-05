import streamlit as st
from auth.authentication import require_login
from database.db import fetch_all, fetch_one, insert_row, update_row, delete_row
from utils.file_manager import save_uploaded_file, delete_file
from utils.validators import is_valid_url, required_field_ok
from utils.helpers import PROJECT_CATEGORIES, PROJECT_STATUSES


def _show_flash():
    if st.session_state.get("_project_flash"):
        st.success(st.session_state.pop("_project_flash"))


def project_form(existing: dict | None = None):
    is_edit = existing is not None
    key_prefix = f"edit_{existing['id']}" if is_edit else "new"

    with st.form(f"project_form_{key_prefix}"):
        title = st.text_input("Project Title *", value=existing.get("title", "") if existing else "")
        category = st.selectbox(
            "Category", PROJECT_CATEGORIES,
            index=PROJECT_CATEGORIES.index(existing["category"]) if existing and existing.get("category") in PROJECT_CATEGORIES else 0,
        )
        short_description = st.text_area("Short Description", value=existing.get("short_description", "") if existing else "", height=70)
        detailed_description = st.text_area("Detailed Description", value=existing.get("detailed_description", "") if existing else "", height=100)

        col1, col2 = st.columns(2)
        with col1:
            problem = st.text_area("Problem Statement", value=existing.get("problem", "") if existing else "")
            solution = st.text_area("Solution", value=existing.get("solution", "") if existing else "")
        with col2:
            approach = st.text_area("Approach", value=existing.get("approach", "") if existing else "")
            results = st.text_area("Results / Impact (leave blank if no real metric)", value=existing.get("results", "") if existing else "")

        features = st.text_area("Key Features (one per line)", value=existing.get("features", "") if existing else "")
        technologies = st.text_input("Technologies (comma separated)", value=existing.get("technologies", "") if existing else "")
        tags = st.text_input("Tags (comma separated)", value=existing.get("tags", "") if existing else "")

        col3, col4 = st.columns(2)
        with col3:
            github_url = st.text_input("GitHub URL", value=existing.get("github_url", "") if existing else "")
            live_url = st.text_input("Live Demo URL", value=existing.get("live_url", "") if existing else "")
        with col4:
            documentation_url = st.text_input("Documentation URL", value=existing.get("documentation_url", "") if existing else "")
            demo_video_url = st.text_input("Demo Video URL", value=existing.get("demo_video_url", "") if existing else "")

        col5, col6, col7 = st.columns(3)
        with col5:
            status = st.selectbox("Status", PROJECT_STATUSES, index=PROJECT_STATUSES.index(existing["status"]) if existing and existing.get("status") in PROJECT_STATUSES else 2)
        with col6:
            version = st.text_input("Version (optional)", value=existing.get("version", "") if existing else "")
        with col7:
            project_date = st.text_input("Project Date (YYYY-MM-DD)", value=existing.get("project_date", "") if existing else "")

        col8, col9 = st.columns(2)
        with col8:
            is_featured = st.checkbox("Featured", value=bool(existing.get("is_featured")) if existing else False)
        with col9:
            is_published = st.checkbox("Published", value=bool(existing.get("is_published", 1)) if existing else True)

        st.markdown("##### Excel/VBA-specific (optional — only relevant for Excel Automation / VBA category)")
        ecol1, ecol2, ecol3, ecol4, ecol5 = st.columns(5)
        with ecol1:
            excel_version = st.text_input("Excel Version", value=existing.get("excel_version", "") if existing else "")
        with ecol2:
            uses_vba = st.checkbox("VBA used", value=bool(existing.get("uses_vba")) if existing else False)
        with ecol3:
            uses_python = st.checkbox("Python used", value=bool(existing.get("uses_python")) if existing else False)
        with ecol4:
            uses_power_query = st.checkbox("Power Query", value=bool(existing.get("uses_power_query")) if existing else False)
        with ecol5:
            uses_power_pivot = st.checkbox("Power Pivot", value=bool(existing.get("uses_power_pivot")) if existing else False)

        st.markdown("##### Files")
        thumbnail = st.file_uploader("Thumbnail (PNG/JPG/WEBP)", type=["png", "jpg", "jpeg", "webp"], key=f"thumb_{key_prefix}")
        screenshots = st.file_uploader("Screenshots (multiple allowed)", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key=f"shots_{key_prefix}")
        sample_xlsx = st.file_uploader("Sample .xlsx (sanitized demo only)", type=["xlsx"], key=f"xlsx_{key_prefix}")
        sample_xlsm = st.file_uploader("Sample .xlsm (sanitized demo only)", type=["xlsm"], key=f"xlsm_{key_prefix}")
        pdf_doc = st.file_uploader("PDF Documentation", type=["pdf"], key=f"pdf_{key_prefix}")

        submitted = st.form_submit_button("Save Project", type="primary")

        if submitted:
            errors = []
            if not required_field_ok(title):
                errors.append("Title is required.")
            for url_val, url_label in [(github_url, "GitHub URL"), (live_url, "Live Demo URL"),
                                        (documentation_url, "Documentation URL"), (demo_video_url, "Demo Video URL")]:
                if url_val and not is_valid_url(url_val):
                    errors.append(f"{url_label} looks invalid — must start with http:// or https://")

            if errors:
                for e in errors:
                    st.error(e)
                return

            data = {
                "title": title.strip(), "category": category,
                "short_description": short_description, "detailed_description": detailed_description,
                "problem": problem, "approach": approach, "solution": solution,
                "features": features, "results": results,
                "technologies": technologies, "tags": tags,
                "github_url": github_url, "live_url": live_url,
                "documentation_url": documentation_url, "demo_video_url": demo_video_url,
                "status": status, "version": version, "project_date": project_date,
                "is_featured": int(is_featured), "is_published": int(is_published),
                "excel_version": excel_version, "uses_vba": int(uses_vba),
                "uses_python": int(uses_python), "uses_power_query": int(uses_power_query),
                "uses_power_pivot": int(uses_power_pivot),
            }

            if thumbnail:
                path = save_uploaded_file(thumbnail, "projects")
                if path:
                    data["thumbnail_path"] = path
            if screenshots:
                paths = [save_uploaded_file(f, "screenshots") for f in screenshots]
                data["screenshots"] = ", ".join([p for p in paths if p])
            if sample_xlsx:
                path = save_uploaded_file(sample_xlsx, "projects")
                if path:
                    data["sample_xlsx_path"] = path
            if sample_xlsm:
                path = save_uploaded_file(sample_xlsm, "projects")
                if path:
                    data["sample_xlsm_path"] = path
            if pdf_doc:
                path = save_uploaded_file(pdf_doc, "projects")
                if path:
                    data["pdf_doc_path"] = path

            with st.spinner("Saving..."):
                if is_edit:
                    update_row("projects", existing["id"], data)
                    st.session_state["_project_flash"] = "Project updated successfully."
                else:
                    insert_row("projects", data)
                    st.session_state["_project_flash"] = "Project created successfully."
            st.rerun()


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Manage Projects</div>', unsafe_allow_html=True)
    _show_flash()

    tab_add, tab_manage = st.tabs(["➕ Add Project", "📋 All Projects"])

    with tab_add:
        project_form()

    with tab_manage:
        projects = fetch_all("SELECT * FROM projects ORDER BY created_at DESC")
        if not projects:
            st.caption("No projects yet.")
        for p in projects:
            with st.expander(f"{'⭐ ' if p['is_featured'] else ''}{p['title']} — {p['category']} ({'Published' if p['is_published'] else 'Draft'})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Toggle Featured", key=f"feat_{p['id']}"):
                        update_row("projects", p["id"], {"is_featured": 0 if p["is_featured"] else 1})
                        st.rerun()
                with col2:
                    if st.button("Toggle Published", key=f"pub_{p['id']}"):
                        update_row("projects", p["id"], {"is_published": 0 if p["is_published"] else 1})
                        st.rerun()
                with col3:
                    if st.button("Delete", key=f"del_{p['id']}"):
                        for field in ["thumbnail_path", "sample_xlsx_path", "sample_xlsm_path", "pdf_doc_path"]:
                            delete_file(p.get(field))
                        for shot in (p.get("screenshots") or "").split(","):
                            delete_file(shot.strip())
                        delete_row("projects", p["id"])
                        st.session_state["_project_flash"] = "Project deleted."
                        st.rerun()

                st.markdown("---")
                st.caption("Edit below and click Save Project to update.")
                project_form(existing=p)


render()
