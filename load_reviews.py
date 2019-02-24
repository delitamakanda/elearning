import sys, os
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myelearning.settings")

import django
django.setup()

from students.models import User
from courses.models import Review, Course

def save_review_from_row(review_row):
    review = Review()
    review.id = review_row[0]
    review.course = Course.objects.get(title=review_row[1])
    review.pub_date = datetime.datetime.now()
    review.user_name = User.objects.get(username=review_row[3])
    review.comment = review_row[4]
    review.rating = review_row[5]
    review.save()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        reviews_df = pd.read_csv(sys.argv[1])
        print(reviews_df)

        reviews_df.apply(
            save_review_from_row,
            axis=1
        )

        print("There are {} reviews in DB".format(Review.objects.count()))

    else:
        print("Provide Reviews file path")
