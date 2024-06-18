def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    Each student document must contain the average score with key 'averageScore'.
    """
    # Calculate the average score for each student
    pipeline = [
        {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': { '$avg': '$topics.score' }
            }
        },
        {
            '$sort': { 'averageScore': -1 }
        }
    ]
    
    return list(mongo_collection.aggregate(pipeline))
