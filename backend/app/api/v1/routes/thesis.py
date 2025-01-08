from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from backend.services.thesisservice import ThesisService
from backend.utils.auth import jwt_required

thesis_bp = Blueprint(
    "thesis_api",
    __name__,
    url_prefix="/api/v1/thesis",
    template_folder="templates",
    static_folder="static",
)

thesis_service = ThesisService()

@thesis_bp.route("/theses", methods=["GET"])
@jwt_required
def list_theses():
    """
    Display all theses created by the current user.
    """
    user_id = g.user_id
    theses = thesis_service.get_user_theses(user_id)
    return render_template("thesis/list.html", theses=theses)


@thesis_bp.route("/thesis/create", methods=["GET", "POST"])
@jwt_required
def create_thesis():
    """
    Create a new thesis.
    """
    user_id = g.user_id
    if request.method == "POST":
        title = request.form["title"]
        abstract = request.form["abstract"]
        status = request.form["status"]

        success = thesis_service.create_thesis(
            user_id, {"title": title, "abstract": abstract, "status": status}
        )
        if success:
            flash("Thesis created successfully!", "success")
            return redirect(url_for("thesis_api.list_theses"))
        else:
            flash("Failed to create thesis. Please try again.", "error")

    return render_template("thesis/create.html")


@thesis_bp.route("/thesis/<int:thesis_id>/edit", methods=["GET", "POST"])
@jwt_required
def edit_thesis(thesis_id):
    """
    Edit an existing thesis.
    """
    user_id = g.user_id
    thesis = thesis_service.get_thesis_by_id(thesis_id, user_id)
    if not thesis:
        flash("You do not have permission to edit this thesis.", "error")
        return redirect(url_for("thesis_api.list_theses"))

    if request.method == "POST":
        updated_data = {
            "title": request.form["title"],
            "abstract": request.form["abstract"],
            "status": request.form["status"],
        }
        success = thesis_service.update_thesis(thesis_id, user_id, updated_data)
        if success:
            flash("Thesis updated successfully!", "success")
            return redirect(url_for("thesis_api.list_theses"))
        else:
            flash("Failed to update thesis. Please try again.", "error")

    return render_template("thesis/edit_profile.html", thesis=thesis)


@thesis_bp.route("/thesis/<int:thesis_id>/delete", methods=["POST"])
@jwt_required
def delete_thesis(thesis_id):
    """
    Delete a thesis.
    """
    user_id = g.user_id
    success = thesis_service.delete_thesis(thesis_id, user_id)
    if success:
        flash("Thesis deleted successfully!", "success")
    else:
        flash("Failed to delete thesis. Please try again.", "error")

    return redirect(url_for("thesis_api.list_theses"))
