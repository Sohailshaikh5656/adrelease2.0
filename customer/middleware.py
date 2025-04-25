from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class LogRequestURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # URLs or page names that don't require login
        byPass = {
            "home", "aboutus", "contactus", "register", "SelectRegion",
            "SelectedRegion", "get-cities", "agency", "agency_login_check",
            "admin_login_check", "login_check", "agency_store", "user_store",
            "ForgetPassword", "ForgetPassword_chk","Agency_ForgetPassword","Agency_ForgetPassword_chk"
        }

        # Log full path and method
        print(f"Requested URL: {request.path}, Method: {request.method}")

        # Break path into parts
        path_parts = request.path.strip('/').split('/')
        print("Path Parts:", path_parts)

        # Extract main section and page name
        main_section = path_parts[0] if len(path_parts) > 0 else ''
        page_name = path_parts[1] if len(path_parts) > 1 else ''

        # Allow direct access to login root pages to prevent infinite redirect loop
        if request.path in ["/customer/", "/myadmin/", "/agency/"]:
            return None  

        # ----------------- Customer Section -----------------
        if main_section == 'customer':
            print("Customer Section Accessed")
            print("Customer Session:", request.session.get('user_id'))
            print("Page Name:", page_name)
            
            if page_name in byPass:
                print("Customer Page is bypassed")
                return None  

            if not request.session.get('user_id'):
                print("Redirecting to Customer Login Page")
                return redirect('/customer/')

        # ----------------- Admin Section -----------------
        elif main_section == 'myadmin':
            print("Admin Section Accessed")
            print("Admin Session:", request.session.get('admin_id'))
            print("Page Name:", page_name)

            if page_name in byPass:
                print("Admin Page is bypassed")
                return None  

            if not request.session.get('admin_id'):
                print("Redirecting to Admin Login Page")
                return redirect('/myadmin/')

        # ----------------- Agency Section -----------------
        elif main_section == 'agency':
            print("Agency Section Accessed")
            print("Agency Session:", request.session.get('agency_id'))
            print("Page Name:", page_name)

            if page_name in byPass:
                print("Agency Page is bypassed")
                return None  

            if not request.session.get('agency_id'):
                print("Redirecting to Agency Login Page")
                return redirect('/agency/')
        elif request.path.startswith('/rozar-pay/'):
            return None

        # No restriction if none of the above match
        return None
