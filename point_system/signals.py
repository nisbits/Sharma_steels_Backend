from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContractorPoints, ContractorPointSummary
from django.db.models import Sum
@receiver(post_save, sender=ContractorPoints)
def update_total_points(sender, instance, **kwargs):
    print("signal fired")
    summary, _ = ContractorPointSummary.objects.get_or_create(
        contractor_code=instance.contractor_code
    )
    summary.total_points = ContractorPoints.objects.filter(
        contractor_code=instance.contractor_code
    ).aggregate(total=Sum('points'))['total'] or 0
    summary.save()

from django.db.models.signals import post_save, post_delete

@receiver(post_delete, sender=ContractorPoints)
def update_total_points_on_delete(sender, instance, **kwargs):
    contractor_code = instance.contractor_code

    total = ContractorPoints.objects.filter(contractor_code=contractor_code).aggregate(
        total=Sum('points')
    )['total'] or 0

    if total == 0:
        # Either update to 0 or delete the summary record
        ContractorPointSummary.objects.filter(contractor_code=contractor_code).delete()
    else:
        ContractorPointSummary.objects.update_or_create(
            contractor_code=contractor_code,
            defaults={'total_points': total}
        )
