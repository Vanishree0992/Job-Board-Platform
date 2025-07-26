from flask import Blueprint, render_template, redirect, url_for, request, flash
from extensions import db, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Job, Application, PricingPlan
from forms import RegisterForm, LoginForm, JobForm, ApplicationForm
from utils import save_resume
import os

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/')
def home():
    jobs = Job.query.order_by(Job.posted_on.desc()).all()
    plans = PricingPlan.query.all()
    return render_template('job_list.html', jobs=jobs, plans=plans)

@main.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(name=form.name.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u); db.session.commit()
        flash('Registered! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.check_password(form.password.data):
            login_user(u)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    jobs = Job.query.filter_by(employer_id=current_user.id).all()
    return render_template('dashboard.html', jobs=jobs)

@main.route('/post_job', methods=['GET','POST'])
@login_required
def post_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, description=form.description.data, employer=current_user)
        db.session.add(job); db.session.commit()
        flash('Job posted.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('post_job.html', form=form)

@main.route('/job/<int:job_id>', methods=['GET','POST'])
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    form = ApplicationForm()
    applied = False
    if form.validate_on_submit():
        filename = save_resume(form.resume.data)
        appn = Application(name=form.name.data, email=form.email.data,
                           resume_filename=filename, job=job, applicant=current_user)
        db.session.add(appn); db.session.commit()
        flash('Application submitted.', 'success')
        applied = True
    return render_template('job_detail.html', job=job, form=form, applied=applied)

@main.route('/applicants/<int:job_id>')
@login_required
def applicants(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('applicants.html', job=job, applications=job.applications)

@main.route('/analytics')
@login_required
def analytics():
    jobs = Job.query.filter_by(employer_id=current_user.id).all()
    total_apps = sum(len(job.applications) for job in jobs)
    return render_template('analytics.html', jobs=jobs, total_apps=total_apps)

@main.route('/pricing')
def pricing():
    plans = PricingPlan.query.all()
    return render_template('pricing.html', plans=plans)
