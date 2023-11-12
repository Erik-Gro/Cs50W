from django.shortcuts import render
from django.shortcuts import redirect, reverse
import random 
import markdown2 

from . import util

def mdToHtml(blogName):
    page = util.get_entry(blogName)
    if page == None:
        return None
    else:
        return markdown2.markdown(page)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def errorPage(request,err):
    return render(request, "encyclopedia/error.html", {
        "err": f"Page {err} is not found"
    })


def showWikiBlog(request,blogName):
    blog = mdToHtml(blogName)
    if blog == None:
        return redirect(reverse('failure',kwargs={'err' : blogName}
    ))
    else:
        return render(request,"encyclopedia/wikiBlog.html",{
        "blogName": blogName,
        "currBlog": blog,
    })


def search(request):
    if request.method == "POST":
        entry = request.POST['q']
        blog = mdToHtml(entry)
        if blog is not None:
            return redirect(reverse('wikiBlog',kwargs={'blogName' : entry}
    ))
        else:
            entries = util.list_entries()
            matches = []
            array = ['q','a','b']
            for word in entries:
                if entry.lower() in word.lower():
                  matches.append(word)
            if len(matches) != 0:        
             
             return render(request,"encyclopedia/search.html",{
                        "matches": matches,
                        "len": f" number of pages that matches {entry} is {len(matches)} "
                    })
            else:
                return redirect(reverse('failure',kwargs={'err' : entry}
    ))


def createPage(request):
    if request.method =="GET":
     return render(request, "encyclopedia/createpage.html", {
    })
    else:
        title = request.POST['title']
        content = request.POST['content']   
        doesPageExist = util.get_entry(title)
        if  doesPageExist is not None:
          return render(request, "encyclopedia/error.html", {
        "err": f"Page {title} already is created"
    })
        else:
         util.save_entry(title, content)
        return redirect(reverse('wikiBlog',kwargs={'blogName': title}
    ))


def smth(request):
         listz = util.list_entries()
         blog = random.choice(listz)
         return redirect('wikiBlog', blogName= blog)

def edit(request):
    if request.method =="POST":
     blogName = request.POST['title']
     blogText = util.get_entry(blogName)
     return render(request,"encyclopedia/edit.html",{
        "blogName": blogName,
        "currBlog": blogText,
    })

def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content'] 
        util.save_entry(title, content)
        return redirect(reverse('wikiBlog',kwargs={'blogName': title}
    ))