<!-- 
.. link: 
.. description: a passionate tale of a daring rescue from a burning house 
.. tags: meta
.. date: 2013/05/10 14:36:19
.. title: Home sweet home
.. slug: home-sweet-home
-->

Since Posterous is going away real soon now, I needed to migrate my
old site from pseudo.posterous.com.  Well, 'need' is of course a
relative term, but the old site did have some posts on using ClueWeb
and HBase which some folks might still find useful.

It's nice that Posterous provided a way to bundle and download your
blog, but I decided to declare my independence (well, mostly) and move
the blog to a github pages site.  This way, the blog itself is
maintained in a git repository, and I can edit and push changes from
the command line.

After reading [this
post][http://jakevdp.github.io/blog/2013/05/07/migrating-from-octopress-to-pelican/]
I spent some time reading up on static page generators and, after
playing with Jekyll-bootstrap and recoiling from its Ruby-ness (sorry, it's
just me), I settled on [Nikola][http://nikola.ralsina.com.ar/], which
is implemented in Python, a language I already speak.

A Posterous dump comes down basically in WordPress format, and Nikola
can import that.  The
[instructions][http://nikola.ralsina.com.ar/handbook.html#importing-your-wordpress-site-into-nikola]
on that couldn't be simpler.

To work with github, I followed some advice from [this
thread][https://groups.google.com/forum/#!topic/nikola-discuss/aDbsPtu4pNc].
I created a branch called 'src', and in that branch set up a
virtualenv with Nikola and all the parts it wanted.  I then ported my
site, which created a directory 'new_site'.  'nikola build' went fine
after chasing down yet more Python packages for dates and Markdown.  I
then made a new clone of the git repository, copied the contents
of the 'output' directory, and committed that to the master branch.
Voila, everything in git and github.

This is really just a test post to see that everything's working.  If
it is, you can [see my
conf.py][https://github.com/isoboroff/isoboroff.github.com/blob/src/new_site/conf.py]
which shows how its done.
