
import settings

def configure_gitmarks():

	print """
	Wecome to gitmarks configurator. This will setup a couple of local
	repositories for you to use as yor gitmarks system.	 Gitmarks will
	maintain 2-3 repositories.
	 - 1 for public use (world+dog read)
	 - 1 for friends use (with some encryption)
	 - 1 (optional) for content. This can be non-repo, or nonexistant 
	 
	 """
	ret = getYesNoFromUser("Ready to start?",'Y')
	if ret is None:
		print "invalid choice"
		return
	elif ret is False:
		print "Goodbye! Share and Enjoy."
		return

	base_dir = getStringFromUser('At what base directories do you want your repos?',
	settings.GITMARK_BASE_DIR)
	
	get_content= getYesNoFromUser('do you want to pull down the content of a page when you download a bookmark?', settings.GET_CONTENT)
	
	content_cache_mb = getIntFromUser('do you want to set a maximum MB of content cache?', settings.CONTENT_CACHE_SIZE_MB)
	
	remote_pub_repo = getStringFromUser('Specify a remote git repository for your public bookmarks',settings.REMOTE_PUB_REPO)

	remote_private_repo = getStringFromUser('Specify a remote git repository for your private bookmarks?',settings.REMOTE_PRIVATE_REPO)
	
	remote_content_repo = None
	content_as_reop= getYesNoFromUser('do you want your content folder to be stored as a repository?',settings.CONTENT_AS_REPO)
	
	if content_as_reop is True:
		remote_content_repo = getStringFromUser('what is the git repository for your content?', settings.REMOTE_CONTENT_REPO)

	fav_color= getStringFromUser('what is your favorite color?',settings.FAVORITE_COLOR)

	wv_u_swallow = getStringFromUser('what is the windspeed velocity of an unladen swallow?',settings.UNLADEN_SWALLOW_GUESS)

	dict = { 'GITMARK_BASE_DIR':base_dir, 'GET_CONTENT':get_content,
	'CONTENT_CACHE_SIZE_MB':content_cache_mb,
	'CONTENT_AS_REPO':content_as_reop,
	'REMOTE_PUB_REPO':remote_pub_repo, 'REMOTE_PRIVATE_REPO': remote_private_repo,
	'SAVE_CONTENT_TO_REPO':content_as_reop, 'REMOTE_CONTENT_REPO':remote_content_repo,
	'FAVORITE_COLOR':fav_color, 'UNLADEN_SWALLOW_GUESS':wv_u_swallow,
	"PUBLIC_GITMARK_REPO_DIR":settings.PUBLIC_GITMARK_REPO_DIR,
	'PRIVATE_GITMARK_REPO_DIR':settings.PRIVATE_GITMARK_REPO_DIR,
	'CONTENT_GITHUB_DIR':settings.CONTENT_GITHUB_DIR, 'BOOKMARK_SUB_PATH':settings.BOOKMARK_SUB_PATH,
	'TAG_SUB_PATH':settings.TAG_SUB_PATH, 'MSG_SUB_PATH':settings.MSG_SUB_PATH,
	'CONTENT_SUB_PATH':settings.CONTENT_SUB_PATH}

	print dict	
	
	#add REMOTE_PUB_REPO, REMOTE_PRIVATE_REPO, SAVE_CONTENT_TO_REPO, REMOTE_CONTENT_REPO
	#add FAVORITE_COLOR UNLADEN_SWALLOW_GUESS, CONTENT_CACHE_SIZE_MB
	




def getIntFromUser(message, value=''):
	msg2 = ' '.join([message,' (',str(value),') (int): ']) 
	value = raw_input(msg2)
	try:
		return int(value)
	except:
		print "int decoe fail for %s" %value
	return None

def getStringFromUser(message,value=''):
	msg2 = ''.join([message,' (',str(value),') (string): ']) 
	value = raw_input(msg2)
	return value
	
def getYesNoFromUser(message,value=''):
	msg2 = ''.join([message,' (',str(value),') (Y,n): ']) 
	value = raw_input(msg2)
	
	if(value == 'Y' or value == 'Yes' or value == 'y'):
		return True
	elif(value == 'n' or value == 'no' or value == 'N'):
		return False
	return None
	
if __name__ == '__main__':
	configure_gitmarks()	