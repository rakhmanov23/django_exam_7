from django_filters import FilterSet, CharFilter, NumberFilter


class VacancyFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    work_time = CharFilter(field_name='time', lookup_expr='icontains')