from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import re
from datetime import datetime
# Create your views here.


def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'register':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            errors = []
            if not email:
                errors.append("Email is required.")
            if email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                errors.append("Email is invalid.")
            if User.objects.filter(email=email).exists():
                errors.append("Email already registered.")
            if password != confirm_password:
                errors.append("Passwords do not match.")
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long.")
            if not fname or not lname:
                errors.append("First and Last names are required.")
            if len(fname) < 2 or len(lname) < 2:
                errors.append(
                    "First and Last names must be at least 2 characters long.")
            if not password:
                errors.append("Password is required.")
            if not confirm_password:
                errors.append("Confirm Password is required.")
            if not errors:
                new_user = User(
                    firstname=fname,
                    lastname=lname,
                    email=email,
                )
                new_user.set_password(password)
                new_user.save()
                request.session['user_id'] = new_user.id
                messages.success(request, "Registration successful.")
                return redirect('dashboard')
            else:
                for error in errors:
                    messages.error(request, error)
                context = {
                    messages: messages.get_messages(request)
                }
                return render(request, 'index.html', context)

        elif action == 'login':
            email = request.POST.get('login_email')
            password = request.POST.get('login_password')
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                request.session['user_id'] = user.id
                messages.success(request, "Login successful.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
                return render(request, 'index.html')

    return render(request, 'index.html')


def add_tree(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to add a tree.")
        return redirect('index')

    if request.method == 'POST':
        species = request.POST.get('species')
        location = request.POST.get('location')
        zip_code = request.POST.get('zip_code')
        date_found = request.POST.get('date_found')
        notes = request.POST.get('notes')

        errors = []
        if len(species) < 2:
            errors.append("Species must be at least 2 characters long.")
        if len(location) < 5:
            errors.append("Location must be at least 5 characters long.")
        if not len(zip_code) == 5:
            errors.append("Zip code must be exactly 5 numbers long.")
        if zip_code and not zip_code.isdigit():
            errors.append("Zip code must contain only numbers.")
        if date_found > datetime.now().strftime('%Y-%m-%d'):
            errors.append("Date found cannot be in the future.")
        if notes and len(notes) > 50:
            errors.append("Notes cannot exceed 50 characters.")

        if not errors:
            user = User.objects.get(id=request.session['user_id'])
            new_tree = Tree(
                species=species,
                location=location,
                mapped_by=user,
                zip_code=zip_code,
                date_found=date_found,
                notes=notes
            )
            new_tree.save()
            messages.success(request, "Tree added successfully.")
            return redirect('dashboard')
        else:
            for error in errors:
                messages.error(request, error)
            return render(request, 'add_tree.html')
    return render(request, 'add_tree.html')


def logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('index')


def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view the dashboard.")
        return redirect('index')

    user = User.objects.get(id=request.session['user_id'])
    trees = Tree.objects.all().order_by('-created_at')
    context = {
        'user': user,
        'trees': trees
    }
    return render(request, 'dashboard.html', context)


def tree_details(request, tree_id):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view tree details.")
        return redirect('index')
    user = User.objects.get(id=request.session['user_id'])

    try:
        tree = Tree.objects.get(id=tree_id)
    except Tree.DoesNotExist:
        messages.error(request, "Tree not found.")
        return redirect('dashboard')

    context = {
        'tree': tree,
        'user': user,
    }
    return render(request, 'tree_details.html', context)


def edit_tree(request, tree_id):
    user = User.objects.get(id=request.session['user_id'])
    mapped_by = Tree.objects.get(id=tree_id).mapped_by.id
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to edit a tree.")
        return redirect('index')
    if request.session['user_id'] != mapped_by:
        messages.error(request, "You can only edit your own trees.")
        return redirect('dashboard')
    try:
        tree = Tree.objects.get(id=tree_id)
    except Tree.DoesNotExist:
        messages.error(request, "Tree not found.")
        return redirect('dashboard')

    if request.method == 'POST':
        species = request.POST.get('species')
        location = request.POST.get('location')
        zip_code = request.POST.get('zip_code')
        date_found = request.POST.get('date_found')
        notes = request.POST.get('notes')

        errors = []
        if len(species) < 2:
            errors.append("Species must be at least 2 characters long.")
        if len(location) < 5:
            errors.append("Location must be at least 5 characters long.")
        if not len(zip_code) == 5:
            errors.append("Zip code must be exactly 5 numbers long.")
        if zip_code and not zip_code.isdigit():
            errors.append("Zip code must contain only numbers.")
        if date_found > datetime.now().strftime('%Y-%m-%d'):
            errors.append("Date found cannot be in the future.")
        if notes and len(notes) > 50:
            errors.append("Notes cannot exceed 50 characters.")

        if not errors:
            tree.species = species
            tree.location = location
            tree.zip_code = zip_code
            tree.date_found = date_found
            tree.notes = notes
            tree.save()
            messages.success(request, "Tree updated successfully.")
            return redirect('dashboard')
        else:
            for error in errors:
                messages.error(request, error)
            return render(request, 'edit_tree.html', {'tree': tree, 'user': user})
    return render(request, 'edit_tree.html', {'tree': tree, 'user': user})


def delete_tree(request, tree_id):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to delete a tree.")
        return redirect('index')
    if 'user_id' == 'mapped_by':
        messages.error(request, "You can only edit your own trees.")
        return redirect('dashboard')
    try:
        tree = Tree.objects.get(id=tree_id)
    except Tree.DoesNotExist:
        messages.error(request, "Tree not found.")
        return redirect('dashboard')

    tree.delete()
    messages.success(request, "Tree deleted successfully.")
    return redirect('dashboard')


def visit_tree(request, tree_id):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to visit a tree.")
        return redirect('index')
    try:
        tree = Tree.objects.get(id=tree_id)
    except Tree.DoesNotExist:
        messages.error(request, "Tree not found.")
        return redirect('dashboard')
    user = User.objects.get(id=request.session['user_id'])
    tree.visitors.add(user)
    messages.success(request, "Thank you for visiting this tree!")
    return redirect('tree_details', tree_id=tree_id)


def zip_code(request, zip_code):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view zip code data.")
        return redirect('index')

    user = User.objects.get(id=request.session['user_id'])
    zip_code_trees = Tree.objects.filter(
        zip_code=zip_code).order_by('-date_found')

    context = {
        'user': user,
        'zip_code': zip_code,
        'zip_code_trees': zip_code_trees
    }
    return render(request, 'zip_code.html', context)
