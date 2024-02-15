from flask import session
from firebase_admin import firestore
from firebaseSetUp import db

def review_sort(sort_option,last_document_id,limit=4,title=None):
    user_id = session.get("user_id")
    user_doc_ref = db.collection('user')
    review_doc_ref = db.collection('review')
    query = review_doc_ref
    
    if title:
        query = query.where('mangaTitle', '==', title)
    # Get the last document
    if last_document_id is not None:
        last_document_snapshot = review_doc_ref.document(last_document_id).get()
        start_after = last_document_snapshot
    else:
        start_after = None


    # Get the field value to start after based on sort_option
 


    # Apply sorting
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

    # Apply start_after
    if start_after:
        query = query.start_after(start_after)

    # Apply limit
    query = query.limit(limit)

    # Get the next documents
    reviews_snapshot = query.get()

    # Process the documents
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
