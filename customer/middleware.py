from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class LogRequestURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        byPass = {
            "home", "aboutus", "contactus", "register", "SelectRegion",
            "SelectedRegion", "get-cities", "agency", "agency_login_check",
            "admin_login_check", "login_check","agency_store","user_store",
            "ForgetPassword","ForgetPassword_chk"
        }

        # Log the requested URL
        print("Requested URL:", request.path)

        path_parts = request.path.strip('/').split('/')
        print("Path Parts:", path_parts)

        if not path_parts or len(path_parts) == 0:
            return None  # Allow root path

        main_section = path_parts[0] if len(path_parts) > 0 else ''
        page_name = path_parts[1] if len(path_parts) > 1 else ''

        # Allow login pages to prevent infinite loops
        if request.path in ["/customer/", "/myadmin/", "/agency/"]:
            return None  

        # Customer Section
        if main_section == 'customer':
            print("Customer Session:", request.session.get('user_id'))
            if page_name in byPass:
                return None  
            if not request.session.get('user_id'):
                return redirect('/customer/')  # Redirect to login page

        # Admin Section
        elif main_section == 'myadmin':
            print("Admin Session:", request.session.get('admin_id'))
            if page_name in byPass:
                return None  
            if not request.session.get('admin_id'):
                return redirect('/myadmin/')  # Redirect to admin login page

        # Agency Section
        elif main_section == 'agency':
            print("Agency Session:", request.session.get('agency_id'))
            if page_name in byPass:
                return None  
            if not request.session.get('agency_id'):
                print("Redirecting to /agency/")
                return redirect('/agency/')  # Correct agency login page

        return None  
