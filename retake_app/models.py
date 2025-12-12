from django.db import models
import bcrypt
# Create your models here.


class User(models.Model):
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128, null=False)  # hashed password
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        hashed = bcrypt.hashpw(raw_password.encode(
            'utf-8'), bcrypt.gensalt(rounds=16))
        self.password = hashed.decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))


class Tree(models.Model):
    species = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=255, null=False)
    mapped_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_id")
    zip_code = models.CharField(max_length=10, null=False)
    date_found = models.DateTimeField(null=False)
    notes = models.TextField(null=True, blank=True, max_length=50)
    visitors = models.ManyToManyField(
        User, related_name="visited_trees", blank=True)
    zip_code_trees = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="zip_code", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
