from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Module
from .forms import ModuleForm

from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'mypython/index.html')

def conda(request):
    return render(request, 'mypython/conda.html')

def ddns(request):
    return render(request, 'mypython/ddns.html')

# @permission_required('module.can_modify_module')
@login_required
def module_create(request):
    # submitted = False
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.added_by = request.user
            module.save()
            # form.save()
            # next = request.POST.get('next', '/')
            # return HttpResponseRedirect(next)
            return redirect('mypython:module_draft_list')
            # return HttpResponse('<script>history.back();</script>')
    else:
        form = ModuleForm()
        # form = ModuleForm(initial={'type': 'Python'})
        # if 'submitted' in request.GET:
        #     submitted = True

    return render(request, 'mypython/module_form.html', {'form':form})

class ModuleListView(ListView):
    model = Module
    # The default value for contxt_object_name is model's name in lower case + "_list"
    # In this case, the default name is module_list
    # The default template name for ListView is module_list.html.
    context_object_name = 'all_modules'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q1', '')
        object_list = Module.objects.filter(
            Q(published_date__lte=timezone.now()) &
            (Q(title__icontains=query) | Q(type__icontains=query))
        ).order_by('title')

        return object_list

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['published'] = True
    #     return context

class ModuleDetailView(DetailView):
    model = Module
    context_object_name = 'module'
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'
    # template_name = "module_detail.html" # Default value, can be omitted!

class ModuleCreateView(PermissionRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    permission_required = "mypython.can_publish_module"
    # fields = '__all__'
    # fields = ['title', 'type', 'reference', 'description']
    # initial = {'type': 'Python'}
    # redirect_field_name = 'mypython/module_detail.html'

class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm

    # The post needs to be re-published if it is updated.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.published_date = None
        self.object.save()
        return super().form_valid(form)

class ModuleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Module
    # success_url = '/'
    permission_required = "mypython.can_publish_module"
    success_url = reverse_lazy('mypython:module_list')  # Remember to use the app name prefix.

class DraftListView(LoginRequiredMixin, ListView):
    model = Module
    context_object_name = 'all_modules'
    paginate_by = 10
    template_name = 'mypython/module_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q1', '')
        object_list = Module.objects.filter(
            Q(published_date__isnull=True) &
            (Q(title__icontains=query) | Q(type__icontains=query))
        ).order_by('title')

        return object_list

@permission_required('mypython.can_publish_module')
def module_publish(request, pk):
    module = get_object_or_404(Module, pk=pk)
    module.publish()
    return redirect('mypython:module_list')
