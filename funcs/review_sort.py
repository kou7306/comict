from datetime import datetime

def review_sort(sort_option, reviews):
    if sort_option == 'evaluation_desc':
        return sorted(reviews, key=lambda r: r.to_dict()['evaluation'], reverse=True)
    elif sort_option == 'evaluation_asc':
        return sorted(reviews, key=lambda r: r.to_dict()['evaluation'])
    elif sort_option == 'newest':
        return sorted(reviews, key=lambda r: r.to_dict()['created_at'], reverse=True)
    elif sort_option == 'oldest':
        return sorted(reviews, key=lambda r: r.to_dict()['created_at'])
    else:
        return reviews