from feedback.forms import FeedbackForm, OrderFeedbackForm


def feedback_form(request):
    feedback_form = None
    feedback_form = FeedbackForm()
    if request.user.is_authenticated():
        feedback_form = FeedbackForm()
    return {'feedback_form': feedback_form}


def order_feedback_form(request):
    order_feedback_form = None
    order_feedback_form = OrderFeedbackForm()
    # if request.user.is_authenticated():
    #     order_feedback_form = OrderFeedbackForm()
    return {'order_feedback_form': order_feedback_form}
