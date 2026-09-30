# Academic Site — Hugo Apéro + Netlify

A personal/academic website built with the [Hugo Apéro](https://github.com/hugo-apero/hugo-apero) theme and deployed to Netlify from this GitHub repository.

- **Source of truth:** this repo (config + content).
- **Theme:** `hugo-apero/hugo-apero`, cloned automatically at build time (not committed).
- **Hosting:** Netlify builds from the `main` branch on every push.

## Local preview (optional)

You need **Git** and **Hugo (extended)** installed locally.

```bash
git clone --depth 1 --branch main https://github.com/hugo-apero/hugo-apero.git themes/hugo-apero
hugo server -D
# open http://localhost:1313
```

Or just run the same build as Netlify:

```bash
chmod +x build.sh && ./build.sh
```

## Deploy to Netlify

1. Push this repo to GitHub (already done).
2. In Netlify: **Add new site → Import an existing project → GitHub → select this repo**.
3. Netlify auto-detects Hugo from `netlify.toml`. Click **Deploy**.
4. You get a `*.netlify.app` URL. (Optional) Add a custom domain in **Site settings → Domain management** and update `baseURL` in `config.toml`, then push.

Every `git push` to `main` triggers a rebuild and redeploy.

## Daily update workflow

1. Edit Markdown in `content/` (see structure below).
2. Commit and push:

   ```bash
   git add -A && git commit -m "update content" && git push
   ```

3. Netlify rebuilds and publishes automatically.

## Content structure

```
content/
├── about/_index.md     # your bio (type: about)
├── project/            # research projects (one folder per project)
│   ├── _index.md
│   └── sample/index.md
├── talk/               # talks & presentations
│   ├── _index.md
│   └── sample/index.md
├── blog/               # news / posts
│   ├── _index.md
│   └── welcome/index.md
├── contact.md          # contact page
└── license.md          # license page
```

Add images to `static/img/` and reference them with a leading slash, e.g. `/img/photo.jpg`.

## Updating the theme

The theme is pulled from `main` on every build. To pin a specific version, edit `build.sh`
to clone a tag/commit, e.g.:

```bash
git clone --depth 1 --branch v1.2.3 https://github.com/hugo-apero/hugo-apero.git themes/hugo-apero
```

If you bump `HUGO_VERSION` past `0.146.0`, you must also install Dart Sass in `build.sh`
(Hugo removed built-in Sass in 0.146). Keep `HUGO_VERSION = "0.126.1"` unless you have a reason to change it.

## Notes

- Theme license: CC BY 4.0 — keep the attribution.
- `config.toml` holds all site settings (title, social links, color theme, fonts).
- Social icons use Font Awesome (`fab`/`fas`) and Academicons (`ai`).
