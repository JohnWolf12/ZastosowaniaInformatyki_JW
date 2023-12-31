# Generated by Django 4.1.7 on 2023-11-21 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplikacjaogloszeniowa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wiadomosc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tresc', models.TextField(max_length=500)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('nowa', models.BooleanField(default=True)),
                ('adresat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adresat', to='aplikacjaogloszeniowa.uzytkownik')),
                ('nadawca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nadawca', to='aplikacjaogloszeniowa.uzytkownik')),
            ],
            options={
                'verbose_name': 'wiadomość',
                'verbose_name_plural': 'wiadomości',
            },
        ),
    ]
