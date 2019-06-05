def check_fiscal_code(fiscal_code):
    """
    Mock function that emulates the interaction with the legacy system containing administrative
    information about students and teachers. It checks if the fiscal code is associated to a student
    or a teacher.
    :param fiscal_code: Fiscal code to check in the legacy system
    :return: teacher, if the fiscal_code is associated to a teacher, student, if it is associated to
             a student, None otherwise.
    """
    if fiscal_code == "teacher":
        return "teacher"
    elif fiscal_code == "student":
        return "student"
    else:
        return None
