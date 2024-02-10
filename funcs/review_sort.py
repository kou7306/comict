from datetime import datetime

def review_sort(sort_option, reviews):
    if sort_option == 'evaluation_desc':
        return sorted(reviews, key=lambda r: r.to_dict()['evaluation'], reverse=True)
    elif sort_option == 'evaluation_asc':
        return sorted(reviews, key=lambda r: r.to_dict()['evaluation'])
    elif sort_option == 'newest':
        return sorted(reviews, key=lambda r: datetime.strptime(r.to_dict()['created_at'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    elif sort_option == 'oldest':
        return sorted(reviews, key=lambda r: datetime.strptime(r.to_dict()['created_at'], "%Y-%m-%d %H:%M:%S"))
    else:
        return reviews