from .models import Split

def calculate_equal_split(expense, participants):
    amount = expense.amount
    split_amount = amount / len(participants)
    return [{'user': user, 'split_amount': split_amount} for user in participants]

def calculate_exact_split(expense, participants, amounts):
    return [{'user': participants[i], 'split_amount': amounts[i]} for i in range(len(participants))]

def calculate_percentage_split(expense, participants, percentages):
    amount = expense.amount
    return [{'user': participants[i], 'split_amount': amount * (percentages[i] / 100)} for i in range(len(participants))]

def save_splits(splits):
    for split in splits:
        Split.objects.create(user=split['user'], expense=split['expense'], amount=split['split_amount'])
