from flask import session
from firebase_admin import firestore
from firebaseSetUp import db

# 特定のユーザーのレビューを取得する関数
def review_sort_for_user(user_id,last_document_id,title=None):
    user_doc_ref = db.collection('user')
    review_doc_ref = db.collection('review')
    comics_doc_ref = db.collection('comics')
    query = review_doc_ref.where('user_id', '==', user_id)
    
    if title:
        query = query.where('mangaTitle', '==', title)

    # Get the last document
    if last_document_id is not None:
        last_document_snapshot = review_doc_ref.document(last_document_id).get()
        start_after = last_document_snapshot
    else:
        start_after = None

    # Apply start_after
    if start_after:
        query = query.start_after(start_after)

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
            
        r_mangaTitle = review_data.get('mangaTitle')
        if r_mangaTitle:
            comics_doc = comics_doc_ref.document(r_mangaTitle).get()
            if comics_doc.exists:
                comics_data = comics_doc.to_dict()
                r_mangaimage = comics_data.get('image')
                review_data['image'] = r_mangaimage

        likes = review_data.get('likes', [])
        if user_id in likes:
            review_data['liked'] = True
        else:
            review_data['liked'] = False

        reviews.append(review_data)

    return reviews