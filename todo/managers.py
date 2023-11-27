from django.db.models import Manager, Count

class AliManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user=1)


class TaskManager(Manager):
    def task_count(self):
        return self.get_queryset().count()


class PersonManager(Manager):
    def users_with_no_task(self):
        return self.get_queryset().annotate(
            task_count=Count("task")).filter(task_count=0)
    """
    SELECT user.* , count(task) as task_count
    from user inner join task on user.id = task.user
    where task_count = 0
    group by user.id
    """
    """
    list of users:
    name    username    password    task_count
    """
