#!/usr/bin/env python
# encoding: utf-8
"""
gitmark.py

Created by Hilary Mason on 2010-09-24.
Copyright (c) 2010 Hilary Mason. All rights reserved.
"""

import sys, os
import urllib, httplib
import re
import hashlib
import csv
import subprocess
import time
from optparse import OptionParser

from settings import *

# Arguments are passed directly to git, not through the shell, to avoid the
# need for shell escaping. On Windows, however, commands need to go through the
# shell for git to be found on the PATH, but escaping is automatic there. So
# send git commands through the shell on Windows, and directly everywhere else.
USE_SHELL = os.name == 'nt'

class gitMark(object):
	""" Object representing a bookmark stored as a git object """
	def __init__(self, options, args):

		modified = [] # track files we need to add - a hack, because it will add files that are already tracked by git
		url = args[0].strip('/')
		
		content_filename = self.generateHash(url)

		if ( os.path.isfile('/'.join(["content",content_filename]))	 and options['lazyAdd'] == True ):
				print "file exists in repo, lazyAdd is true, skipping add"
				return
		print url
		content = self.getContent(url)
		title = self.parseTitle(content)
		
		modified.append(self.saveContent(content_filename, content))
		tags = ['all']
		tags.extend(options['tags'].split(','))
		for tag in tags:
			t = tag.strip()
			if not t:
				continue
			if '/' in t:
				t = ''.join(t.split('/'))
			modified.append(self.saveTagData(t, url, title, content_filename))
			
		self.gitAdd(modified)
		
		commit_msg = options['msg']
		if not commit_msg:
			commit_msg = 'adding %s' % url
		
		self.gitCommit(commit_msg)
		
		if options['push']:
			self.gitPush()


	@classmethod
	def gitAdd(cls, files):
		""" add this git object's files to the local repository"""
		subprocess.call(['git', 'add'] + files, shell=USE_SHELL)
		
	@classmethod
	def gitCommit(cls, msg):
		""" commit the local repository to the server"""
		subprocess.call(['git', 'commit', '-m', msg], shell=USE_SHELL)
		
	@classmethod
	def gitPush(cls):
		""" push the local origin to the master"""
		pipe = subprocess.Popen("git push origin master", shell=True)
		pipe.wait()
	
	@classmethod
	def saveContent(cls, filename, content):
		f = open('%s%s' % (CONTENT_PATH, filename), 'w')
		f.write(content)
		f.close()
		return '%s%s' % (CONTENT_PATH, filename)
		
	@classmethod
	def saveTagData(cls, tag, url, title, content_filename):
		tag_writer = csv.writer(open('%s%s' % (TAG_PATH, tag), 'a'))
		tag_writer.writerow([url, title, content_filename])
		return '%s%s' % (TAG_PATH, tag)

	@classmethod
	def parseTitle(cls, content):
		re_htmltitle = re.compile(".*<title>(.*)</title>.*")
		t = re_htmltitle.search(content)
		try:
			title = t.group(1)
		except AttributeError:
			title = '[No Title]'
		
		return title
		
	@classmethod
	def generateHash(cls, text):
		m = hashlib.md5()
		m.update(text)
		return m.hexdigest()
		
	@classmethod
	def getContent(cls, url):
		try:
			h = urllib.urlopen(url)
			content = h.read()
			h.close()
			h = urllib.urlopen(url)
		except IOError, e:
			print >>sys.stderr, ("Error: could not retrieve the content of a"
				" URL. The bookmark will be saved, but its content won't be"
				" searchable. URL: <%s>. Error: %s" % (url, e))
			content = ''
		except httplib.InvalidURL, e: #case: a redirect is giving me www.idealist.org:, which causes a fail during port-number search due to trailing :
			print >>sys.stderr, ("Error: url or url redirect contained an"
			"invalid  URL. The bookmark will be saved, but its content"
			"won't be searchable. URL: <%s>. Error: %s" % (url, e))
			content=''
		return content


if __name__ == '__main__':

	parser = OptionParser("usage: %prog [options]")
	parser.add_option("-p", "--push", dest="push", action="store_true", default=False, help="don't push to origin.")
	parser.add_option("-t", "--tags", dest="tags", action="store", default='notag', help="comma seperated list of tags")
	parser.add_option("-m", "--message", dest="msg", action="store", default=None, help="specify a commit message (default is 'adding [url]')")
	(options, args) = parser.parse_args()
	
	opts = {'push': options.push, 'tags': options.tags, 'msg': options.msg}
	
	g = gitMark(opts, args)
