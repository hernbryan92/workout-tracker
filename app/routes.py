from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Workout
from sqlalchemy import func
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/', methods =["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        exercise = request.form.get("exercise", "").strip()
        
        try:
            sets_i = int(request.form.get("sets", ""))
            reps_i = int(request.form.get("reps", ""))
            weight_f = float(request.form.get("weight", ""))
        except ValueError:
            return "Invalid numbers. Please go back and try again", 400
        
        if not exercise:
            return "Exercise is required.", 400
        if sets_i <= 0 or reps_i <= 0 or weight_f < 0:
            return "Sets and reps must be positive integers, weight must be non-negative.", 400
        
        workout = Workout(
            exercise=exercise,
            sets=int(sets_i),
            reps=int(reps_i),
            weight=weight_f,
            user_id=current_user.id
        )
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('main.home'))
    
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.created_at.desc()).all()
    return render_template('home.html', workouts=workouts, username=current_user.username)

@main.route("/delete/<int:workout_id>", methods=["POST"])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.filter_by(id=workout_id, user_id=current_user.id).first()
    if workout:
        db.session.delete(workout)
        db.session.commit()
    return redirect(url_for('main.home'))

@main.route("/stats")
@login_required
def stats():
    total_workouts = Workout.query.filter_by(user_id=current_user.id).count()

    unique_exercises = (
        db.session.query(func.count(func.distinct(Workout.exercise)))
        .filter(Workout.user_id == current_user.id)
        .scalar()
    )

    most_common = (
        db.session.query(Workout.exercise, func.count(Workout.id))
        .filter(Workout.user_id == current_user.id)
        .group_by(Workout.exercise)
        .order_by(func.count(Workout.id).desc())
        .first()
    )
    most_common_exercise = most_common[0] if most_common else None
    most_common_count = most_common[1] if most_common else 0

    # PRs max weight per exercise

    prs = (
        db.session.query(
            Workout.exercise, 
            func.max(Workout.weight).label("max_weight")
    )
        .filter(Workout.user_id == current_user.id)
        .group_by(Workout.exercise)
        .order_by(func.max(Workout.weight).desc())
        .all()
    )

    # Workouts in last 7 days
    cutoff = datetime.utcnow() - timedelta(days=7)
    last_7_days = (
        Workout.query.filter(
            Workout.user_id == current_user.id,
            Workout.created_at >= cutoff
        ).count()
    )

    return render_template(
        'stats.html',
        total_workouts=total_workouts,
        unique_exercises=unique_exercises,
        most_common_exercise=most_common_exercise,
        most_common_count=most_common_count,
        prs=prs,
        last_7_days=last_7_days,
        username=current_user.username
    )