from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('reading_app', '0002_highlight'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Highlight',
        ),
    ] 