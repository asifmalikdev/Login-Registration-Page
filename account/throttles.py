from rest_framework.throttling import AnonRateThrottle
class RegistrationThrottleRate(AnonRateThrottle):
    rate='20/hour'
class LoginThrottleRate(AnonRateThrottle):
    rate = "10/hour"