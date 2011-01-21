#!/usr/bin/env python
# encoding: utf-8
"""
delicious_import.py

Created by Hilary Mason on 2010-11-28.
Copyright (c) 2010 Hilary Mason. All rights reserved.
"""

import sys, os
import urllib
from xml.dom import minidom
from xml.parsers import expat
from optparse import OptionParser

from gitmark import gitMarkImporter


def import_delicious_to_local_git(username, password='', url=None):
    """ imports a delicious file to the local git system. If url is not set
    a delicious API url is generated. if url is set (for a file, for example) that file is imported."""
#    if not url:
#        # API URL: https://user:passwd@api.del.icio.us/v1/posts/all
#        url = "https://%s:%s@api.del.icio.us/v1/posts/all" % (username, password)
#    h = urllib.urlopen(url)
#    content = h.read()
#    h.close()
#    #--enable these to cache a copy of the file to test using
#    #h = open('cache.htm', 'w')
#    #h.write(content)
#    #h.close()
# 
# 
#    # check for signs of a yahoo error page, with causes minidom to flip out
#    if( len(content) >=6 and content[:5] == '<!-- ' ):
#        print content
#        print "yahoo error, no data fetched "
#        return
#    
#    try:
#        x = minidom.parseString(content)
#    except expat.ExpatError, e:
#        print content
#        print "== Above content caused minidom to flipped out %s " % (e)
#        return
#        
#    # sample post: <post href="http://www.pixelbeat.org/cmdline.html" hash="e3ac1d1e4403d077ee7e65f62a55c406" description="Linux Commands - A practical reference" tag="linux tutorial reference" time="2010-11-29T01:07:35Z" extended="" meta="c79362665abb0303d577b6b9aa341599" />
#    
#    post_list = x.getElementsByTagName('post')
#    
#    for post_index, post in enumerate(post_list):
#    
#        try:
#            url = post.getAttribute('href')
#            desc = post.getAttribute('description')
#            timestamp = post.getAttribute('time')
#            raw_tags  = post.getAttribute('tag')
#            extended =  post.getAttribute('extended')
#            meta     =  post.getAttribute('meta')
#            # turn a comma separated list of tags into a real list of tags
#            tags = ",".join([tag for tag in raw_tags.split()])
# 
#            #build our post data into an options list
#            options = {'tags': tags, 'push':False, 'msg':desc, "lazyAdd":True}            

#            # turn a comma separated list of tags into a real list of tags            
#            # TRICKY: Set the authoring date of the commit based on the imported
#            # timestamp. git reads the GIT_AUTHOR_DATE environment var.
#            os.environ['GIT_AUTHOR_DATE'] = timestamp
#    
#            args = [url]
#            g = gitMarkImporter(options, args)
#            
#            # TRICKY:  Reset authoring timestamp (abundance of caution)
#            del os.environ['GIT_AUTHOR_DATE']
#            
#            if post_list.length > 1:
#                print '%d of %d bookmarks imported (%d%%)' % (
#                    post_index + 1, post_list.length,
#                    (post_index + 1.0) / post_list.length * 100)
#        except (KeyboardInterrupt, SystemExit):
#            print >>sys.stderr, ("backup interrupted by KeyboardInterrupt/SystemExit" )
#            return 
            
if __name__ == '__main__':
 
    usage =  "Usage: python delicious_import.py cached-page-uri\nOR\nUsage: python delicious_import.py username password"

    if( len(sys.argv) == 2): 
            import_delicious_to_local_git(username=None, password=None, url=sys.argv[1])
    elif(len(sys.argv) == 3):
        try:
            (username, password) = sys.argv[1:]
        except ValueError:
            print usage
        import_delicious_to_local_git(username=username, password=password)
    else:
        print usage
 
