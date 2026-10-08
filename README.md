# Blake Hill - Engineering Portfolio

A static GitHub Pages portfolio, with plain HTML/CSS and a small JavaScript filter.
Project pages are generated from one shared template using Python's standard library.
No Ruby, Jekyll, pip packages, or npm packages are required.

## Preview with Live Server

The generated HTML is already in `projects/`, so you can preview immediately:

1. Open this repository folder in VS Code.
2. Right-click the root `index.html` and choose **Open with Live Server**, or use
   your extension's equivalent preview command.
3. Open any project link normally. All detail pages, images, and repository
   buttons are regular HTML and work with the same server.

Use the address your extension displays (often `http://127.0.0.1:5500`).
Use **Stop Live Server** or its status-bar control when you're done.
The site also works by opening `index.html` directly in a browser.

## Where to edit

- `index.html`: homepage, project cards, and about section.
- `styles.css`: shared styling, responsive layouts, and image sizing.
- `script.js`: homepage category filters.
- `templates/project.html`: shared HTML layout for all project pages.
- `content/projects/*.json`: project titles, metadata, descriptions, images, and links.
- `content/projects/*.html`: optional project-specific engineering story sections.
- `scripts/build_projects.py`: generator and optional watch mode.
- `projects/*.html`: generated pages. Edit the source content, not these outputs.
- `images/project-*`: supplied project images and SVG diagrams.

## Rebuild after changing project content

From a terminal in this repository:

```powershell
python scripts/build_projects.py
```

If your computer uses the Windows Python launcher, use `py` instead of `python`.
Run this after editing project JSON, story HTML, or the shared template. You do not
need it after editing the homepage, CSS, images, or homepage JavaScript.

For automatic rebuilding while Live Server runs:

```powershell
python scripts/build_projects.py --watch
```

Keep this terminal open while editing. Saving a project source or the template
regenerates the affected HTML; Live Server can then refresh your browser.
Press **Ctrl+C** to stop the watcher. The watcher itself does not start a server.

## Multiple GitHub repositories for one project

In a project's JSON file, set a labeled list:

```json
"repositories": [
  { "label": "Firmware", "url": "https://github.com/OWNER/FIRMWARE-REPO" },
  { "label": "Backend", "url": "https://github.com/OWNER/BACKEND-REPO" },
  { "label": "Dashboard", "url": "https://github.com/OWNER/DASHBOARD-REPO" }
]
```

Each entry becomes its own button. Add as many entries as you need, then rebuild.
JSON requires double quotes and no trailing commas. You can use any GitHub owner
or organization. Existing `github_url` values still work when `repositories` is
empty; a nonempty list takes precedence. Leave both empty to hide the buttons.

A source repository URL is `https://github.com/OWNER/REPOSITORY`. A live GitHub
Pages demo URL is `https://OWNER.github.io/REPOSITORY/`, only if that repository
has its own Pages site. No GitHub API or authentication is needed for links.

## Add a project

1. Copy `templates/project.json` to `content/projects/your-project.json`.
2. Fill in its title, summary, overview, metadata, components, flow, and links.
   Optional `role`, `year`, and `status` fields appear when supplied.
3. To add a longer engineering story, copy `templates/project-story.html` beside
   that JSON file with the same stem: `content/projects/your-project.html`.
4. Run the build command. It creates `projects/your-project.html`.
5. Add a card to the homepage; update the displayed count and `next_project` links.

For an image, copy the `hero` or `images` structure from an existing project.
Include its path (`/images/project-name.png`), alt text, caption, width, and height.
All project image filenames start with `project-`. Images preserve their aspect
ratio, and clicking them opens the full-size version.

## Add class projects or another class

The homepage has a separate **Class projects** section, linked by **Classes** in
navigation. Data verification lives there, alongside the ECEn 340 course notebook.

1. Copy `templates/class-project.json` to `content/projects/your-class-project.json`.
2. Keep `"collection": "class"`. Set `course` to the course code, and fill in the
   title, summary, overview, and other project fields. A course notebook can use
   its course name as the title and contain several labs or project write-ups.
3. Optionally add `content/projects/your-class-project.html` for longer explanations,
   diagrams, or links to individual lab/project pages. Use `templates/project-story.html`
   as a starting point.
4. Run `python scripts/build_projects.py`, or use watch mode. The generator creates
   the project page **and its homepage class-project card automatically**.

The `course` field appears on the homepage card and in the page metadata. For a
class project without a course code yet, use `"course": "Class project"`.

The generator only edits the area between `CLASS PROJECTS START` and
`CLASS PROJECTS END` in `index.html`. Edit class cards through the JSON files; keep
those markers intact. Other homepage sections remain manually editable.

## Publish on GitHub Pages

Commit the source files and generated `projects/*.html` together. For branch-based
GitHub Pages, publish this repository's root folder. `.nojekyll` tells GitHub to
serve the regular HTML without applying Jekyll. No build command is needed on GitHub.

All generated local links are relative, so the pages also work under a repository
subpath. Public project page URLs remain `projects/project-name.html`.
