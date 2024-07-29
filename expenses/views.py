from rest_framework import viewsets, status
from rest_framework.response import Response
from decimal import Decimal
from .models import User, Expense, ExpenseParticipant
from .serializers import UserSerializer, ExpenseSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        split_method = data['split_method']
        total_amount = Decimal(data['amount'])
        participants = data['participants']

        # Handle split_method logic
        if split_method == 'equal':
            if not participants:
                return Response({"error": "No participants provided"}, status=status.HTTP_400_BAD_REQUEST)
            amount_per_person = total_amount / len(participants)
            for participant in participants:
                participant['amount'] = round(amount_per_person, 2)
                participant.pop('percentage', None)  # Remove percentage if not needed

        elif split_method == 'percentage':
            total_percentage = sum(Decimal(p['percentage']) for p in participants)
            if total_percentage != Decimal('100'):
                return Response({"error": "Percentages must add up to 100%"}, status=status.HTTP_400_BAD_REQUEST)

            for participant in participants:
                participant['amount'] = round((Decimal(participant['percentage']) / Decimal('100')) * total_amount, 2)

        elif split_method == 'exact':
            if sum(Decimal(p['amount']) for p in participants) != total_amount:
                return Response({"error": "Exact amounts must sum up to total amount"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Expense object
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        expense = serializer.save()

        # Create ExpenseParticipant objects
        for participant_data in participants:
            user_id = participant_data.get('user')  # Fetch user ID
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    # Remove 'user' from participant_data before passing to create()
                    participant_data.pop('user', None)
                    # Ensure 'amount' or 'percentage' is present in participant_data
                    if 'amount' not in participant_data and 'percentage' not in participant_data:
                        return Response({"error": "Either 'amount' or 'percentage' must be provided for each participant"}, status=status.HTTP_400_BAD_REQUEST)
                    # Create ExpenseParticipant object with User instance
                    ExpenseParticipant.objects.create(expense=expense, user=user, **participant_data)
                except User.DoesNotExist:
                    return Response({"error": f"User with ID {user_id} not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "User ID is missing in participant data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
