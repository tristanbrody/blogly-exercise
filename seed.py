from models import User, Post, Tag, PostTag, db

def seed():
    db.drop_all()
    db.create_all()

    user1 = User(first_name="ash", last_name='g', profile_image_url='https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=1.00xw:0.669xh;0,0.190xh&resize=640:*')
    user2 = User(first_name='tristo', last_name='brobo', profile_image_url='https://thezebra.org/wp-content/uploads/2020/07/Training-Time-Aug2020-GR-with-ball-scaled.jpg')

    db.session.add_all([user1, user2])
    db.session.commit() 

    post1 = Post(title="I want pizza",content="Pizza would be nice given I'm starving to death", posted_by=2)
    post2 = Post(title="Why is the weekend so suffocatingly, brutally short?", content="just wondering", posted_by=1)

    db.session.add_all([post1, post2])
    db.session.commit()

    tag1 = Tag(name="food")
    tag2 = Tag(name="existential")
    
    db.session.add_all([tag1, tag2])
    db.session.commit()     

    posttag1 = PostTag(post_id=1, tag_id=1)
    posttag2 = PostTag(post_id=2, tag_id=2)

    db.session.add_all([posttag1, posttag2])
    db.session.commit()
