"""Generate static project pages. Uses only Python's standard library."""

import argparse
import json
import time
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
COLLECTIONS = ("projects", "class-projects")
TEMPLATE = ROOT / "templates" / "project.html"


def local_path(path):
    """Convert site paths to relative links from either project output folder."""
    return "../" + path.lstrip("/")


def paragraphs(text):
    return "\n".join(f"<p>{escape(part)}</p>" for part in text.split("\n\n") if part.strip())


def image_figure(image, lazy=True):
    src = escape(local_path(image["src"]))
    alt = escape(image["alt"])
    caption = escape(image.get("caption", ""))
    loading = ' loading="lazy"' if lazy else ""
    return f'''<figure class="document-figure project-image">
      <a href="{src}" aria-label="Open full-size image: {alt}">
        <img src="{src}" alt="{alt}" width="{int(image['width'])}" height="{int(image['height'])}"{loading}>
      </a>
      <figcaption>{caption}</figcaption>
    </figure>'''


def repository_buttons(project):
    repositories = project.get("repositories", [])
    # Keep older single-repository entries working.
    if not repositories and project.get("github_url"):
        repositories = [{"label": "View source on GitHub", "url": project["github_url"]}]
    if not repositories:
        return ""
    buttons = []
    for repository in repositories:
        label = escape(repository.get("label", "GitHub repository"))
        url = escape(repository["url"])
        buttons.append(f'<a class="button repository-link" href="{url}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">&#8599;</span></a>')
    return '<div class="repository-links" aria-label="Project source repositories">' + "\n".join(buttons) + "</div>"


def system_outline(project):
    diagram = project.get("diagram")
    if diagram:
        src = escape(local_path(diagram["src"]))
        alt = escape(diagram["alt"])
        title = escape(project["title"])
        result = f'''<figure class="document-figure flow-figure">
          <img src="{src}" alt="{alt}" width="600" height="330" loading="lazy">
          <figcaption>System overview / {title}</figcaption>
        </figure>'''
    else:
        steps = [f"<span>{escape(step)}</span>" for step in project.get("flow", [])]
        result = '<div class="architecture-flow" aria-label="Conceptual system flow">' + '<i aria-hidden="true">&#8594;</i>'.join(steps) + "</div>"
    return result + paragraphs(project.get("system_notes", ""))


def render_project(project, story, template):
    fields = ("area", "platform", "focus", "course", "role", "year", "status")
    metadata = []
    for field in fields:
        if project.get(field):
            metadata.append(f"<div><dt>{field.upper()}</dt><dd>{escape(str(project[field]))}</dd></div>")
    gallery = ""
    images = project.get("images", [])
    if images:
        figures = "\n".join(image_figure(image) for image in images)
        gallery = f'''<section id="gallery">
          <p class="eyebrow">04 / PROJECT IMAGES</p><h2>A closer look</h2>
          <div class="project-gallery">{figures}</div>
        </section>'''
    next_project = ""
    if project.get("next_project"):
        url = escape(local_path(project["next_project"]))
        next_project = f'<a href="{url}">Next project <span aria-hidden="true">&#8594;</span></a>'
    return template.substitute(
        title=escape(project["title"]),
        summary=escape(project["summary"]),
        number=escape(str(project["number"])),
        area_upper=escape(project["area"].upper()),
        metadata="\n".join(metadata),
        repository_links=repository_buttons(project),
        hero=image_figure(project["hero"], lazy=False) if project.get("hero") else "",
        overview=paragraphs(project["overview"]),
        system=system_outline(project),
        components="\n".join(f"<li>{escape(item)}</li>" for item in project["components"]),
        gallery_link='<a href="#gallery">04 / Project images</a>' if images else "",
        gallery=gallery,
        story=story,
        next_project=next_project,
        collection_anchor="class-projects" if project.get("collection") == "class" else "projects",
        collection_label="Class projects" if project.get("collection") == "class" else "All projects",
        back_label="BACK TO CLASS PROJECTS" if project.get("collection") == "class" else "BACK TO PROJECTS",
    )


def class_project_card(project, slug):
    """Build a homepage card from a class project's source content."""
    title = escape(project["title"])
    course = escape(project.get("course", "Class project"))
    summary = escape(project["summary"])
    url = f"class-projects/{slug}.html"
    hero = project.get("hero")
    if hero:
        src = escape(hero["src"].lstrip("/"))
        alt = escape(hero["alt"])
        visual = f'<img src="{src}" alt="{alt}" loading="lazy" width="{int(hero["width"])}" height="{int(hero["height"])}">'
    else:
        visual = f'<span class="course-code">{course}</span><span class="course-caption">{escape(project["area"])}</span>'
    return f'''<article class="project-card class-project-card">
      <div class="class-project-visual">{visual}</div>
      <div class="project-content">
        <p class="eyebrow">{course}</p>
        <h3><a href="{url}">{title}<span aria-hidden="true">&#8599;</span></a></h3>
        <p>{summary}</p>
        <a class="project-link" href="{url}">Explore coursework <span aria-hidden="true">&#8594;</span></a>
      </div>
    </article>'''


def build():
    template = Template(TEMPLATE.read_text(encoding="utf-8"))
    changed = 0
    class_cards = []
    for collection in COLLECTIONS:
        output = ROOT / collection
        output.mkdir(exist_ok=True)
        for source in sorted((ROOT / "content" / collection).glob("*.json")):
            project = json.loads(source.read_text(encoding="utf-8"))
            project["collection"] = "class" if collection == "class-projects" else "main"
            story_path = source.with_suffix(".html")
            story = story_path.read_text(encoding="utf-8") if story_path.exists() else ""
            result = render_project(project, story, template)
            if collection == "class-projects":
                class_cards.append(class_project_card(project, source.stem))
            destination = output / (source.stem + ".html")
            # Unchanged files stay untouched so Live Server doesn't reload needlessly.
            if not destination.exists() or destination.read_text(encoding="utf-8") != result:
                destination.write_text(result, encoding="utf-8")
                changed += 1
    # Only replace the marked class-card area; keep the rest of the homepage intact.
    homepage = ROOT / "index.html"
    original = homepage.read_text(encoding="utf-8")
    start = "<!-- CLASS PROJECTS START -->"
    end = "<!-- CLASS PROJECTS END -->"
    before, remainder = original.split(start, 1)
    _, after = remainder.split(end, 1)
    updated = before + start + "\n" + "\n".join(class_cards) + "\n" + end + after
    if updated != original:
        homepage.write_text(updated, encoding="utf-8")
    print(f"Built project pages: {changed} updated.", flush=True)


def source_changes():
    files = [TEMPLATE]
    for collection in COLLECTIONS:
        content = ROOT / "content" / collection
        files.extend(content.glob("*.json"))
        files.extend(content.glob("*.html"))
    return {file: file.stat().st_mtime_ns for file in files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watch", action="store_true", help="Rebuild when project content or the template changes.")
    args = parser.parse_args()
    build()
    if args.watch:
        previous = source_changes()
        print("Watching project sources. Press Ctrl+C to stop.", flush=True)
        try:
            while True:
                time.sleep(1)
                current = source_changes()
                if current != previous:
                    try:
                        build()
                    except (ValueError, KeyError) as error:
                        print(f"Build error: {error}. Fix the source and save again.", flush=True)
                    previous = current
        except KeyboardInterrupt:
            print("Stopped watching.")


if __name__ == "__main__":
    main()
