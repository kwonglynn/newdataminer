from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Deep
from .forms import DeepForm

from django.db.models import Q

@login_required
def deep_create(request):
    if request.method == 'POST':
        form = DeepForm(request.POST)
        if form.is_valid():
            deep = form.save(commit=False)
            deep.added_by = request.user
            deep.save()

            return redirect('deep:deep_draft_list')
    else:
        form = DeepForm()

    return render(request, 'deep/deep_form.html', {'form':form})

class DeepListView(ListView):
    model = Deep
    template_name = 'deep/deep_list.html'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q3', '')
        object_list = Deep.objects.filter(
            Q(published_date__lte=timezone.now()) & Q(title__icontains=query)
        ).order_by('title')

        return object_list

class DeepDetailView(DetailView):
    model = Deep

class DeepCreateView(PermissionRequiredMixin, CreateView):
    model = Deep
    form_class = DeepForm
    permission_required = "deep.can_publish_delete"

class DeepUpdateView(LoginRequiredMixin, UpdateView):
    model = Deep
    form_class = DeepForm

    # The post needs to be re-published if it is updated.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.published_date = None
        self.object.save()
        return super().form_valid(form)

class DeepDeleteView(PermissionRequiredMixin, DeleteView):
    model = Deep
    permission_required = "deep.can_publish_delete"
    success_url = reverse_lazy('deep:deep_list')  # Remember to use the app name prefix.

class DraftListView(LoginRequiredMixin, ListView):
    model = Deep
    paginate_by = 10
    template_name = 'deep/deep_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q3', '')
        object_list = Deep.objects.filter(
            Q(published_date__isnull=True) & Q(title__icontains=query)
        ).order_by('title')

        return object_list

@permission_required('deep.can_publish_delete')
def publish(request, pk):
    object = get_object_or_404(Deep, pk=pk)
    object.publish()
    return redirect('deep:deep_list')
