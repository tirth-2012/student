from django.db import models

# Create your models here.

class studentdata(models.Model):
    Male='Male'
    Female='Famale'
    gender=(
        (Male,'Male'),
        (Female,'Female')
    )
    Ahemadabad='Ahemadabad'
    Surendernagar='Surendernagar'
    Surat='Surat'
    Bhavanagar='Bhavanagar'
    Gandhinagar='Gandhinagar'
    city=(
        (Ahemadabad,'Ahemadabad'),
        (Surendernagar,'Surendernagar'),
        (Surat,'Surat'),
        (Bhavanagar,'Bhavanagar'),
        (Gandhinagar,'Gandhinagar')
    )
    fname=models.CharField(max_length=200)
    mname=models.CharField(max_length=200)
    lname=models.CharField(max_length=200)
    gender=models.CharField(max_length=200,choices=gender,default=Male)
    email=models.EmailField(max_length=200)
    phone=models.IntegerField()
    city=models.CharField(max_length=50,choices=city,default=Ahemadabad)
    address=models.CharField(max_length=200)
    coures=models.CharField(max_length=50)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    admission_date=models.DateField()
    image=models.ImageField(upload_to='student_image', null=True, blank=True)
    
    def __str__(self):
        return self.fname
    
class fees(models.Model):
    Cash='Cash'
    Online='Online'
    Card='Card'
    pay_method=(
        (Cash,'Cash'),
        (Online,'Online'),
        (Card,'Card')
    )
    student = models.ForeignKey(studentdata, on_delete=models.CASCADE, related_name='fees')
    payment=models.DecimalField(max_digits=10,decimal_places=2)
    date_paid=models.DateField()
    take=models.CharField(max_length=50)
    pay_method=models.CharField(max_length=50,choices=pay_method)
    
    def __str__(self):
        return self.take

class attendance(models.Model):
    student = models.ForeignKey(studentdata, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return self.status
    
class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
    

    
    