from django.shortcuts import render
from datetime import date, timedelta
from django.db.models import Count
from .models import Customer, Interaction 

def index(request):
    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "index.html", context)

def create_customer(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        social_media_handle = request.POST["social_media_handle"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        customer = Customer.objects.create(
            name=name, 
            email=email, 
            social_media_handle=social_media_handle,
            phone=phone, 
            address=address
        )
        customer.save()
        msg = "Customer saved successfully"
        return render(request, "add.html", context={"msg": msg})
    return render(request, "add.html")

def interact(request, cid):
    channels = Interaction.CHANNEL_CHOICES
    directions = Interaction.DIRECTION_CHOICES
    context = {"channels": channels, "directions": directions}

    if request.method == "POST":
        customer = Customer.objects.get(id=cid)
        channel = request.POST["channel"]
        direction = request.POST["direction"]
        summary = request.POST["summary"]
        interaction = Interaction.objects.create(
            customer=customer,
            channel=channel,
            direction=direction,
            summary=summary
        )
        interaction.save()
        context["msg"] = "Interaction recorded successfully"
        return render(request, "interact.html", context=context)

    return render(request, "interact.html", context=context)

def summary(request):
    thirty_days_ago = date.today() - timedelta(days=30)
    interactions = Interaction.objects.filter(
        interaction_date__gte=thirty_days_ago
    )
    count = len(interactions)
    interactions = interactions.values(
        "channel", "direction"
    ).annotate(count=Count('channel'))
    context = {
        "interactions": interactions,
        "count": count
    }
    return render(request, "summary.html", context=context)