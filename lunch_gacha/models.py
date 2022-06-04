from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """UserManagerのラッパー

    参考: https://github.com/django/django/blob/main/django/contrib/auth/models.py#L129
    """

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('username is required.'))

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ユーザー

    参考: https://github.com/django/django/blob/main/django/contrib/auth/models.py#L321
    """
    username_validator = \
        RegexValidator(
            regex=u'^[a-zA-z0-9_]+$',
            message='無効なユーザー名です。半角英数字と_(アンダースコア)のみ使用可能です。',
        )

    username = models.CharField(
        _('username'),
        max_length=63,
        unique=True,
        help_text='半角英数字と_(アンダースコア)のみ使用可能です。127文字以内である必要があります。',
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.username = self.normalize_username(self.username)

    def __str__(self):
        return self.username


class District(models.Model):
    """お店のある地区

    """
    name = models.CharField(unique=True, max_length=31, verbose_name='地区名称')

    class Meta:
        verbose_name = verbose_name_plural = '店舗地区'

    def __str__(self):
        return self.name


class StoreType(models.Model):
    """店舗形態

    """
    name = models.CharField(unique=True, max_length=15, verbose_name='形態名称')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='説明')

    class Meta:
        verbose_name = verbose_name_plural = '店舗形態'

    def __str__(self):
        return self.name


class LunchGenre(models.Model):
    """食事のジャンル

    """
    name = models.CharField(unique=True, max_length=15, verbose_name='ジャンル名称')

    class Meta:
        verbose_name = verbose_name_plural = '食事ジャンル'

    def __str__(self):
        return self.name


class LunchPlace(models.Model):
    """
    ガチャ要素
    """
    name = models.CharField(unique=True, max_length=63, verbose_name='店舗名')
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name='地区')
    store_type = models.ForeignKey(StoreType, on_delete=models.PROTECT, verbose_name='店舗形態')
    genre = models.ManyToManyField(LunchGenre, verbose_name='ジャンル')
    has_eatin = models.BooleanField(default=False, verbose_name='店内飲食')
    has_takeout = models.BooleanField(default=False, verbose_name='持ち帰り')
    is_valid =\
        models.BooleanField(
            default=True,
            verbose_name='有効フラグ',
            help_text='結果に含める場合はこのフラグを立ててください。',
        )

    class Meta:
        verbose_name = verbose_name_plural = '店舗'

    def __str__(self):
        return self.name
