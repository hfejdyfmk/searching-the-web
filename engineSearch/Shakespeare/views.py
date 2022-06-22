import csv, os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader

from .models import Work, Category

import logging
logger = logging.getLogger("mylogger")


def index(request):
    categories = Category.objects.all()
    context = {  # target of template
        'category_list': categories,
    }
    return render(request, 'Shakespeare/index.html', context)


def detail(request, pk):
    work = Work.objects.get(pk=pk)
    path = os.path.join('./Shakespeare/.data', work.work_fname)
    with open(path, 'r') as f:
        lines = f.readlines()
    context = {
        'content': "".join(lines)
    }
    return render(request, 'Shakespeare/detail.html', context)


def results(request):
    term_by_document = {}
    with open("./.tmp/term_by_document.csv", 'r') as f:
        rows = csv.DictReader(f)
        for row in rows:
            term_by_document.setdefault(row['term'], []).append(row['document'])

    def operation(set1, set2, op):
        if op == 'OR':
            return set1 | set2
        return set1 & set2  # case: operation == 'AND'

    def query(operations):
        operations = operations.lower().split()
        stack = []
        for ch in operations:
            if ch == ')':
                ch = stack.pop()
                if isinstance(ch, str):
                    ch = set("".join(term_by_document.get(ch, set())).split(','))
                operator = stack.pop()
                if operator != '(': # either '(' or a operator (AND, OR)
                    set2 = stack.pop()
                    if isinstance(set2, str):
                        set2 = set("".join(term_by_document.get(set2, set())).split(','))
                    stack.pop()  # '('
                    ch = operation(ch, set2, operator.upper())
            stack.append(ch)
        return list(stack[0]) or -1  # -1 if not found
    documents = query(request.POST['keywords'])
    works = Work.objects.filter(work_fname__in=documents)
    context = {
        'work_list': works,
    }
    return render(request, 'Shakespeare/results.html', context) if works else HttpResponse("No result")
