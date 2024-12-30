from . import models
from . import serializers
from rest_framework import viewsets, status
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.response import Response

class ContactViewsets(viewsets.ModelViewSet):
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializers

    def create(self, request, *args, **kwargs):
        # Use the serializer to validate and save the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        name = serializer.validated_data.get('Name')
        email = serializer.validated_data.get('email')
        message = serializer.validated_data.get('message')

        # Compose the email content
        email_subject = f"New Contact Submission from {name}"
        email_message = (
            f"Hello,\n\n"
            f"You have received a new contact submission from your website:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Message: {message}\n\n"
            f"Best regards,\n"
            f"Rabiul Pramanik"
        )

        try:
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=email,
                recipient_list=['robiul.drubok@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {"detail": f"Error sending email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # Return the created data response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
