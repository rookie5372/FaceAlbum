import web
from web import form
import urllib2
import os
import all_search
from all_search import *
import envir
urls = (
    '/', 'index',
    '/img','image1',
    '/s', 's',
    '/i','image',
    '/l','l_r',
)

piclist =[]
render = web.template.render('search_item/') # your templates

login = form.Form(
    form.Textbox('keyword'),
    form.Button('Search'),
)

class index:
    def GET(self):
        f = login()
        return render.homepage(f)

class image1:
    def GET(self):
        f = login()
        return render.img(f)    
class s:
    def GET(self):
        global piclist
        user_data = web.input()
        if user_data.keyword:
            piclist,s = all_search.text_search(user_data.keyword)
        return render.picresult(s,user_data.keyword,piclist,login)

class image:
    def POST(self):
        x = web.input(myfile={})

        filedir = '' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created

            # filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filepath = x.myfile.filename
            if filepath[-3:] != 'jpg':
                return render.upload('') # putout errorinformation
            
            print filepath

            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open('static/test.jpg','wb')
            # fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored

            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.

        # x.myfile.file.read()
        # fout =open('test.jpg','wb')
        # fout.write(x.myfile.file.read())
        # fout.close()
        filepath ='static/test.jpg'
        global piclist
        c,d = all_search.img_search(filepath)
        piclist = []
        n1 = len(c)
        n2 = len(d)
        if n1>n2:
            for i in range(n2):
                piclist.append(c[i])
                piclist.append(d[i])
            for i in range(n2,n1):
                piclist.append(c[i])
        elif n2>n1:
            for i in range(n1):
                piclist.append(c[i])
                piclist.append(d[i])
            for i in range(n1,n2):
                piclist.append(d[i])
        else:
            for i in range(n1):
                piclist.append(c[i])
                piclist.append(d[i])    
        return render.pictopicresult(piclist,login)

class l_r:
    def GET(self):
        global piclist
        user_data = web.input()
        if user_data.picname:
            print user_data.picname
            print type(user_data.picname)
            print type(urltolabeldict.keys()[0])
            picnamestr= str(user_data.picname)
            i = 0
            n = 0
            for x in piclist:
                if x==user_data.picname:
                    n=i
                else:
                    i=i+1
            if (picnamestr in urltolabeldict.keys()):
                a=urltolabeldict[picnamestr]
                return render.left_right(piclist,n,a,login)
            else:      
                return render.left_right(piclist,n,'',login)

    
if __name__ == "__main__":
    app = web.application(urls, globals()) 
    app.run()
