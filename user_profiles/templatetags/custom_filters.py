from django import template

register = template.Library()


@register.filter
def assigned_tutor(subjects):
    mary_subjects = {"English SL", "English HL", "Extended Essay (EE)", "TOK"}
    ivan_subjects = {"Math SL", "Math HL", "Physics SL", "Physics HL"}

    subject_names = set(subject.name for subject in subjects.all())

    if subject_names & ivan_subjects:
        return "Ivan"
    elif subject_names & mary_subjects:
        return "Mary"
    return "Unassigned"
