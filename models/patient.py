from odoo import models, fields, api


class Patient(models.Model):
    _name = "patient.patient"
    _description = "Patient Class"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(
        string="Name",
        required=True,
        copy=False,
        index=True,
        store=True,
        track_visibility="always",
    )
    dob = fields.Date(string="Date of Birth", required=True)
    age = fields.Float(string="Age")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")],
        string="Gender",
        required=True,
    )
    doctor_ids = fields.One2many(
        "doctor.doctor", "patient_id", string="Doctors", track_visibility="always"
    )
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone", required=True)
    address = fields.Char(string="Address", required=True)


class Doctor(models.Model):
    _name = "doctor.doctor"
    _description = "Doctor Management"
    # _order = "id desc"

    name = fields.Char("Name", require=True, copy=False, index=True, store=True)
    patient_id = fields.Many2one("patient.patient")
    dept_id = fields.Many2one("doc.department", string="Department")
    license_no = fields.Char(string="License No")
    app_date = fields.Date(string="Appointment Date")


class Department(models.Model):
    _name = "doc.department"
    _description = "Department"

    name = fields.Char(string="Name")


class Appointment(models.Model):
    _name = "appointment.appointment"
    _description = "Appointment Management"

    name = fields.Char(
        string="Name", copy=False, index=True, store=True, track_visibility="always"
    )
    patient_id = fields.Many2one("patient.patient")
    doctor_id = fields.Many2one("doctor.doctor")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    urgency_level = fields.Selection(
        [("urgent", "URGENT"), ("non-urgent", "NON-URGENT")],
        string="Urgency Level",
    )
    state = fields.Selection(
        [("new", "NEW"), ("in-progress", "IN-PROGRESS"), ("end", "END")],
        string="Status",
        default="new",
    )
    comments = fields.Text(string="Comments")

    def action_start(self):
        self.write({"state": "in-progress"})

    def action_end(self):
        self.write({"state": "end"})

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = (
                self.env["ir.sequence"].next_by_code("centroid.application") or "/"
            )
        return super(Appointment, self.with_context([])).create(vals)
