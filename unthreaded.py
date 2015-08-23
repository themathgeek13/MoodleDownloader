import mechanize
import cookielib
import os
import threading
import getpass

course_list=['EE2001', 'EE2002', 'ID1200', 'AM1100', 'BT1010', 'EE2701', 'HS3410', 'MA2010']

def process(course):
    br=browser(user, pwd);
    print 'Connected one browser instance.'
    br2=browser(user, pwd);
    print 'Connected second browser instance.'
    
    link=''; count=0;
    if not os.path.exists('/home/rohan/Moodle/'+course):
        os.makedirs('/home/rohan/Moodle/'+course)

    os.chdir('/home/rohan/Moodle/'+course)
    for item in br.links():
        if course+':' in str(item):
            link=item.url
            
    br2.open(link)
    resources=[]
    for i in br2.links():
        if 'resource' in str(i):
            resources.append(i)
            
    for filename in resources:
        count+=1
        os.chdir('/home/rohan/Moodle/'+course)
        t=''.join(filename.text.split()).split('[IMG]')[1]
        try:
            br2.retrieve(filename.url, t+'.pdf')[0]
        except:
            br2.retrieve(filename.url, course+'_'+str(count)+'.pdf')[0]

def browser(user='ee14b118', pwd='default'):
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent Headers
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # Open Login Page and login using browser
    br.open("https://courses.iitm.ac.in/login/index.php")
    br.select_form(nr=0)
    br.form['username']=user
    br.form['password']=pwd
    br.submit()

    return br


user=raw_input('Enter your username:')
pwd=getpass.getpass('Enter your password:')
thread_list=[]; pdfs=[]; link=''

if not os.path.exists('/home/rohan/Moodle'):
    os.makedirs('/home/rohan/Moodle')

for course in course_list:
    process(course)
    print course_list.index(course)+1
