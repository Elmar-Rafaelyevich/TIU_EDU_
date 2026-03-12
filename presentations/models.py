from django.db import models
from django.contrib.auth.models import User
import os

class Group(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название группы")
    description = models.TextField(blank=True, verbose_name="Описание")
    # ИЗМЕНИТЕ ЭТУ СТРОКУ - добавьте related_name
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='teacher_groups'  # Изменено с 'groups' на 'teacher_groups'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Presentation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='presentations')
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to='presentations/%Y/%m/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Презентация"
        verbose_name_plural = "Презентации"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title
    
    def filename(self):
        return os.path.basename(self.file.name)