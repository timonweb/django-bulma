import random
from django.db import migrations


def create_tasks(apps, schema_editor):
    Task = apps.get_model('showcase', 'Task')
    for number in range(1, 51):
        task = Task(
            name='Boring task name #{}'.format(number),
            done=random.randint(0, 1)
        )
        task.save()


def delete_tasks(apps, schema_editor):
    Task = apps.get_model('showcase', 'Task')
    Task.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_tasks, delete_tasks),
    ]
