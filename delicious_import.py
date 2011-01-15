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

from gitmark import gitMark

def import_delicious_to_local_git(username, password=''):
	# API URL: https://user:passwd@api.del.icio.us/v1/posts/all
	url = "https://%s:%s@api.del.icio.us/v1/posts/all" % (username, password)
	h = urllib.urlopen(url)
	content = h.read()
	h.close()

	# check for signs of a yahoo error page, with causes minidom to flip out
	if(len(content) >=6 and content[:5] == '<!-- ' or 
		content[-4:] == " -->"):
		print content
		print "yahoo error, no data fetched "
		return
	
	try:
		x = minidom.parseString(content)
	except expat.ExpatError, e:
		print content
		print "== Above content caused minidom to flipped out %s " % (e)
		return
		
	# sample post: <post href="http://www.pixelbeat.org/cmdline.html" hash="e3ac1d1e4403d077ee7e65f62a55c406" description="Linux Commands - A practical reference" tag="linux tutorial reference" time="2010-11-29T01:07:35Z" extended="" meta="c79362665abb0303d577b6b9aa341599" />
	
	post_list = x.getElementsByTagName('post')
	
	for post_index, post in enumerate(post_list):
	
		try:
			url = post.getAttribute('href')
			desc = post.getAttribute('description')
			# turn a comma separated list of tags into a real list of tags
			tags = ",".join([t for t in post.getAttribute('tag').split()])
			timestamp = post.getAttribute('time')		
			options = {'tags': tags, 'push':False, 'msg':desc, "lazyAdd":True}
			
			# Set the authoring date of the commit based on the imported
			# timestamp. git reads the GIT_AUTHOR_DATE environment var.
			os.environ['GIT_AUTHOR_DATE'] = timestamp
	
			args = [url]
			g = gitMark(options, args)
			
			# Reset authoring timestamp (abundance of caution)
			del os.environ['GIT_AUTHOR_DATE']
			
			if post_list.length > 1:
				print '%d of %d bookmarks imported (%d%%)' % (
					post_index + 1, post_list.length,
					(post_index + 1.0) / post_list.length * 100)
		except (KeyboardInterrupt, SystemExit):
			print >>sys.stderr, ("backup interrupted by KeyboardInterrupt/SystemExit" )
			return 
			
if __name__ == '__main__':
	try:
		(username, password) = sys.argv[1:]
	except ValueError:
		print "Usage: python delicious_import.py username password"
			
	import_delicious_to_local_git(username, password)

