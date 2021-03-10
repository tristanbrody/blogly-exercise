from models import User, Post, db

def seed():
    db.drop_all()
    db.create_all()

    user1 = User(first_name="ash", last_name='g', profile_image_url='https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=1.00xw:0.669xh;0,0.190xh&resize=640:*')
    user2 = User(first_name='tristo', last_name='brobo', profile_image_url='https://thezebra.org/wp-content/uploads/2020/07/Training-Time-Aug2020-GR-with-ball-scaled.jpg')

    db.session.add_all([user1, user2])
    db.session.commit()

