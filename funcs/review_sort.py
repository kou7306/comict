from flask import session
from firebase_admin import firestore
from firebaseSetUp import db
from datetime import datetime

# def review_sort(sort_option, reviews):
#     if sort_option == 'evaluation_desc':
#         return sorted(reviews, key=lambda r: r.to_dict()['evaluation'], reverse=True)
#     elif sort_option == 'evaluation_asc':
#         return sorted(reviews, key=lambda r: r.to_dict()['evaluation'])
#     elif sort_option == 'newest':
#         return sorted(reviews, key=lambda r: datetime.strptime(r.to_dict()['created_at'], "%Y-%m-%d %H:%M:%S"), reverse=True)
#     elif sort_option == 'oldest':
#         return sorted(reviews, key=lambda r: datetime.strptime(r.to_dict()['created_at'], "%Y-%m-%d %H:%M:%S"))
#     else:
#         return reviews

def review_sort(sort_option, title=None):
    user_id = session.get("user_id")
    user_doc_ref = db.collection('user')
    review_doc_ref = db.collection('review')
    query = review_doc_ref
    
    if title:
        query = query.where('mangaTitle', '==', title)
    
    if sort_option == 'newest':
        query = query.order_by('created_at', direction=firestore.Query.DESCENDING)
    elif sort_option == 'oldest':
        query = query.order_by('created_at', direction=firestore.Query.ASCENDING)
    elif sort_option == 'likes_count_desc':
        query = query.order_by('likes_count', direction=firestore.Query.DESCENDING)
    elif sort_option == 'likes_count_asc':
        query = query.order_by('likes_count', direction=firestore.Query.ASCENDING)
    elif sort_option == 'evaluation_desc':
        query = query.order_by('evaluation', direction=firestore.Query.DESCENDING)
    elif sort_option == 'evaluation_asc':
        query = query.order_by('evaluation', direction=firestore.Query.ASCENDING)
    else:
        query = query.order_by('evaluation', direction=firestore.Query.DESCENDING)
    
    reviews_snapshot = query.get()
    
    reviews = []
    for review in reviews_snapshot:
        review_data = review.to_dict()
        review_data['id'] = review.id
        
        r_user_id = review_data.get('user_id')
        if r_user_id:
            user_doc = user_doc_ref.document(r_user_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                r_username = user_data.get('username')
                review_data['username'] = r_username
        
        likes = review_data.get('likes', [])
        if user_id in likes:
            review_data['liked'] = True
        else:
            review_data['liked'] = False
            
        reviews.append(review_data)
    
    return reviews