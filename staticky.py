"""Quick-and-dirty static site generator using
jinja & markdown for lillian.link.

I really just made this for fun.

Works exclusively in Python3.

"""

import time
import os
import glob
from collections import namedtuple

import jinja2
from bs4 import BeautifulSoup
import markdown


jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader('_src', 'templates')
)


class Post(object):
    """A blog post; make templating much easier.

    Constants:
        SUMMARY_LENGTH (int): --
        MARKDOWN_SOURCE (str): --

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

    SUMMARY_LENGTH = 100
    MARKDOWN_SOURCE = '_src/markdown_blog/'
    POST_TEMPLATE = 'blog-article.html'

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

        category = file_path.replace(
            cls.MARKDOWN_SOURCE, '', 1
        ).split('/', 1)[0]
        return category

    @classmethod
    def summarize(cls, soup):
        """Take BeautifulSoup and summarize the first paragraph.

        Returns:
            str:

        """

        first_paragraph = soup.find('p').get_text()

        if len(first_paragraph) > cls.SUMMARY_LENGTH:
            return first_paragraph[:self.SUMMARY_LENGTH] + '&hellip;'
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
        post_template = jinja_env.get_template(self.POST_TEMPLATE)
        return post_template.render(post=self)


# Create the regular pages first
for template_name in jinja_env.list_templates():

    if template_name in ('base.html', 'blog-article.html'):
        continue

    template = jinja_env.get_template(template_name)

    with open(template_name, 'w') as f:
        f.write(template.render())

# Create the blog
posts_for_index_unsorted = []

for file_path in glob.iglob('_src/markdown_blog/**/*.md', recursive=True):
    post = Post(file_path)
    with open(post.href, 'w') as f:
        f.write(post.render())
    posts_for_index_unsorted.append(post)

# TODO: .. sort the blog posts by created date
posts_sorted = sorted(
    posts_for_index_unsorted,
    key=lambda x: x.created_epoch
)

# .. finally render the blog index
template = jinja_env.get_template('blog.html')
with open('blog.html', 'w') as f:
    f.write(template.render(posts=posts_sorted))
