from random import choice
from django.shortcuts import render
from markdown2 import Markdown
from . import util
from . import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import re

app_name = "encyclopedia"

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": forms.NewSearchFrom(),
        "deleteFlag": False
    })
    
def entry(request, title):
    markdowner = Markdown()
        
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
            "message": f"{title} cannot be found",
            "form": forms.NewSearchFrom()
        })
    
    entry = markdowner.convert(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry,
        "form": forms.NewSearchFrom(),
    })

def search(request):  
    if request.method == "POST":
        form = forms.NewSearchFrom(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"].lower()
            entries = util.list_entries()
            
            if util.get_entry(query):
                return HttpResponseRedirect(reverse("entry", kwargs={'title': query}))
                
            else:
                matches = [entry for entry in entries if re.search(query, entry, re.IGNORECASE)]
                return render(request, "encyclopedia/search.html", {
                    "matches": matches,
                    "form": forms.NewSearchFrom()
                })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": forms.NewSearchFrom()
            })
            
    return render(request, "encyclopedia/error.html", {
        "message": "Please search for something",
        "form": forms.NewSearchFrom()        
    })

def new(request):
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "message": "Sorry, the new entry you are trying to save already exists, please provide a unique entry."
                })
                
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/new.html", {
            "form" : forms.NewSearchFrom(),
            "entryForm": forms.NewEntryForm()
        })
            
    return render(request, "encyclopedia/new.html", {
        "form" : forms.NewSearchFrom(),
        "entryForm": forms.NewEntryForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = forms.NewEditForm(request.POST)
        
        if form.is_valid:
            editedContent = form.data["editedContent"]
            
            util.save_entry(title, editedContent)
            markdowner = Markdown()
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdowner.convert(editedContent),
                "form": forms.NewSearchFrom(),
                "editFlag": True
            })
        else:
            pass
        
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
                    "message": "Sorry, the entry you are trying to edit does not exist."
                })

    form = forms.NewEditForm()
    form.fields["editedContent"].initial = content
    return render(request, "encyclopedia/edit.html", {
        'title': title,
        'editForm': form
    })
    
def delete(request, title):
    if request.method == "POST":
        util.delete_entry(title)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": forms.NewSearchFrom(),
            "deleteFlag": True,
            "deletedTitle" : title
        })
    
    return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

def random(request):
    entries = util.list_entries()
    randomTitle = choice(entries)
    
    return HttpResponseRedirect(reverse("entry", kwargs={'title': randomTitle}))
