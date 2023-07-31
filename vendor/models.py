from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification_email


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='media/vendor/license')
    is_approved: bool = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    # Gửi email thông báo đến nhà hàng
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email
                }
                if self.is_approved:
                    mail_subject = "Xin chúc mừng! Nhà hàng của bạn đã được phê duyệt!"
                    send_notification_email(mail_subject, mail_template, context)
                else:
                    mail_subject = "Rất tiếc! Bạn không đủ điều kiện để đăng nhà hàng lên sàn giao dịch của chúng tôi"
                    send_notification_email(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)
