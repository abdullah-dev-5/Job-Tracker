from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="logo_image",
            field=models.ImageField(blank=True, null=True, upload_to="company_logos/"),
        ),
        migrations.AddField(
            model_name="application",
            name="logo_url",
            field=models.URLField(blank=True),
        ),
    ]