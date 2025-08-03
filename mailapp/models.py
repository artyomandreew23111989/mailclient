
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import signing

from django.conf import settings

class User(AbstractUser):
    imap_server = models.CharField(max_length=255, default="mail.akmosk.ru")
    imap_port = models.PositiveIntegerField(default=993)
    smtp_server = models.CharField(max_length=255, default="mail.akmosk.ru")
    smtp_port = models.PositiveIntegerField(default=587)
    signature = models.TextField(blank=True, null=True)
    
    # Добавьте эти строки для решения конфликта:
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="mailapp_user_groups",
        related_query_name="mailapp_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="mailapp_user_permissions",
        related_query_name="mailapp_user",
    )
    class Meta:
        db_table = 'mailapp_user'

class Mailbox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    imap_login = models.CharField(max_length=255)
    _imap_password = models.CharField(max_length=255, db_column='imap_password')
    
    @property
    def imap_password(self):
        return signing.loads(self._imap_password)
    
    @imap_password.setter
    def imap_password(self, value):
        self._imap_password = signing.dumps(value)
    is_active = models.BooleanField(default=True)

class Folder(models.Model):
    FOLDER_TYPES = (
        ('INBOX', 'Входящие'),
        ('SENT', 'Отправленные'),
        ('DRAFTS', 'Черновики'),
        ('TRASH', 'Корзина'),
        ('ARCHIVE', 'Архив'),
        ('JUNK', 'Спам'),
        ('CUSTOM', 'Пользовательская'),
    )
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=FOLDER_TYPES, default='CUSTOM')
    last_uid = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

class Message(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    uid = models.PositiveIntegerField()
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    recipients = models.JSONField()
    date = models.DateTimeField()
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)

class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    content = models.BinaryField()

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Email(models.Model):
    to = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject