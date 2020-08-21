from django.shortcuts import render
from django.shortcuts import redirect

import markdown
import random as rand
from . import util

md = markdown.Markdown()

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_content(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/404.html")
    else:
        return render(request, "encyclopedia/content.html", {
            "title": title.capitalize(),
            "content": markdown.markdown(content),
        })

def search_content(request):
    search_string = request.GET.get('q', '')
    all_entries = util.list_entries()
    if search_string in all_entries:
        return redirect(f"wiki/{search_string}")
    else:
        fuzzy_list = []
        for entry in all_entries:
            if search_string.lower() in entry.lower():
                fuzzy_list.append(entry)
        return render(request, "encyclopedia/results.html", {
            "entries": fuzzy_list
        })

def new_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newentry.html")
    else:
        new_title = request.POST.get('new_title', '')
        new_content = request.POST.get('new_content', '')

        if util.get_entry(new_title):   # check if there is existing Entry
            return render(request, "encyclopedia/newentry.html", {
                "error": "There is a duplicate entry, please try again"
            })
        elif new_title == "":
            return render(request, "encyclopedia/newentry.html", {
                "error": "Title cannot be empty, please try again"
            })
        else:
            util.save_entry(new_title, new_content)
            return redirect(f"/wiki/{new_title}")

def edit(request, entry_title):
    wiki_content = util.get_entry(entry_title)
    if request.method == "GET":
        return render(request, "encyclopedia/editentry.html", {
            "wiki_title": entry_title,
            "wiki_content": wiki_content
        })
    elif request.method == "POST":
        new_content = request.POST.get('edited_content', '')
        util.save_entry(entry_title, new_content)
        return redirect(f"/wiki/{entry_title}")

def get_random_entry(request):
    random_entry = rand.choice(util.list_entries())
    return redirect(f"/wiki/{random_entry}")
