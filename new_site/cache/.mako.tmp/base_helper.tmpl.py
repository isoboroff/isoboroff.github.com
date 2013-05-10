# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1368211930.059505
_enable_loop = True
_template_filename = u'/Users/soboroff/isoboroff.github.com/lib/python2.7/site-packages/nikola/data/themes/default/templates/base_helper.tmpl'
_template_uri = u'base_helper.tmpl'
_source_encoding = 'utf-8'
_exports = ['html_head', 'html_sidebar_links', 'late_load_js', 'html_social', 'html_translations']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 49
        __M_writer(u'\n\n')
        # SOURCE LINE 70
        __M_writer(u'\n\n')
        # SOURCE LINE 86
        __M_writer(u'\n\n\n')
        # SOURCE LINE 97
        __M_writer(u'\n\n\n')
        # SOURCE LINE 106
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_head(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        favicons = context.get('favicons', UNDEFINED)
        description = context.get('description', UNDEFINED)
        title = context.get('title', UNDEFINED)
        use_cdn = context.get('use_cdn', UNDEFINED)
        translations = context.get('translations', UNDEFINED)
        blog_author = context.get('blog_author', UNDEFINED)
        mathjax_config = context.get('mathjax_config', UNDEFINED)
        rss_link = context.get('rss_link', UNDEFINED)
        has_custom_css = context.get('has_custom_css', UNDEFINED)
        len = context.get('len', UNDEFINED)
        _link = context.get('_link', UNDEFINED)
        use_bundles = context.get('use_bundles', UNDEFINED)
        blog_title = context.get('blog_title', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n    <meta charset="utf-8">\n    <meta name="description" content="')
        # SOURCE LINE 4
        __M_writer(unicode(description))
        __M_writer(u'" >\n    <meta name="author" content="')
        # SOURCE LINE 5
        __M_writer(unicode(blog_author))
        __M_writer(u'">\n    <title>')
        # SOURCE LINE 6
        __M_writer(unicode(title))
        __M_writer(u' | ')
        __M_writer(unicode(blog_title))
        __M_writer(u'</title>\n    ')
        # SOURCE LINE 7
        __M_writer(unicode(mathjax_config))
        __M_writer(u'\n')
        # SOURCE LINE 8
        if use_bundles:
            # SOURCE LINE 9
            if use_cdn:
                # SOURCE LINE 10
                __M_writer(u'            <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/css/bootstrap-combined.min.css" rel="stylesheet">\n            <link href="/assets/css/all.css" rel="stylesheet" type="text/css">\n')
                # SOURCE LINE 12
            else:
                # SOURCE LINE 13
                __M_writer(u'            <link href="/assets/css/all-nocdn.css" rel="stylesheet" type="text/css">\n')
            # SOURCE LINE 15
        else:
            # SOURCE LINE 16
            if use_cdn:
                # SOURCE LINE 17
                __M_writer(u'            <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/css/bootstrap-combined.min.css" rel="stylesheet">\n')
                # SOURCE LINE 18
            else:
                # SOURCE LINE 19
                __M_writer(u'            <link href="/assets/css/bootstrap.min.css" rel="stylesheet" type="text/css">\n            <link href="/assets/css/bootstrap-responsive.min.css" rel="stylesheet" type="text/css">\n')
            # SOURCE LINE 22
            __M_writer(u'        <link href="/assets/css/rst.css" rel="stylesheet" type="text/css">\n        <link href="/assets/css/code.css" rel="stylesheet" type="text/css">\n        <link href="/assets/css/colorbox.css" rel="stylesheet" type="text/css"/>\n        <link href="/assets/css/theme.css" rel="stylesheet" type="text/css"/>\n')
            # SOURCE LINE 26
            if has_custom_css:
                # SOURCE LINE 27
                __M_writer(u'            <link href="/assets/css/custom.css" rel="stylesheet" type="text/css">\n')
        # SOURCE LINE 30
        __M_writer(u'    <!--[if lt IE 9]>\n      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js" type="text/javascript"></script>\n    <![endif]-->\n')
        # SOURCE LINE 33
        if rss_link:
            # SOURCE LINE 34
            __M_writer(u'        ')
            __M_writer(unicode(rss_link))
            __M_writer(u'\n')
            # SOURCE LINE 35
        else:
            # SOURCE LINE 36
            if len(translations) > 1:
                # SOURCE LINE 37
                for language in translations:
                    # SOURCE LINE 38
                    __M_writer(u'                <link rel="alternate" type="application/rss+xml" title="RSS (')
                    __M_writer(unicode(language))
                    __M_writer(u')" href="')
                    __M_writer(unicode(_link('rss', None, language)))
                    __M_writer(u'">\n')
                # SOURCE LINE 40
            else:
                # SOURCE LINE 41
                __M_writer(u'            <link rel="alternate" type="application/rss+xml" title="RSS" href="')
                __M_writer(unicode(_link('rss', None)))
                __M_writer(u'">\n')
        # SOURCE LINE 44
        if favicons:
            # SOURCE LINE 45
            for name, file, size in favicons:
                # SOURCE LINE 46
                __M_writer(u'            <link rel="')
                __M_writer(unicode(name))
                __M_writer(u'" href="')
                __M_writer(unicode(file))
                __M_writer(u'" sizes="')
                __M_writer(unicode(size))
                __M_writer(u'"/>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_sidebar_links(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        lang = context.get('lang', UNDEFINED)
        rel_link = context.get('rel_link', UNDEFINED)
        permalink = context.get('permalink', UNDEFINED)
        sidebar_links = context.get('sidebar_links', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 89
        __M_writer(u'\n')
        # SOURCE LINE 90
        for url, text in sidebar_links[lang]:
            # SOURCE LINE 91
            if rel_link(permalink, url) == "#":
                # SOURCE LINE 92
                __M_writer(u'            <li class="active"><a href="')
                __M_writer(unicode(url))
                __M_writer(u'">')
                __M_writer(unicode(text))
                __M_writer(u'</a>\n')
                # SOURCE LINE 93
            else:
                # SOURCE LINE 94
                __M_writer(u'            <li><a href="')
                __M_writer(unicode(url))
                __M_writer(u'">')
                __M_writer(unicode(text))
                __M_writer(u'</a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_late_load_js(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        use_cdn = context.get('use_cdn', UNDEFINED)
        use_bundles = context.get('use_bundles', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 51
        __M_writer(u'\n')
        # SOURCE LINE 52
        if use_bundles:
            # SOURCE LINE 53
            if use_cdn:
                # SOURCE LINE 54
                __M_writer(u'            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>\n            <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/js/bootstrap.min.js"></script>\n            <script src="/assets/js/all.js" type="text/javascript"></script>\n')
                # SOURCE LINE 57
            else:
                # SOURCE LINE 58
                __M_writer(u'            <script src="/assets/js/all-nocdn.js" type="text/javascript"></script>\n')
            # SOURCE LINE 60
        else:
            # SOURCE LINE 61
            if use_cdn:
                # SOURCE LINE 62
                __M_writer(u'            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>\n            <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/js/bootstrap.min.js"></script>\n')
                # SOURCE LINE 64
            else:
                # SOURCE LINE 65
                __M_writer(u'            <script src="/assets/js/jquery-1.7.2.min.js" type="text/javascript"></script>\n            <script src="/assets/js/bootstrap.min.js" type="text/javascript"></script>\n')
            # SOURCE LINE 68
            __M_writer(u'        <script src="/assets/js/jquery.colorbox-min.js" type="text/javascript"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_social(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        add_this_buttons = context.get('add_this_buttons', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 72
        __M_writer(u'\n')
        # SOURCE LINE 73
        if add_this_buttons:
            # SOURCE LINE 74
            __M_writer(u'    <!-- Social buttons -->\n    <div id="addthisbox" class="addthis_toolbox addthis_peekaboo_style addthis_default_style addthis_label_style addthis_32x32_style">\n    <a class="addthis_button_more">Share</a>\n    <ul><li><a class="addthis_button_facebook"></a>\n    <li><a class="addthis_button_google_plusone_share"></a>\n    <li><a class="addthis_button_linkedin"></a>\n    <li><a class="addthis_button_twitter"></a>\n    </ul>\n    </div>\n    <script type="text/javascript" src="http://s7.addthis.com/js/300/addthis_widget.js#pubid=ra-4f7088a56bb93798"></script>\n    <!-- End of social buttons -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_html_translations(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        lang = context.get('lang', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        translations = context.get('translations', UNDEFINED)
        _link = context.get('_link', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 100
        __M_writer(u'\n')
        # SOURCE LINE 101
        for langname in translations.keys():
            # SOURCE LINE 102
            if langname != lang:
                # SOURCE LINE 103
                __M_writer(u'            <a href="')
                __M_writer(unicode(_link("index", None, langname)))
                __M_writer(u'">')
                __M_writer(unicode(messages("LANGUAGE", langname)))
                __M_writer(u'</a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


