import pytz
from datetime import datetime

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone_name = request.META.get('HTTP_USER_TIMEZONE', 'UTC')

        # Convert datetime fields in request data
        if request.method in ['POST', 'PUT', 'PATCH']:
            request_data = getattr(request, request.method)
            self.convert_datetimes(request_data, timezone_name)

        response = self.get_response(request)

        # Convert datetime fields in response data
        if response.status_code == 200 and response.data:
            self.convert_datetimes(response.data, timezone_name)

        return response

    def convert_datetimes(self, data, timezone_name):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and self.is_datetime_string(value):
                    data[key] = self.convert_to_timezone(value, timezone_name)
                elif isinstance(value, dict) or isinstance(value, list):
                    self.convert_datetimes(value, timezone_name)
        elif isinstance(data, list):
            for item in data:
                self.convert_datetimes(item, timezone_name)

    def is_datetime_string(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%dT%H:%M')
            return True
        except ValueError:
            return False

    def convert_to_timezone(self, value, timezone_name):
        user_timezone = pytz.timezone(timezone_name)
        dt = datetime.strptime(value, '%Y-%m-%dT%H:%M').replace(tzinfo=user_timezone)
        return dt.astimezone(user_timezone).strftime('%d-%m-%Y %H:%M:%S')  # Convert to UTC format
    


import logging

logger = logging.getLogger(__name__)

class LogUnhandledExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.exception('Unhandled exception occurred')