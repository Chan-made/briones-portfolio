from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, Education, Skill, Profile, About, ContactInfo, Owner
from .forms import ContactForm


def get_profile():
    """Get profile from database"""
    return Profile.objects.first()


def get_about():
    """Get about info from database"""
    return About.objects.first()


def get_contact_info():
    """Get contact info from database"""
    return ContactInfo.objects.first()


def home(request):
    context = {
        'owner': get_profile(),
        'about': get_about(),
        'projects': Project.objects.all().order_by('order')[:3],  # Latest 3 projects
        'skills': Skill.objects.all().order_by('order')[:6],  # Top 6 skills
    }
    return render(request, 'briones_app/home.html', context)


def about(request):
    context = {
        'owner': get_profile(),
        'about': get_about(),
        'skills': Skill.objects.all().order_by('order'),
        'education': Education.objects.all().order_by('order'),
    }
    return render(request, 'briones_app/about.html', context)


def skills(request):
    # Get all skills from database
    skills_list = Skill.objects.all().order_by('category', 'order')
    
    # Debug print to terminal
    print(f"Found {skills_list.count()} skills")
    for skill in skills_list:
        print(f"- {skill.name}: {skill.proficiency}% ({skill.category})")
    
    # Organize skills by category
    categories = {}
    for skill in skills_list:
        # Get the display name for the category
        cat_display = skill.get_category_display()
        if cat_display not in categories:
            categories[cat_display] = []
        categories[cat_display].append(skill)
    
    print(f"Categories: {list(categories.keys())}")  # Debug print
    
    context = {
        'owner': get_profile(),
        'categories': categories,
    }
    return render(request, 'briones_app/skills.html', context)


def projects(request):
    context = {
        'owner': get_profile(),
        'projects': Project.objects.all().order_by('order'),
    }
    return render(request, 'briones_app/projects.html', context)


def education(request):
    context = {
        'owner': get_profile(),
        'education_list': Education.objects.all().order_by('order'),
    }
    return render(request, 'briones_app/education.html', context)


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent! I will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    context = {
        'owner': get_profile(),
        'contact_info': get_contact_info(),
        'form': form,
    }
    return render(request, 'briones_app/contact.html', context)

def about_view(request):
    about = About.objects.first()
    owner = Owner.objects.first()

    return render(request, 'briones_app/about.html', {
        'about': about,
        'owner': owner,
    })