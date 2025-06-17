from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from .models import ContactMessage
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def index(request):
    profile = models.Profile.objects.first()
    about = models.About.objects.first()
    colors = models.Color.objects.first()
    skills = models.Skill.objects.all()
    education = models.Education.objects.all()
    experience = models.Experience.objects.all()

    projects = models.Project.objects.all()[:6]  
    contact = models.ContactMessage.objects.all()
    professions = models.Profession.objects.all()
    services = models.Service.objects.all()
    socialMedia = models.SocialMedia.objects.all()


    # paginator = Paginator(projects, 6)
    # page = request.GET.get('page')
    # projectDataFinal = paginator.get_page(page)

    projects_total = models.Project.objects.all().count()

    


    data={
        'profile' : profile,
        'about' : about,
        'skills' : skills,
        'education' : education,
        'experience' : experience,
        'projects' : projects,
        'contact' : contact,
        'professions' : professions,
        'services' : services,
        'socialMediaIcons' : socialMedia,
        'projects_total' : projects_total,
        'colors' : colors,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact = models.ContactMessage.objects.create(name=name, email=email, message=message)
        contact.save()
        messages.success(request, "Message submitted successfully! You will get a response soon.")
        return redirect('/')
    return render(request, 'index.html', data)


def project_detail(request, id):
    project = models.Project.objects.get(id=id)
    profile = models.Profile.objects.first()
    return render(request, 'portfolioProject.html', {'project': project, 'profile':profile })

def load_more_projects(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 6))
    
    projects = models.Project.objects.all()[offset:offset + limit]
    
    if projects.exists():  # This check is important!
        html = render_to_string('partials/project_card.html', {'projects': projects})
        return HttpResponse(html)
    else:
        return HttpResponse("")  

 
@login_required(login_url='/login/')
def mainAdmin(request):
    profile = models.Profile.objects.first()
    messages = ContactMessage.objects.all().order_by('-id')  # latest first

    # Get filters from query parameters
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Apply keyword search
    if query:
        messages = messages.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(message__icontains=query)
        )

    # Filter by response status
    if status == 'responded':
        messages = messages.filter(responded=True)
    elif status == 'not_responded':
        messages = messages.filter(responded=False)
    else:
        messages = messages    

    # Filter by date range
    if start_date:
        messages = messages.filter(created_at__gte=start_date)

    if end_date:
        messages = messages.filter(created_at__lte=end_date)

    # ✅ Add Pagination (10 messages per page)
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    colors  = models.Color.objects.first()

    context = {
        'contactMessages': page_obj,  # use page_obj here
        'profile' : profile,
        'is_admin': True,
        'colors': colors,
    }
    return render(request, 'mainAdmin/mainAdmin.html', context)


@login_required(login_url='/login/')
def mark_responded(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)

    # Gmail compose URL
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={message.email}&su=Regarding your message&body=Hi {message.name},%0D%0A"
    message.responded = True
    message.save()
    return redirect(gmail_url)

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Password changed successfully.")
            return redirect('mainAdmin')  # or your desired page
    colors = models.Color.objects.first()
    profile = models.Profile.objects.first()

    return render(request, 'mainAdmin/change_password.html', {'is_admin': True, 'colors': colors, 'profile':profile })

@login_required(login_url='/login/')
def settings(request):
    profile = models.Profile.objects.first()

    # if request.method == 'POST':
    if 'profile-form' in request.POST:
        profile_name = request.POST.get('profile-name')
        profile_email = request.POST.get('profile-email')
        profile_phone = request.POST.get('profile-phone')
        profile_image = request.FILES.get('profile-image')
        profile_cv = request.FILES.get('profile-cv')
        home_intro = request.POST.get('home-intro')



        if profile:
            profile.name = profile_name
            profile.email = profile_email
            profile.phone = profile_phone
            profile.intro = home_intro
            if profile_image:
                profile.profile_image = profile_image
            if profile_cv:
                profile.pdf = profile_cv

            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('/settings/#profile-form')

    if 'profession-form' in request.POST:
            profession = request.POST.get('profession')
            profession_obj = models.Profession.objects.create(profession=profession)
            profession_obj.save() 
            return redirect('/settings/#profession-form')
    if 'about-form' in request.POST:
            about_obj = models.About.objects.first()
            about_intro = request.POST.get('about-intro')
            about_image = request.FILES.get('about-image')
            about_obj.about_intro = about_intro
            about_obj.about_image = about_image
            about_obj.save() 
            messages.success(request, 'About section has changed successfully!')
            return redirect('/settings/#about-form')
    if 'skill-form' in request.POST:
            skill_name = request.POST.get('skill-name')
            skill_perc = request.POST.get('skill-percentage')
            skills_obj = models.Skill.objects.create(name=skill_name, percentage=skill_perc)
            skills_obj.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('/settings/#skill-form')
    
    if 'education-form' in request.POST:
            edu_title = request.POST.get('education-title')
            edu_desc = request.POST.get('education-description')
            edu_year = request.POST.get('education-year')
            edu_obj = models.Education.objects.create(title=edu_title, description=edu_desc, year=edu_year)
            edu_obj.save()
            messages.success(request, 'Degree added successfully!')
            return redirect('/settings/#education-form')
    if 'experience-form' in request.POST:
            exp_title = request.POST.get('experience-title')
            exp_desc = request.POST.get('experience-description')
            exp_year = request.POST.get('experience-year')
            exp_obj = models.Experience.objects.create(title=exp_title, description=exp_desc, year=exp_year)
            exp_obj.save()
            messages.success(request, 'Experience added successfully!')
            return redirect('/settings/#experience-form')
    if 'project-form' in request.POST:
            project_title = request.POST.get('project-title')
            project_desc = request.POST.get('project-description')
            project_url = request.POST.get('project-url')
            project_image = request.FILES.get('project-image')
            project_image2 = request.FILES.get('project-image2')
            project_image3 = request.FILES.get('project-image3')
            project_image4 = request.FILES.get('project-image4')
            project_obj = models.Project.objects.create(title=project_title, description=project_desc, url=project_url, image=project_image, image2=project_image2, image3=project_image3, image4=project_image4)
            project_obj.save()
            messages.success(request, 'Project added in portfolio successfully!')
            return redirect('/settings/#project-form')
    if 'services-form' in request.POST:
            ser_title = request.POST.get('service-title')
            ser_desc = request.POST.get('service-description')
            ser_icon = request.POST.get('service-icon')
            ser_obj = models.Service.objects.create(name=ser_title, description=ser_desc, icon=ser_icon)
            ser_obj.save()
            messages.success(request, 'Service added successfully!')
            return redirect('/settings/#service-form')
    if 'socialMedia-form' in request.POST:
            social_title = request.POST.get('social-title')
            social_icon = request.POST.get('social-icon')
            social_link = request.POST.get('social-link')
            social_obj = models.SocialMedia.objects.create(name=social_title, link=social_link, icon=social_icon)
            social_obj.save()
            messages.success(request, 'Link added successfully!')
            return redirect('/settings/#socialMedia-form')
    if 'color-form' in request.POST:
        colors = models.Color.objects.first()
    
    # If no color object exists, create one
        if not colors:
            colors = models.Color.objects.create(color1='#13141E', color2='#FFFFFF', color3='#7328FF', color4='#28282B' )

        if colors.color1=='' and colors.color2=='' and colors.color3=='' and colors.color4=='':
            colors.color1 = '#13141E'
            colors.color2 = '#FFFFFF'
            colors.color3 = '#7328FF'
            colors.color4 = '#28282B'
        else:
            colors.color1 = request.POST.get('color1')
            colors.color2 = request.POST.get('color2')
            colors.color3 = request.POST.get('color3')
            colors.color4 = request.POST.get('color4')
        colors.save()

        messages.success(request, 'Color updated successfully!')
        return redirect('/settings/#color-form')

                 
    about = models.About.objects.first()
    colors = models.Color.objects.first()
    professions = models.Profession.objects.all().order_by('id')
    skills = models.Skill.objects.all().order_by('id')
    education = models.Education.objects.all().order_by('id')
    experience = models.Experience.objects.all().order_by('id')
    projects = models.Project.objects.all().order_by('id')
    services = models.Service.objects.all().order_by('id')
    socialMedia = models.SocialMedia.objects.all().order_by('id')
    context = {
        'profile': profile,
        'is_admin': True,
        'professions' : professions,
        'skills' : skills,
        'education' : education,
        'experience' : experience,
        'projects' : projects,
        'about' : about,
        'services' : services,
        'socialMedia' : socialMedia,
        'colors' : colors,
    }
    return render(request, 'mainAdmin/settings.html', context)

@login_required(login_url='/login/')
def delete_social_media(request, id):
    social = get_object_or_404(models.SocialMedia, id=id)
    social.delete()
    messages.success(request, 'Record delete succesfully!')
    return redirect('/settings/#socialMedia-form')
@login_required(login_url='/login/')
def delete_profession(request, id):
    profession = get_object_or_404(models.Profession, id=id)
    profession.delete()
    messages.success(request, 'profession delete succesfully')
    return redirect('/settings/#profession-form')
@login_required(login_url='/login/')
def delete_skill(request, id):
    skill = get_object_or_404(models.Skill, id=id)
    skill.delete()
    messages.success(request, 'Skill delete succesfully!')
    return redirect('/settings/#skill-form')
@login_required(login_url='/login/')
def delete_edu(request, id):
    education = get_object_or_404(models.Education, id=id)
    education.delete()
    messages.success(request, 'Info delete succesfully!')
    return redirect('/settings/#education-form')
@login_required(login_url='/login/')
def delete_exp(request, id):
    experience = get_object_or_404(models.Experience, id=id)
    experience.delete()
    messages.success(request, 'Info delete succesfully!')
    return redirect('/settings/#experience-form')
@login_required(login_url='/login/')
def delete_service(request, id):
    service = get_object_or_404(models.Service, id=id)
    service.delete()
    messages.success(request, 'Service delete succesfully!')
    return redirect('/settings/#service-form')
@login_required(login_url='/login/')
def delete_proj(request, id):
    project = get_object_or_404(models.Project, id=id)
    project.delete()
    messages.success(request, 'Info delete succesfully!')
    return redirect('/settings/#project-form')
@login_required(login_url='/login/')
def update_proj(request, id):
     project = get_object_or_404(models.Project, id=id)
     if request.method == 'POST':
          if 'project-form' in request.POST:
               
                proj_title = request.POST.get('project-title')
                proj_image = request.FILES.get('project-image')
                proj_url = request.POST.get('project-url')
                proj_desc = request.POST.get('project-description')

                project.title = proj_title
                project.image = proj_image
                project.url = proj_url
                project.description = proj_desc

                project.save()

                messages.success(request, 'Project details update successfully')
                return redirect('/settings/#project-form')
     context = {
          'project' : project
     }     
     return render(request, 'mainAdmin/settings.html', context)


    
