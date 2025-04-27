from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, permissions
from .models import Lead
from customers.models import Customer
from .serializers import LeadSerializer
from rest_framework import viewsets

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]  


    # Add the "convert" action
    @action(detail=True, methods=['post'])
    def convert_to_customer(self, request, pk=None):
        lead = self.get_object()
        
        # Create customer from lead data
        customer_data = {
            'name': lead.name,
            'email': lead.email,
            'phone': lead.phone,
        }
        
        # Create customer
        customer = Customer.objects.create(**customer_data)
        
        # Optionally delete or archive lead
        lead.delete()

        return Response({"message": "Lead converted to customer successfully!", "customer_id": customer.id}, status=status.HTTP_200_OK)

    