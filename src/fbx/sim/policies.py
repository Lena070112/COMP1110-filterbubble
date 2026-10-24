"""Permitted intervention policies. Each sees only observable records + remaining budget.
act(t, shown, rec, label_fn, budget) -> effort spent this step."""


class Policy:
    name = "base"

    def act(self, t, shown, rec, label_fn, budget):
        return 0


class NoIntervention(Policy):
    name = "none"


class TopicFilter(Policy):
    name = "topic_filter"

    def act(self, t, shown, rec, label_fn, budget):
        if t == 0 and budget >= 1:
            rec.blocked_topics.add("parenting")
            return 1
        return 0


class NegativeFeedback(Policy):
    """Press 'not interested' on shown items that (by the noisy report label) carry the unwanted claim."""
    name = "negative_feedback"

    def act(self, t, shown, rec, label_fn, budget):
        spent = 0
        for it in shown:
            if spent < budget and label_fn(it) == "strict":
                rec.not_interested(it)
                spent += 1
        return spent


class SelectiveFilterPlusSupplement(Policy):
    name = "selective_filter+supplement"

    def act(self, t, shown, rec, label_fn, budget):
        if t == 0 and budget >= 4:
            rec.filter_stances.add("strict")
            rec.boost.update({"alt": 2.0, "balanced": 1.5})
            return 4
        return 0


class SearchFollow(Policy):
    name = "search_follow"

    def act(self, t, shown, rec, label_fn, budget):
        if t % 10 == 0 and budget >= 1:
            rec.boost["alt"] = rec.boost.get("alt", 1.0) * 1.3
            rec.boost["balanced"] = rec.boost.get("balanced", 1.0) * 1.15
            return 1
        return 0


ALL = [NoIntervention, TopicFilter, NegativeFeedback, SelectiveFilterPlusSupplement, SearchFollow]
