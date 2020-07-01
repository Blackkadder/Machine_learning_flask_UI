# ML Flask UI

Flask based UI for interactive apps with machine learning models.

Base template based on Atlantis flask dashboard tempplate.


## Project structure

```

< PROJECT ROOT >                          # application root folder
    |
    |--- app/__init__.py                  # application constructor  
    |--- app//assets                      # Img, CSS, Javascript files
    |--- app/templates                    # Jinja2 files
    |            |---<includes>           # Page chunks, components
    |            |---<layouts>            # Layouts
    |            |---<pages>              # Pages
    |                |---- index.html     # Main dashboard page
    |                |---- login.html     # Login page
    |                |---- register.html  # Registration Page
    |                |---- tables.html    # UI Tables
    |                |---- charts.html    # Charts
    |
    |--- requirements.txt                 # Modules and dependencies
    |
    |--- run.py                           # bootstrap the app
    |
    |-----------------------------


```


~ Rob