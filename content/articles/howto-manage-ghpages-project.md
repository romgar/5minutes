Title: How to manage GitHub Pages on front-end project
Date: 2015-05-05 17:47
Modified: 2015-05-05 17:47
Category: Technical
Tags: GitHub, front-end
Slug: howto-manage-ghpages-project
Authors: Romain Garrigues
Summary: How to manage GitHub Pages on front-end project

You are working on a frond-end project hosted on GitHub, with lot of useful tools (grunt/gulp, sass, ...), and you want to properly manage generated files from this project on GitHub Pages ?

Let's imagine this kind of folder on your `master` branch:

    .
    +-- Gruntfile.js
    +-- bower.json
    +-- package.json
    +-- README.md
    +-- dist  <-- You need this folder to be the root of the gh-pages branch
    |   +-- index.html
    |   +-- other_page.html
    |   +-- theme
    |   |    +-- main.css

If you want to use [GitHub pages](https://pages.github.com/) to access your static files, then you need to :

1. create a branch named `gh-pages`,
* have all your static files at the branch root (including `index.html`).

So that, when you checkout `gh-pages`, you need to have:

    .
    +-- index.html
    +-- other_page.html
    +-- theme
    |   +-- main.css


