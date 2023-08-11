from django.db import models
from django.template.defaultfilters import slugify

class Book(models.Model):
    bid = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField()
    genre = models.CharField(max_length=255, blank=True, null=True)
    page_count = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    date_published = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    edition = models.CharField(max_length=100, blank=True, null=True)
    format = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    img = models.URLField(blank=True, null=True)
    info_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)

    # OLD MODEL
    # bid = models.CharField(max_length=100, primary_key=True)
    # title = models.CharField(max_length=255)
    # slug = models.SlugField(max_length=255, null=True, blank=True)
    # author = models.CharField(max_length=255)
    # about = models.TextField()
    # date_published = models.IntegerField()
    # publisher = models.CharField(max_length=255, blank=True, null=True)
    # book_edition = models.CharField(max_length=100, blank=True, null=True)
    # book_format = models.CharField(max_length=100, blank=True, null=True)
    # book_isbn = models.CharField(max_length=100, blank=True, null=True)
    # book_language = models.CharField(max_length=100, blank=True, null=True)
    # img = models.URLField(blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        to_assign = slugify(self.title[:44])
        if Book.objects.filter(title=self.title).exists():
            return
        if Book.objects.filter(slug=to_assign).exists():
            to_assign = to_assign + '-' + str(Book.objects.all().count())
        self.slug = to_assign
        super().save()

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    review = models.TextField(default='')
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['book', '-created_at']

    def __str__(self):
        return self.name+'-'+self.book.title
