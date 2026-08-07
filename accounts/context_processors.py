from events.models import Participant


def participant_profile(request):

    participant = None

    if request.user.is_authenticated:

        participant = Participant.objects.filter(
            user=request.user
        ).first()

    return {
        "participant": participant,
    }