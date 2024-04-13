from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from ..forms import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from ..models import *
import uuid
from django.contrib.auth.decorators import permission_required


@permission_required("main.is_HMC", "/login")
def register_warden(request):
    if request.method == "POST":
        form = WardenRegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            stakeholderID = form.cleaned_data.get("stakeholderID")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            mobile = form.cleaned_data.get("mobile")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            hall = form.cleaned_data.get("hall")
            token = str(uuid.uuid4())
            department = form.cleaned_data.get("department")
            designation = form.cleaned_data.get("designation")
            posts_held = form.cleaned_data.get("posts_held")
            client = Client.objects.create_user(
                stakeholderID,
                email,
                password,
                mobile,
                first_name,
                last_name,
                address,
                token,
                "warden",
            )
            perm = Permission.objects.get(name="is_warden")
            client.user_permissions.add(perm)
            perm = Permission.objects.filter(name="is_hall").first()
            client.user_permissions.add(perm)
            perm = Permission.objects.get(name="is_mess")
            client.user_permissions.add(perm)
            warden = Warden(
                client=client,
                hall=hall,
                department=department,
                designation=designation,
                posts_held=posts_held,
            )
            warden.save()
            subject = "Your account needs to be verified"
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/hmc/verify-warden/{token}"
            email_from = "se.mhc.2024@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request,
                f"Pls click on the link sent to {email} to complete registration",
            )
            return redirect("/hmc/landing")
    else:
        form = WardenRegistrationForm()
    return render(
        request,
        "hmc/register_warden.html",
        context={"form": form, "title": "register"},
    )


@permission_required("main.is_HMC", "/login")
def search_warden(request):
    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            stakeholderID = form.cleaned_data.get("stakeholderID")
            try:
                client = Client.objects.filter(stakeholderID=stakeholderID).first()
                print(client.role)
                if client.role == "warden":
                    return redirect(f"/hmc/update-warden-profile/{stakeholderID}")
                else:
                    messages.MessageFailure(
                        request,
                        f"User not found",
                    )
                    return redirect("/hmc/search-warden")

            except:
                messages.MessageFailure(
                    request,
                    f"User not found",
                )
                return redirect("/hmc/search-warden")
    else:
        form = UserSearchForm()
    return render(
        request,
        "hmc/search_warden.html",
        context={"form": form, "title": "register"},
    )


@permission_required("main.is_HMC", "/login")
def update_warden_profile(request, stakeholderID):
    client = Client.objects.filter(stakeholderID=stakeholderID).first()
    warden = Warden.objects.filter(client=client).first()
    if request.method == "POST":
        form = UpdateWardenForm(request.POST, instance=warden)
        if form.is_valid():
            client.stakeholderID = form.cleaned_data.get("stakeholderID")
            client.email = form.cleaned_data.get("email")
            client.address = form.cleaned_data.get("address")
            client.mobile = form.cleaned_data.get("mobile")
            client.first_name = form.cleaned_data.get("first_name")
            client.last_name = form.cleaned_data.get("last_name")
            warden.hall = form.cleaned_data.get("hall")
            warden.designation = form.cleaned_data.get("designation")
            warden.posts_held = form.cleaned_data.get("posts_held")
            client.save()
            warden.client = client
            warden.save()
            messages.success(
                request,
                "Warden Profile Edited!",
            )
            return redirect("/hmc/search-warden")  # Redirect to a success page
    else:
        form = UpdateWardenForm(
            initial={
                "stakeholderID": stakeholderID,
                "email": client.email,
                "mobile": client.mobile,
                "address": client.address,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "hall": warden.hall,
                "designation": warden.designation,
                "posts_held": warden.posts_held,
            }
        )
        # print(form.instance)
        # form.instance = student

    return render(request, "hmc/update_warden_profile.html", {"form": form})


@permission_required("main.is_HMC", "/login")
def verify_warden(request, token):
    client = Client.objects.filter(token=token).first()
    if client:
        client.is_active = True
        client.save()
        messages.info(request, "Your account has been verified")
        return redirect("/hmc/landing")
    else:
        return redirect("/error")


@permission_required("main.is_HMC", "/login")
def hmc_landing(request):
    return render(request, "hmc/landing.html")


@permission_required("main.is_HMC", "/login")
def register_hall(request):
    if request.method == "POST":
        form = HallRegistrationForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data.get("name")
            no_of_blocks = form.cleaned_data.get("blocks")
            no_of_floors = form.cleaned_data.get("floors")
            singles = form.cleaned_data.get("singles")
            rent_singles = form.cleaned_data.get("rent_singles")
            doubles = form.cleaned_data.get("doubles")
            rent_doubles = form.cleaned_data.get("rent_doubles")
            triples = form.cleaned_data.get("triples")
            rent_triples = form.cleaned_data.get("triples")

            print(int(rent_singles))

            hall = Hall.objects.create(
                name=name,
                singles=singles,
                doubles=doubles,
                triples=triples,
                floors=no_of_floors,
                blocks=no_of_blocks,
            )
            hall.save()

            for x in range(int(no_of_blocks)):
                for y in range(int(no_of_floors)):
                    for z in range(int(singles)):
                        room = Room(
                            hall=hall,
                            rent=rent_singles,
                            sharing=1,
                            floor=y,
                            block=chr(65 + x),
                            number=z,
                            code=name + "-" + str(chr(65 + x)) + str(y) + str(z),
                        )
                        room.save()

            x = 0
            y = 0

            for x in range(int(no_of_blocks)):
                for y in range(int(no_of_floors)):
                    for z in range(int(singles), int(singles) + int(doubles)):
                        room = Room(
                            hall=hall,
                            rent=rent_doubles,
                            sharing=2,
                            floor=y,
                            block=chr(65 + x),
                            number=z,
                            code=name + "-" + str(chr(65 + x)) + str(y) + str(z),
                        )
                        room.save()

            x = 0
            y = 0

            for x in range(int(no_of_blocks)):
                for y in range(int(no_of_floors)):
                    for z in range(
                        int(singles) + int(doubles),
                        int(singles) + int(doubles) + int(triples),
                    ):
                        room = Room(
                            hall=hall,
                            rent=rent_triples,
                            sharing=3,
                            floor=y,
                            block=chr(65 + x),
                            number=z,
                            code=name + "-" + str(chr(65 + x)) + str(y) + str(z),
                        )
                        room.save()

            hall.max_occupancy = hall.calculate_max_occupancy()
            hall.save()
            hall_passbook = HallPassbook.objects.create(hall=hall)
            mess_passbook = MessPassbook.objects.create(hall=hall)
            warden_passbook = WardenPassbook.objects.create(hall=hall)
            messages.info(request, f"Hall {name} has been created")
            return redirect("/hmc/view-halls")

    else:
        form = HallRegistrationForm()

    return render(request, "hmc/hall_registration.html", {"form": form})


@permission_required("main.is_HMC", "/login")
def hmc_landing(request):
    return render(request, "hmc/landing.html")


@permission_required("main.is_HMC", "/login")
def view_halls(request):
    halls = list(Hall.objects.all())
    for hall in halls:
        hall.max_occupancy = hall.calculate_max_occupancy()
        hall.current_occupancy = hall.calculate_curr_occupancy()
        hall.save()
    return render(request, "hmc/view_halls.html", context={"halls": halls})


@permission_required("main.is_HMC", "/login")
def grant_allotment(request):
    if request.method == "POST":
        form = GrantForm(request.POST)
        if form.is_valid():
            password_to_confirm = form.cleaned_data.get("verify_password")
            hall = form.cleaned_data.get("hall")
            amount = form.cleaned_data.get("amount")
            client = request.user
            success = client.check_password(password_to_confirm)
            if success:
                # try:
                warden_passbook = WardenPassbook.objects.filter(hall=hall).first()

                warden_transaction = WardenTransaction.objects.create(
                    type="grant",
                    timestamp=datetime.now(),
                    amount=amount,
                    warden_passbook=warden_passbook,
                )
                # except:
                messages.success(request, "Your grant has been alloted old codger")
                redirect("/hmc/landing")

            # except:
            #     messages.error(request, "Connection issues")
            else:
                messages.error(request, "you are unreal")
                redirect("/login")
    else:
        form = GrantForm()

    return render(
        request,
        "hmc/verify_password.html",
        context={"form": form, "title": "verify"},
    )


@permission_required("main.is_HMC", "/login")
def delete_warden(request):
    if request.method == "POST":
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            stakeholderID = form.cleaned_data.get("stakeholderID")
            password_to_confirm = form.cleaned_data.get("verify_password")
            client = Client.objects.filter(stakeholderID=stakeholderID).first()
            warden = Warden.objects.filter(client=client).first()
            if warden:
                client = request.user
                success = client.check_password(password_to_confirm)
                if success:
                    warden.client.delete()
                    messages.success(
                        request,
                        f"Warden with stakeholder ID {stakeholderID} has been deleted",
                    )
                else:
                    messages.error(request, "Invalid password")
            else:
                messages.error(
                    request,
                    f"No active warden found with stakeholder ID {stakeholderID}",
                )
    else:
        form = DeleteUserForm()
    return render(
        request,
        "hmc/delete_warden.html",
        context={"form": form, "title": "verify"},
    )


@permission_required("main.is_HMC", "/login")
def hmc_view_profile(request):
    if request.method == "GET":
        hmc = HMC.objects.filter(client=request.user).first()
        return render(
            request,
            "hmc/profile.html",
            context={"hmc": hmc, "title": "view_profile"},
        )


@permission_required("main.is_HMC", "/login")
def hmc_change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            client = request.user
            hmc = HMC.objects.filter(client=client).first()
            current_password = form.cleaned_data.get("current_password")
            success = client.check_password(current_password)
            if success:
                new_password = form.cleaned_data.get("new_password")
                confirm_password = form.cleaned_data.get("confirm_password")
                if new_password == confirm_password:
                    client.set_password(new_password)
                    client.save()
                    hmc.client = client
                    hmc.save()
                    logout(request)
                    hmc = authenticate(
                        request, username=client.stakeholderID, password=new_password
                    )
                    login(request, hmc)
                    messages.success(request, "Password has been updated")
                    return redirect("/hmc/landing")
                else:
                    messages.error(
                        request, f"New password did not match confirm password"
                    )
                    return redirect("/hmc/change-password")
            else:
                messages.error(request, f"Current password entered is incorrect")
                return redirect("/hmc/change-password")

    else:
        form = ChangePasswordForm()
    return render(
        request,
        "hmc/change_password.html",
        context={"form": form, "title": "Password"},
    )
