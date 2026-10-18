# Franco & Coco — Family Recipes

Static recipe site for francococo.com (GitHub Pages). Plain HTML/CSS/JS — no build tools needed to host.

## Layout
- `index.html` — recipe grid with search and category filter
- `recipes/<slug>.html` — one page per recipe (print-friendly)
- `style.css` — shared styles
- `pdfs/<slug>.pdf` — original recipe printouts
- `assets/img/<slug>.jpg` — recipe photos
- `data/recipes/<slug>.json` — recipe source data
- `build.py` — regenerates the HTML from the JSON (Python 3, standard library only)

## Adding a recipe
1. Create `data/recipes/my-new-dish.json`:
   ```json
   {
     "slug": "my-new-dish",
     "title": "My New Dish",
     "category": "Entree",
     "servings": "4",
     "time": "45 minutes",
     "intro": "Optional short intro.",
     "ingredients": ["## Optional subheading", "1 cup flour", "2 eggs"],
     "steps": ["Mix.", "Bake."],
     "notes": ["Optional note."],
     "image": "assets/img/my-new-dish.jpg",
     "pdf": "pdfs/my-new-dish.pdf"
   }
   ```
   Categories: Appetizer, Entree, Salads, Soup, Sides, Dessert, Breakfast. Lines starting with `## ` become subheadings. Write `[unclear]` for anything you can't read.
2. Add the photo / PDF if you have them (both optional).
3. Run `python3 build.py`, then commit and push.

## Hosting
`CNAME` contains `francococo.com`; `.nojekyll` disables Jekyll processing on GitHub Pages.
