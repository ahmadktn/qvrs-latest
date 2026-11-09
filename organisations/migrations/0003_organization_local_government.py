from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0002_alter_organization_id_alter_organizationvetting_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='local_government',
            field=models.CharField(default='', help_text='Local Government Area (LGA)', max_length=100, verbose_name='Local Government'),
        ),
    ]

