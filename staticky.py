"""Quick-and-dirty static site generator for Python 3 (exclusively)
using jinja & markdown.

This script generates the lillian.link static website from `_src`.

I really just made this for fun and I knew exactly
what I wanted in a static site generator:

  * `jinja2` for templates and pages (`_src/templates/`)
  * `markdown` for blog posts (`_src/markdown_blog/`), which can be
    categorized simply by organizing the markdown files into directories

Works exclusively in Python3.

How it works:
    Every file in `_src/templates/` that isn't `base.html`,
    `category-index.html', or `blog-article.html` is a page that gets
    rendered to an HTML file of the same name.

    The `_src/markdown_blog/` directory is scanned for markdown files
    recursively (`*.md`). Metadata, such as creation and modified time,
    are obtained through the file's metadata itself. Files in the
    `_src/markdown_blog/` directory may be put into directories, for
    example `_src/markdown_blog/rants/i-really-love-halloween.md` would
    belong to the `rants` category, and would be rendered to
    `blog/rants/i-really-love-halloween.html`.

    Just modify some files in `_src` and then run this script!

      $ python staticky.py

    If you want to test the site, just do this:

        $ python -m http.server 8000

    ... then open http://localhost/index.html in web browser.

"""

import time
import os
import glob
from collections import namedtuple

import jinja2
from bs4 import BeautifulSoup
import markdown


MARKDOWN_SOURCE = os.path.join('_src', 'markdown_blog')


jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader('_src', 'templates')
)


class Post(object):
    """A blog post; make templating much easier.

    Constants:
        SUMMARY_CHARACTER_LIMIT (int): --
        TEMPLATE (str): jinja2 template to pull from the jinja2
            environment. This temple is used to render the post.

    Attributes:
        href (str): Relative path to this article (html). Usable for
            both writing to local directory and as the href attribute
            of a link, in order to link to this post.
        category (str): Derived from the name of the directory
            containing this post.
        summary (str): A string summary (truncated) of the first
            paragraph of the content.
        content (BeautifulSoup): --
        modified (str): --
        modified_epoch (str): --
        created (str): --
        created_epoch (int): --
        title (str): The first <h1> tag once the markdown was rendered
            to HTML.

    """

    SUMMARY_CHARACTER_LIMIT = 100
    TEMPLATE = 'blog-article.html'

    def __init__(self, file_path):
        self.category = self.get_category(file_path)
        self.content, self.title = self.get_html(file_path)
        self.summary = self.summarize(self.content)
        self.href = self.get_href(self.category, file_path)
        self.modified, self.modified_epoch = self.get_date(
            file_path,
            os.path.getmtime
        )
        self.created, self.created_epoch = self.get_date(
            file_path,
            os.path.getctime
        )

        if not os.path.exists('blog/' + self.category):
            os.makedirs('blog/' + self.category)

    @classmethod
    def get_category(cls, path_to_file):
        """Return the directory which contains path_to_file.

        Returns:
            str

        """

        directory_path = os.path.dirname(path_to_file)
        category = os.path.basename(directory_path)
        return category

    @classmethod
    def summarize(cls, soup):
        """Take BeautifulSoup and summarize the first paragraph.

        Returns:
            str:

        """

        first_paragraph = soup.find('p').get_text()

        if len(first_paragraph) > cls.SUMMARY_CHARACTER_LIMIT:
            return first_paragraph[:cls.SUMMARY_CHARACTER_LIMIT] + '&hellip;'
        else:
            return first_paragraph

    @staticmethod
    def get_href(category, file_path):
        """Path usable on both web server and for writing
        HTML locally.

        Arguments:
            category (str):
            file_path (str):

        """

        _, file_name_md = file_path.rsplit('/', 1)
        return os.path.join(
            'blog',
            category,
            os.path.splitext(file_name_md)[0] + '.html',
        )

    @staticmethod
    def get_date(file_path, getmtime_or_getctime):
        """

        getmtime_or_getctime (func): either os.path.getmtime,
            or os.path.getctime.

        """

        try:
            epoch_time = getmtime_or_getctime(file_path)
        except OSError:
            epoch_time = 0

        string_time = time.strftime(
            "%a, %d %b %Y %H:%M:%S +0000",
            time.gmtime(epoch_time)
        )
        return string_time, epoch_time

    @staticmethod
    def get_html(file_path):

        with open(file_path) as f:
            html_string = markdown.markdown(f.read())

        soup = BeautifulSoup(html_string, 'html.parser')
        title = soup.h1.extract().get_text()
        return soup, title

    def render(self):
        post_template = jinja_env.get_template(self.TEMPLATE)
        return post_template.render(post=self)


# Create the regular pages first
for template_name in jinja_env.list_templates():
    if template_name in ('base.html', 'category-index.html', Post.TEMPLATE):
        continue

    template = jinja_env.get_template(template_name)
    with open(template_name, 'w') as f:
        f.write(template.render())

# Create the blog by first creating all the individual
# posts, building an index of those posts..
list_of_all_posts_unsorted = []
categorized_posts = {}
search_path = os.path.join(MARKDOWN_SOURCE, '**/*.md')
for file_path in glob.iglob(search_path, recursive=True):
    # Create the post object and render/output
    post = Post(file_path)
    with open(post.href, 'w') as f:
        f.write(post.render())

    # File by category and add to list of all posts
    list_of_all_posts_unsorted.append(post)
    if post.category not in categorized_posts:
        categorized_posts[post.category] = [post]

    else:
        categorized_posts[post.category].append(post)

# create the category indexes
category_template = jinja_env.get_template('category-index.html')
for category, posts in categorized_posts.items():
    with open(os.path.join('blog', category, 'index.html'), 'w') as f:
        f.write(category_template.render(category=category, posts=posts))

# ... then sort said post list by their creation time
sorted_list_of_all_posts = sorted(
    list_of_all_posts_unsorted,
    key=lambda x: x.created_epoch,
    reverse=True,
)

# .. finally render the blog index
template = jinja_env.get_template('blog.html')
with open('blog.html', 'w') as f:
    f.write(template.render(posts=sorted_list_of_all_posts, categories=categorized_posts.keys()))
