from django.conf import settings
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import Http404, JsonResponse
from .forms import ShortenForm
from .models import ShortURL
from .utils import (
    generate_unique_code, suggest_code_from_url, default_expiry,
    fetch_opengraph_meta, rate_limit_ok
)

def home(request):
    ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
    suggested = None
    new_short = None
    og = {}

    form = ShortenForm(request.POST or None)
    if request.method == "POST":
        if not rate_limit_ok(ip):
            form.add_error(None, f"Rate limit exceeded. Try later.")
        elif form.is_valid():
            original_url = form.cleaned_data["original_url"]
            custom_code = form.cleaned_data["custom_code"] or None
            expires_in = form.cleaned_data.get("expires_in_days")

            expires_at = default_expiry() if not expires_in else timezone.now() + timezone.timedelta(days=expires_in)
            title, image = fetch_opengraph_meta(original_url)

            try:
                with transaction.atomic():
                    code = custom_code or generate_unique_code()
                    obj = ShortURL.objects.create(
                        original_url=original_url, code=code, expires_at=expires_at,
                        title=title, image_url=image
                    )
                new_short = request.build_absolute_uri(reverse("go", args=[obj.code]))
                og = {"title": obj.title, "image": obj.image_url}
            except IntegrityError:
                form.add_error("custom_code", "This code is already taken. Try another.")
    else:
        # 1%: when landing, pre-suggest a vanity code once user starts typing (AJAX route exists too)
        suggested = ""

    latest = ShortURL.objects.all()[:10]
    return render(request, "home.html", {
        "form": form, "latest": latest, "new_short": new_short,
        "suggested": suggested, "og": og
    })

def suggest(request):
    url = request.GET.get("url","")
    if not url:
        return JsonResponse({"suggestion": ""})
    return JsonResponse({"suggestion": suggest_code_from_url(url)})

def details(request, code: str):
    obj = get_object_or_404(ShortURL, code=code)
    return render(request, "detail.html", {"item": obj})

def go(request, code: str):
    obj = get_object_or_404(ShortURL, code=code)
    if obj.expires_at and timezone.now() > obj.expires_at:
        raise Http404("This link has expired.")
    ShortURL.objects.filter(pk=obj.pk).update(clicks=obj.clicks + 1)
    return redirect(obj.original_url)
