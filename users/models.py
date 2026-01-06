from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UnicodeUsernameValidator,
    UserManager as UserManagerDjango, _,
)
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.utils.timezone import now, timedelta, timezone
from django.template.loader import render_to_string
from users.tasks import send_email


class UserManager(UserManagerDjango):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_deleted", False)
        extra_fields.setdefault("is_email_verified", True)
        extra_fields.setdefault("verification_code", None)
        extra_fields.setdefault("expire_verification_code", None)

        return super().create_superuser(username, email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
       An abstract base class implementing a fully featured User model with
       admin-compliant permissions.

       Username and password are required. Other fields are optional.
   """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"),
                              unique=True,
                              error_messages={
                                  "unique": _("A user with that email already exists")
                              })
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    expire_verification_code = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    # phone = models.CharField(max_length=15, validators=[RegexValidator(
    #     regex=r'^(01|\+201|00201)[0-2,5]{1}[0-9]{8}$',
    #     message="Phone number must be entered in the format: +201011111/010111/0020111 . Up to 15 digits allowed.")
    # ])

    # is_phone_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True
        ordering = ('-date_joined',)

    def generate_verification_code(self):
        return get_random_string(length=6)

    def send_email_verification(self):
        if self.is_email_verified:
            return False

        self.verification_code = self.generate_verification_code()
        self.expire_verification_code = now() + timedelta(minutes=settings.EXPIRE_VERIFICATION_CODE_MINUTES)
        self.save()

        context = {
            'app_name': settings.APP_NAME.capitalize(),
            'email_contact_us': settings.EMAIL_CONTACT_US,
            'verification_code': self.verification_code,
            'display_name': self.username
        }
        body = render_to_string('users/verification_code.html', context)
        send_email.delay(f"{settings.APP_NAME.capitalize()} Email Verification", self.email, body)

        return True

    # def send_phone_verification(self):
    #     if self.is_phone_verified or self.verification_code is not None:
    #         return False
    #
    #     self.verification_code = self.generate_verification_code()
    #     self.expire_verification_code = now() + timedelta(minutes=settings.EXPIRE_VERIFICATION_CODE_MINUTES)
    #     self.save()
    #
    #     ## apply third party for send sms message
    #     return True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
