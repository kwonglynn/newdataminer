from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Machine
from .forms import MachineForm

from django.db.models import Q


def pandas(request):
    return render(request, "machine/pandas.html")

@login_required
def machine_create(request):
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            machine = form.save(commit=False)
            machine.added_by = request.user
            machine.save()

            return redirect('machine:machine_draft_list')
    else:
        form = MachineForm()

    return render(request, 'machine/machine_form.html', {'form':form})

class MachineListView(ListView):
    model = Machine
    template_name = 'machine/machine_list.html'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q2', '')
        object_list = Machine.objects.filter(
            Q(published_date__lte=timezone.now()) & Q(title__icontains=query)
        ).order_by('title')

        return object_list

class MachineDetailView(DetailView):
    model = Machine

class MachineCreateView(PermissionRequiredMixin, CreateView):
    model = Machine
    form_class = MachineForm
    permission_required = "machine.can_publish_delete"

class MachineUpdateView(LoginRequiredMixin, UpdateView):
    model = Machine
    form_class = MachineForm

    # The post needs to be re-published if it is updated.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.published_date = None
        self.object.save()
        return super().form_valid(form)

class MachineDeleteView(PermissionRequiredMixin, DeleteView):
    model = Machine
    permission_required = "machine.can_publish_delete"
    success_url = reverse_lazy('machine:machine_list')  # Remember to use the app name prefix.

class DraftListView(LoginRequiredMixin, ListView):
    model = Machine
    paginate_by = 10
    template_name = 'machine/machine_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q3', '')
        object_list = Machine.objects.filter(
            Q(published_date__isnull=True) & Q(title__icontains=query)
        ).order_by('title')

        return object_list

@permission_required('machine.can_publish_delete')
def publish(request, pk):
    object = get_object_or_404(Machine, pk=pk)
    object.publish()
    return redirect('machine:machine_list')
