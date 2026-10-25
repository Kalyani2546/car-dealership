def dealer_data(dealer):
    return {
        "id": dealer.id,
        "name": dealer.name,
        "city": dealer.city,
        "state": dealer.state,
        "address": dealer.address,
        "zip": dealer.zip_code,
        "phone": dealer.phone,
        "website": dealer.website,
        "image_url": dealer.image_url,
    }


def review_data(review):
    return {
        "id": review.id,
        "dealer_id": review.dealer_id,
        "username": review.user.get_username(),
        "rating": review.rating,
        "review": review.review,
        "created_at": review.created_at.isoformat(),
    }
