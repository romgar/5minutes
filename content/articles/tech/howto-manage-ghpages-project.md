Title: How to manage GitHub Pages on front-end project
Date: 2015-04-08 20:47
Modified: 2015-04-08 20:47
Category: Tech
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


Solution 1
==========

You could copy your `dist` folder of `master` in another folder (outside of this git project), then checkout to `gh-pages`, paste copied folder to this branch, and commit.
We feel easily that it's not a clean way to manage it, we will have to manually copy/paste each time...

A script could be written to do this kind of task each time we need to deploy on `gh-pages`, but
 somebody has already done that for us : [ghp-import](https://github.com/davisp/ghp-import)

You can install it via `pip`:

    pip install ghp-import

And then, go to your `master` branch, and to deploy your `dist` folder:

    ghp-import dist

It will then create a new commit (and push it) on your `gh-pages` branch with the current files of your `dist` folder.


Solution 2
==========

Clone another time your project in the same project folder:

    .
    +-- Gruntfile.js
    +-- bower.json
    +-- package.json
    +-- README.md
    +-- dist
    |   +-- index.html
    |   +-- other_page.html
    |   +-- theme
    |   |    +-- main.css
    +-- your_project <-- Your cloned project repository on master branch
        +-- Gruntfile.js
        +-- bower.json
        +-- package.json
        +-- README.md
        +-- dist
        |   +-- index.html
        |   +-- other_page.html
        |   +-- theme
        |   |    +-- main.css

Checkout your sub-cloned project to gh-pages branch, and remove everything no more needed in your `gh-pages` branch.

    .
    +-- Gruntfile.js
    +-- bower.json
    +-- package.json
    +-- README.md
    +-- dist
    |   +-- index.html
    |   +-- other_page.html
    |   +-- theme
    |   |    +-- main.css
    +-- your_project <-- Your cloned project repository on gh-pages branch
        +-- index.html
        +-- other_page.html
        +-- theme
        |    +-- main.css

Remove `dist` folder in your `master branch`, and replace it with a symbolic link to `your_project` repository:

    .
    +-- Gruntfile.js
    +-- bower.json
    +-- package.json
    +-- README.md
    +-- dist <-- Now a symlink to your_project
    +-- your_project <-- Your cloned project repository on gh-pages branch
        +-- index.html
        +-- other_page.html
        +-- theme
        |    +-- main.css

Your tools, that were working on `dist` folder, will now generate new content on the project `gh-pages` branch, and you can commit them when you want.
